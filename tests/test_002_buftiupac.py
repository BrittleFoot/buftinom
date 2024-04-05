import pytest

from buftinom.iupac import Iupac, iupac2str
from buftinom.smiles_parser import SmilesParser


@pytest.fixture
def parser():
    return SmilesParser(debug=True)


@pytest.mark.parametrize(
    "smiles,expected",
    [
        ("C", "methane"),
        ("CC", "ethane"),
        ("C=C", "ethene"),
        ("C#C", "ethyne"),
        #
        ("CCC", "propane"),
        ("C=CC", "propene"),
        ("C#CC", "propyne"),
        #
        ("CCCC", "butane"),
        ("C=CCC", "butene"),
        ("CCC=C", "butene"),
        ("C#CCC", "butyne"),
        ("CCC#C", "butyne"),
        ("CC=CC", "but-2-ene"),
        ("CC#CC", "but-2-yne"),
        #
        ("CCCCC", "pentane"),
        ("CC=CCC#CC", "hept-2-en-5-yne"),
        ("CCC=CC#CC", "hept-4-en-2-yne"),
        #
        ("C=C#C", "propen-2-yne"),
    ],
)
def test_simple_chain_name(parser, smiles, expected):
    (mol,) = parser.parse(smiles)
    iupac = Iupac(mol)
    name = iupac.decompose_name(iupac.decomposition)

    assert iupac2str(name) == expected


@pytest.mark.parametrize(
    "smiles,expected",
    [
        ("C", 1),
        ("CCCCCCCC(C(C)CC)C(C(C)=C=C)CCCCCC=C", 1),
    ],
)
def test_decomposed_chain_name(parser, smiles, expected):
    (mol,) = parser.parse(smiles)
    iupac = Iupac(mol)

    names = iupac.subchain_simple_names()

    for dec, connector, name in names:
        print(name, connector, dec.chain)


@pytest.mark.parametrize(
    "smiles,expected",
    [
        ("CCC(C=C)CCCC", 1),
    ],
)
def test_decomposed_chain_name(parser, smiles, expected):
    (mol,) = parser.parse(smiles)
    iupac = Iupac(mol)

    names = iupac.subchain_simple_names()

    for dec, connector, name in names:
        print(name, connector, dec.chain)


@pytest.mark.parametrize(
    "smiles,expected",
    [
        ("CCC(C)(C)CC", "3,3-dimethylpentane"),
        ("CC(C)CC(C)C", "2,4-dimethylpentane"),
        # Note here he found that it is hexane, ill provide numeration for clearance
        #  3 21 4   56
        ("CC(CC)C(C)CC", "3,4-dimethylhexane"),
        ("CCCCC(CC)C(C)CCC", "5-ethyl-4-methylnonane"),
    ],
)
def test_decomposed_multichain(parser, smiles, expected):
    (mol,) = parser.parse(smiles)
    iupac = Iupac(mol)

    mol.print_table()
    iupac.decomposition.print()

    name = iupac.decompose_name(iupac.decomposition)
    assert iupac2str(name) == expected
