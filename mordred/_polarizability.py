from ._atomic_property import Polarizabilities78, Polarizabilities94
from ._base import Descriptor


class PolarizabilityBase(Descriptor):
    @classmethod
    def preset(cls):
        yield cls()

    def __str__(self):
        return self.__class__.__name__.lower() + ('78' if self._use78 else '')

    def __init__(self, use78=False):
        self._use78 = use78

    def _get_table(self):
        return Polarizabilities78 if self._use78 else Polarizabilities94


class APol(PolarizabilityBase):
    r"""atomic polarizability descriptor.

    :type use78: bool
    :param use78: use old atomic polarizability data

    :rtype: float
    """

    __slots__ = ('_use78',)

    def calculate(self, mol):
        table = self._get_table()
        return sum(table[a.GetAtomicNum()] for a in mol.GetAtoms())


class BPol(PolarizabilityBase):
    r"""bond polarizability descriptor.

    :type use78: bool
    :param use78: use old atomic polarizability data

    :rtype: float
    """

    __slots__ = ('_use78',)

    def calculate(self, mol):
        table = self._get_table()

        def bond_pol(bond):
            a = bond.GetBeginAtom().GetAtomicNum()
            b = bond.GetEndAtom().GetAtomicNum()
            return abs(table[a] - table[b])

        return sum(bond_pol(b) for b in mol.GetBonds())
