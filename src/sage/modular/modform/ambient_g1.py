r"""
Modular forms for `\Gamma_1(N)` and `\Gamma_H(N)` over `\QQ`

EXAMPLES::

    sage: M = ModularForms(Gamma1(13),2); M
    Modular Forms space of dimension 13 for Congruence Subgroup Gamma1(13) of weight 2 over Rational Field
    sage: S = M.cuspidal_submodule(); S
    Cuspidal subspace of dimension 2 of Modular Forms space of dimension 13 for Congruence Subgroup Gamma1(13) of weight 2 over Rational Field
    sage: S.basis()
    [
    q - 4*q^3 - q^4 + 3*q^5 + O(q^6),
    q^2 - 2*q^3 - q^4 + 2*q^5 + O(q^6)
    ]

    sage: M = ModularForms(GammaH(11, [3])); M
    Modular Forms space of dimension 2 for Congruence Subgroup Gamma_H(11) with H generated by [3] of weight 2 over Rational Field
    sage: M.q_expansion_basis(8)
    [
    q - 2*q^2 - q^3 + 2*q^4 + q^5 + 2*q^6 - 2*q^7 + O(q^8),
    1 + 12/5*q + 36/5*q^2 + 48/5*q^3 + 84/5*q^4 + 72/5*q^5 + 144/5*q^6 + 96/5*q^7 + O(q^8)
    ]


TESTS::

    sage: m = ModularForms(Gamma1(20),2)
    sage: loads(dumps(m)) == m
    True

    sage: m = ModularForms(GammaH(15, [4]), 2)
    sage: loads(dumps(m)) == m
    True


We check that :trac:`10453` is fixed::

    sage: CuspForms(Gamma1(11), 2).old_submodule()
    Modular Forms subspace of dimension 0 of Modular Forms space of dimension 10 for Congruence Subgroup Gamma1(11) of weight 2 over Rational Field
    sage: ModularForms(Gamma1(3), 12).old_submodule()
    Modular Forms subspace of dimension 4 of Modular Forms space of dimension 5 for Congruence Subgroup Gamma1(3) of weight 12 over Rational Field

"""

#########################################################################
#       Copyright (C) 2006 William Stein <wstein@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#                  http://www.gnu.org/licenses/
#########################################################################

from sage.rings.rational_field import Q as QQ

import sage.modular.arithgroup.all as arithgroup

from . import ambient
from . import cuspidal_submodule
from . import eisenstein_submodule

from sage.misc.cachefunc import cached_method


