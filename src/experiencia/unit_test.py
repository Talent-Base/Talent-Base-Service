import sys
from pathlib import Path
import pytest
from sqlalchemy.exc import IntegrityError


sys.path.append(str(Path(__file__).resolve().parents[1]))

from ..models import Experiencia, Candidato, Usuario
from .repository import ExperienciaRepository
from ..candidato.repository import CandidatoRepository
from ..usuario.repository import UsuarioRepository


# import pytest


@pytest.fixture
def add_candidato(db):
	usuario = Usuario(
		nome='João Silva',
		email='joao_silva@example.com',
		senha='hashed_password',
		papel='candidato',
		ativo=True,
	)
	usuario = UsuarioRepository.createUsuario(usuario, db)

	candidato = Candidato(
		id_candidato=usuario.id,
		nome='João Silva',
		email='joao@example.com',
		estado='SP',
		cidade='São Paulo',
		resumo='Experiência em FastAPI',
		situacao_empregaticia='Desempregado',
	)
	return CandidatoRepository.createCandidato(candidato, db)


@pytest.fixture
def sample_experiencia(add_candidato):
	return Experiencia(
		id_candidato=add_candidato.id_candidato,
		nome_instituicao='TechCorp',
		cargo='Desenvolvedor Backend',
		periodo_experiencia='Jan 2020 - Dez 2022',
		descricao='Desenvolvimento de APIs com FastAPI e PostgreSQL',
		nome_curso=None,
		grau_obtido=None,
	)


def make_experiencias(valid: bool = True):
	id_val = 1 if valid else -1
	return [
		Experiencia(
			id_candidato=id_val,
			nome_instituicao='Empresa X',
			cargo='Desenvolvedor Backend',
			periodo_experiencia='Jan 2020 - Dez 2022',
			descricao='APIs RESTful com FastAPI.',
		),
		Experiencia(
			id_candidato=id_val,
			nome_instituicao='Empresa Y',
			cargo='Desenvolvedora Backend',
			periodo_experiencia='Jan 2020 - Dez 2022',
		),
		Experiencia(
			id_candidato=id_val,
			nome_instituicao='Faculdade Z',
			cargo='Estudante',
			periodo_experiencia='Jan 2020 - Dez 2022',
			descricao='Análise de dados.',
			nome_curso='Engenharia de Dados',
			grau_obtido='Graduação',
		),
	]


@pytest.mark.parametrize('experiencia', make_experiencias())
def test_createExperiencia(add_candidato, experiencia, db):
	experiencia.id_candidato = add_candidato.id_candidato

	result = ExperienciaRepository.createExperiencia(experiencia, db)

	assert result.id_experiencia is not None
	assert result.id_candidato == add_candidato.id_candidato
	assert result.nome_instituicao == experiencia.nome_instituicao

	experiencias_db = (
		db.query(Experiencia).filter_by(id_candidato=add_candidato.id_candidato).all()
	)
	assert len(experiencias_db) == 1


@pytest.mark.parametrize('experiencia', make_experiencias(valid=False))
def test_nonExistentCandidato_createExperiencia(experiencia, db):
	with pytest.raises(IntegrityError):
		ExperienciaRepository.createExperiencia(experiencia, db)
	db.rollback()


@pytest.mark.parametrize('experiencia', make_experiencias())
def test_getExperienciaByCandidatoId(add_candidato, experiencia, db):
	experiencia.id_candidato = add_candidato.id_candidato
	ExperienciaRepository.createExperiencia(experiencia, db)

	result = ExperienciaRepository.getExperienciasByCandidatoId(
		add_candidato.id_candidato, db
	)

	assert len(result) == 1
	assert result[0].nome_instituicao == experiencia.nome_instituicao


def test_nonExistentCandidato_getExperienciaByCandidatoId(db):
	result = ExperienciaRepository.getExperienciasByCandidatoId(-1, db)
	assert len(result) == 0


@pytest.mark.parametrize('nova_instituicao', ['Inst A', 'Inst B', 'Inst C'])
def test_updateExperienciaById(add_candidato, nova_instituicao, sample_experiencia, db):
	ExperienciaRepository.createExperiencia(sample_experiencia, db)

	sample_experiencia.nome_instituicao = nova_instituicao
	result = ExperienciaRepository.updateExperiencia(sample_experiencia, db)

	assert result.nome_instituicao == nova_instituicao


@pytest.mark.parametrize('experiencia', make_experiencias())
def test_deleteExperiencia(add_candidato, experiencia, db):
	experiencia.id_candidato = add_candidato.id_candidato
	created = ExperienciaRepository.createExperiencia(experiencia, db)

	result = ExperienciaRepository.deleteExperiencia(created, db)

	assert result is True
	assert db.query(Experiencia).count() == 0


@pytest.mark.parametrize('experiencia', make_experiencias())
def test_nonExistentExperiencia_deleteExperiencia(add_candidato, experiencia, db):
	experiencia.id_experiencia = -1  # força inexistência
	with pytest.raises(Exception):
		ExperienciaRepository.deleteExperiencia(experiencia, db)


