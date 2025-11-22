from datetime import date
from decimal import Decimal
import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from ..database import Base
from ..models import VagaDeEmprego, Empresa
from .repository import VagaDeEmpregoRepository
from ..empresa.repository import EmpresaRepository


@pytest.fixture
def add_empresa(db):
    empresa = Empresa(
        id_empresa=1,
        nome_empresa="Empresa G",
        cnpj="12345671234567",
        cidade="Gama",
        estado="DF",
        descricao="A Gama Company",
    )
    return EmpresaRepository.createEmpresa(empresa, db)


@pytest.fixture
def sample_vaga_de_emprego(add_empresa):
    return VagaDeEmprego(
        id_empresa=1,
        nome_vaga_de_emprego="Desenvolvedor Backend",
        data=date(2023, 10, 28),
        cidade="São Paulo",
        estado="SP",
        salario=Decimal("8000.00"),
        cargo="Desenvolvedor Backend",
        nivel="Pleno",
        tipo_contrato="CLT",
        modalidade="Presencial",
        descricao="Vaga para desenvolvedor backend com experiência em Python e FastAPI.",
    )


def make_vagas_de_emprego():
    return [
        VagaDeEmprego(
            id_empresa=1,
            nome_vaga_de_emprego="Desenvolvedor Backend",
            data=date(2023, 10, 28),
            cidade="São Paulo",
            estado="SP",
            salario=Decimal("8000.00"),
            cargo="Desenvolvedor Backend",
            nivel="Pleno",
            tipo_contrato="CLT",
            modalidade="Presencial",
            descricao="Vaga para desenvolvedor backend com experiência em Python e FastAPI.",
        ),
        VagaDeEmprego(
            id_empresa=1,
            nome_vaga_de_emprego="Analista de Dados",
            data=date(2023, 10, 28),
            cidade="Rio de Janeiro",
            estado="RJ",
            salario=Decimal("6000.00"),
            cargo="Analista de Dados",
            nivel="Júnior",
            tipo_contrato="PJ",
            modalidade="Remoto",
            descricao="Vaga para analista de dados com experiência em SQL, Python e ferramentas de BI.",
        ),
        VagaDeEmprego(
            id_empresa=1,
            nome_vaga_de_emprego="Engenheiro de Software",
            data=date(2023, 10, 28),
            cidade="Belo Horizonte",
            estado="MG",
            salario=Decimal("12000.00"),
            cargo="Engenheiro de Software",
            nivel="Sênior",
            tipo_contrato="CLT",
            modalidade="Híbrido",
            descricao="Vaga para engenheiro de software com forte experiência em sistemas distribuídos.",
        ),
    ]


@pytest.mark.parametrize("vaga_de_emprego", make_vagas_de_emprego())
def test_createVagaDeEmprego(vaga_de_emprego, add_empresa, db):
    result = VagaDeEmpregoRepository.createVagaDeEmprego(vaga_de_emprego, db)

    assert result.id_vaga_de_emprego is not None
    assert result.nome_vaga_de_emprego == vaga_de_emprego.nome_vaga_de_emprego

    vaga_de_emprego_db = (
        db.query(VagaDeEmprego).filter_by(id_empresa=add_empresa.id_empresa).all()
    )
    assert len(vaga_de_emprego_db) == 1
    assert (
        vaga_de_emprego_db[0].nome_vaga_de_emprego
        == vaga_de_emprego.nome_vaga_de_emprego
    )


@pytest.mark.parametrize("vaga_de_emprego", make_vagas_de_emprego())
def test_getVagaDeEmpregoById(add_empresa, vaga_de_emprego, db):
    created_vaga_de_emprego = VagaDeEmpregoRepository.createVagaDeEmprego(
        vaga_de_emprego, db
    )
    result = VagaDeEmpregoRepository.getVagaDeEmpregoById(
        created_vaga_de_emprego.id_vaga_de_emprego, db
    )
    assert result.id_empresa == add_empresa.id_empresa
    assert result.data == vaga_de_emprego.data


def test_nonExistentCandidato_getVagaDeEmpregoByCandidatoId(db):
    result = VagaDeEmpregoRepository.getVagaDeEmpregoById(-1, db)
    assert result == None


""" @pytest.mark.parametrize(
    "novo_valor", 
    ["0.00", "100000.00", "999999999.9"]
)
def test_updateVagaDeEmpregoById(add_empresa, novo_valor, sample_vaga_de_emprego, db):
    VagaDeEmpregoRepository.createVagaDeEmprego(sample_vaga_de_emprego, db)
    sample_vaga_de_emprego.salario = Decimal(novo_valor)
    result = VagaDeEmpregoRepository.updateVagaDeEmprego(sample_vaga_de_emprego, db)
    assert result.salario == Decimal(novo_valor) """


@pytest.mark.parametrize("vaga_de_emprego", make_vagas_de_emprego())
def test_deleteVagaDeEmprego(add_empresa, vaga_de_emprego, db):
    VagaDeEmpregoRepository.createVagaDeEmprego(vaga_de_emprego, db)
    result = VagaDeEmpregoRepository.deleteVagaDeEmprego(vaga_de_emprego, db)
    assert result == True
    assert db.query(VagaDeEmprego).count() == 0


@pytest.mark.parametrize("vaga_de_emprego", make_vagas_de_emprego())
def test_nonExistentVagaDeEmprego_deleteVagaDeEmprego(add_empresa, vaga_de_emprego, db):
    with pytest.raises(Exception):
        VagaDeEmpregoRepository.deleteVagaDeEmprego(vaga_de_emprego, db)