class ModularFormsAmbient_gH_Q(ambient.ModularFormsAmbient):
    r"""
    A space of modular forms for the group `\Gamma_H(N)` over the rational numbers.
    """
    def __init__(self, group, weight, eis_only):
        r"""
        Create a space of modular forms for `\Gamma_H(N)` of integral weight over the
        rational numbers.

        EXAMPLES::

            sage: m = ModularForms(GammaH(100, [41]),5); m
            Modular Forms space of dimension 270 for Congruence Subgroup Gamma_H(100) with H generated by [41] of weight 5 over Rational Field
            sage: type(m)
            <class 'sage.modular.modform.ambient_g1.ModularFormsAmbient_gH_Q_with_category'>
        """
        ambient.ModularFormsAmbient.__init__(self, group, weight, QQ, eis_only=eis_only)

    ####################################################################
    # Computation of Special Submodules
    ####################################################################
    @cached_method
    def cuspidal_submodule(self):
        """
        Return the cuspidal submodule of this modular forms space.

        EXAMPLES::

            sage: m = ModularForms(GammaH(100, [29]),2); m
            Modular Forms space of dimension 48 for Congruence Subgroup Gamma_H(100) with H generated by [29] of weight 2 over Rational Field
            sage: m.cuspidal_submodule()
            Cuspidal subspace of dimension 13 of Modular Forms space of dimension 48 for Congruence Subgroup Gamma_H(100) with H generated by [29] of weight 2 over Rational Field
        """
        if self.level() == 1:
            return cuspidal_submodule.CuspidalSubmodule_level1_Q(self)
        elif self.weight() == 1:
            return cuspidal_submodule.CuspidalSubmodule_wt1_gH(self)
        else:
            return cuspidal_submodule.CuspidalSubmodule_gH_Q(self)

    @cached_method
    def eisenstein_submodule(self):
        """
        Return the Eisenstein submodule of this modular forms space.

        EXAMPLES::

            sage: E = ModularForms(GammaH(100, [29]),3).eisenstein_submodule(); E
            Eisenstein subspace of dimension 24 of Modular Forms space of dimension 72 for Congruence Subgroup Gamma_H(100) with H generated by [29] of weight 3 over Rational Field
            sage: type(E)
            <class 'sage.modular.modform.eisenstein_submodule.EisensteinSubmodule_gH_Q_with_category'>
        """
        return eisenstein_submodule.EisensteinSubmodule_gH_Q(self)

    def _compute_diamond_matrix(self, d):
        r"""
        Compute the matrix of the diamond operator <d> on this space.

        EXAMPLES::

            sage: ModularForms(GammaH(9, [4]), 7)._compute_diamond_matrix(2)
            [-1  0  0  0  0  0  0  0]
            [ 0 -1  0  0  0  0  0  0]
            [ 0  0 -1  0  0  0  0  0]
            [ 0  0  0 -1  0  0  0  0]
            [ 0  0  0  0 -1  0  0  0]
            [ 0  0  0  0  0 -1  0  0]
            [ 0  0  0  0  0  0 -1  0]
            [ 0  0  0  0  0  0  0 -1]
        """
        return self.cuspidal_submodule().diamond_bracket_matrix(d).block_sum(
            self.eisenstein_submodule().diamond_bracket_matrix(d))

    def _compute_hecke_matrix(self, n):
        r"""
        Compute the matrix of the Hecke operator T_n acting on this space.

        EXAMPLES::

            sage: ModularForms(Gamma1(7), 4).hecke_matrix(3) # indirect doctest
            [           0          -42          133            0            0            0            0            0            0]
            [           0          -28           91            0            0            0            0            0            0]
            [           1           -8           19            0            0            0            0            0            0]
            [           0            0            0           28            0            0            0            0            0]
            [           0            0            0   -10152/259            0      5222/37    -13230/37    -22295/37     92504/37]
            [           0            0            0    -6087/259            0  312067/4329 1370420/4329   252805/333 3441466/4329]
            [           0            0            0     -729/259            1       485/37      3402/37      5733/37      7973/37]
            [           0            0            0      729/259            0      -189/37     -1404/37     -2366/37     -3348/37]
            [           0            0            0      255/259            0  -18280/4329  -51947/4329   -10192/333 -190855/4329]
        """
        return self.cuspidal_submodule().hecke_matrix(n).block_sum(self.eisenstein_submodule().hecke_matrix(n))


class ModularFormsAmbient_g1_Q(ModularFormsAmbient_gH_Q):
    r"""
    A space of modular forms for the group `\Gamma_1(N)` over the rational numbers.
    """
    def __init__(self, level, weight, eis_only):
        r"""
        Create a space of modular forms for `\Gamma_1(N)` of integral weight over the
        rational numbers.

        EXAMPLES::

            sage: m = ModularForms(Gamma1(100),5); m
            Modular Forms space of dimension 1270 for Congruence Subgroup Gamma1(100) of weight 5 over Rational Field
            sage: type(m)
            <class 'sage.modular.modform.ambient_g1.ModularFormsAmbient_g1_Q_with_category'>
        """
        ambient.ModularFormsAmbient.__init__(self, arithgroup.Gamma1(level), weight, QQ, eis_only=eis_only)

    ####################################################################
    # Computation of Special Submodules
    ####################################################################
    @cached_method
    def cuspidal_submodule(self):
        """
        Return the cuspidal submodule of this modular forms space.

        EXAMPLES::

            sage: m = ModularForms(Gamma1(17),2); m
            Modular Forms space of dimension 20 for Congruence Subgroup Gamma1(17) of weight 2 over Rational Field
            sage: m.cuspidal_submodule()
            Cuspidal subspace of dimension 5 of Modular Forms space of dimension 20 for Congruence Subgroup Gamma1(17) of weight 2 over Rational Field
        """
        if self.level() == 1:
            return cuspidal_submodule.CuspidalSubmodule_level1_Q(self)
        elif self.weight() == 1:
            return cuspidal_submodule.CuspidalSubmodule_wt1_gH(self)
        else:
            return cuspidal_submodule.CuspidalSubmodule_g1_Q(self)

    @cached_method
    def eisenstein_submodule(self):
        """
        Return the Eisenstein submodule of this modular forms space.

        EXAMPLES::

            sage: ModularForms(Gamma1(13),2).eisenstein_submodule()
            Eisenstein subspace of dimension 11 of Modular Forms space of dimension 13 for Congruence Subgroup Gamma1(13) of weight 2 over Rational Field
            sage: ModularForms(Gamma1(13),10).eisenstein_submodule()
            Eisenstein subspace of dimension 12 of Modular Forms space of dimension 69 for Congruence Subgroup Gamma1(13) of weight 10 over Rational Field
        """
        return eisenstein_submodule.EisensteinSubmodule_g1_Q(self)
