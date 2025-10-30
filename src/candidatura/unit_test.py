from datetime import date
from decimal import Decimal
from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1])) 

from ..database import Base
from ..models import Candidatura, VagaDeEmprego, Candidato, Empresa
from .repository import CandidaturaRepository
from ..candidato.repository import CandidatoRepository
from ..empresa.repository import EmpresaRepository
from ..vaga_de_emprego.repository import VagaDeEmpregoRepository

@pytest.fixture
def add_candidato(db):
    sample = Candidato(
        id_usuario=1,
        nome="João Silva",
        email="joao@example.com",
        estado="SP",
        cidade="São Paulo",
        resumo="Experiência em FastAPI",
        situacao_empregaticia="Desempregado",
    )
    return CandidatoRepository.createCandidato(sample, db)

@pytest.fixture
def add_empresa(db):
    sample = Empresa(
        id_empresa = 1,
        nome_empresa = "Empresa G",
        cnpj = "12345671234567",
        cidade = "Gama",
        estado = "DF",
        descricao = "A Gama Company"
    )
    return EmpresaRepository.createEmpresa(sample, db)

@pytest.fixture
def add_vaga_de_emprego(add_empresa, db):
    sample = VagaDeEmprego(
        id_vaga_de_emprego = 1,
        id_empresa=add_empresa.id_empresa,
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
    return VagaDeEmpregoRepository.createVagaDeEmprego(sample, db)

@pytest.fixture
def sample_candidatura(add_candidato, add_vaga_de_emprego, db):
    sample = Candidatura(
            id_candidato = add_candidato.id_usuario,
            id_vaga_de_emprego = add_vaga_de_emprego.id_vaga_de_emprego,
            status = "Em análise",
            data = date(2025, 10, 28)
        )
    return CandidaturaRepository.createCandidatura(sample, db)

def make_candidaturas():
    return [
        Candidatura(
            id_candidato = 1,
            id_vaga_de_emprego = 1,
            status = "Em análise",
            data = date(2025, 10, 28)
        ),
    ]

@pytest.mark.parametrize("candidatura", make_candidaturas())
def test_createCandidatura(candidatura, add_candidato, add_vaga_de_emprego, db):
    candidatura.id_candidato = add_candidato.id_usuario
    candidatura.id_vaga_de_emprego = add_vaga_de_emprego.id_vaga_de_emprego
    result = CandidaturaRepository.createCandidatura(candidatura, db)
    assert result.status == candidatura.status

@pytest.mark.parametrize("candidatura", make_candidaturas())
def test_candidaturaExists(candidatura, add_candidato, add_vaga_de_emprego, db):
    CandidaturaRepository.createCandidatura(candidatura, db)
    result = CandidaturaRepository.candidaturaExists(candidatura.id_candidato, candidatura.id_vaga_de_emprego, db)
    assert result == True
    assert db.query(Candidatura).count() == 1

@pytest.mark.parametrize("candidatura", make_candidaturas())
def test_nonExistentCandidatura_candidaturaExists(candidatura, add_candidato, add_vaga_de_emprego, db):
    result = CandidaturaRepository.candidaturaExists(candidatura.id_candidato, candidatura.id_vaga_de_emprego, db)
    assert result == False
    assert db.query(Candidatura).count() == 0

@pytest.mark.parametrize("candidatura", make_candidaturas())
def test_getCandidaturaById(candidatura, add_candidato, add_vaga_de_emprego, db):
    created_candidatura = CandidaturaRepository.createCandidatura(candidatura,  db)
    result = CandidaturaRepository.getCandidaturaById(created_candidatura.id_candidatura, db)
    assert result.data == candidatura.data

def test_getCandidaturaById(db):
    result = CandidaturaRepository.getCandidaturaById(-1, db)
    assert result == None

@pytest.mark.parametrize("novo_status", ["Rejeitado", "Aprovado"])
def test_updateCandidatura(sample_candidatura, novo_status, add_candidato, add_empresa, db):
    CandidaturaRepository.createCandidatura(sample_candidatura, db)
    sample_candidatura.status = novo_status
    result = CandidaturaRepository.updateCandidatura(sample_candidatura, db)
    assert result.status == novo_status

@pytest.mark.parametrize("candidatura", make_candidaturas())
def test_deleteCandidatura(candidatura, add_candidato, add_vaga_de_emprego, db):
    CandidaturaRepository.createCandidatura(candidatura, db)
    result = CandidaturaRepository.deleteCandidatura(candidatura, db)
    assert result == True
    assert db.query(Candidatura).count() == 0

@pytest.mark.parametrize("candidatura", make_candidaturas())
def test_deleteCandidatura(candidatura, add_candidato, add_vaga_de_emprego, db):
    with pytest.raises(Exception):
        CandidaturaRepository.deleteCandidatura(candidatura, db)
    