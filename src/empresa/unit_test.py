import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from ..models import Empresa
from .repository import EmpresaRepository


def make_empresas():
	return [
		Empresa(
			nome_empresa='Empresa G',
			cnpj='12345671234567',
			cidade='Gama',
			estado='DF',
			descricao='A Gama Company',
		),
		Empresa(
			nome_empresa='Empresa 14',
			cnpj='14145671434514',
			cidade='São Paulo',
			estado='SP',
			descricao='7 plus 7 is 14',
		),
		Empresa(
			nome_empresa='Empresa 81',
			cnpj='12811281128103',
			cidade='Rio de Janeiro',
			estado='RJ',
			descricao="Rio's Best",
		),
	]


@pytest.fixture
def sample_empresa():
	return Empresa(
		nome_empresa='Empresa G',
		cnpj='12345671234567',
		cidade='Gama',
		estado='DF',
		descricao='A Gama Company',
	)


@pytest.mark.parametrize('empresa', make_empresas())
def test_createEmpresa(empresa, db):
	result = EmpresaRepository.createEmpresa(empresa, db)

	assert result.id_empresa is not None
	assert result.nome_empresa == empresa.nome_empresa
	assert db.query(Empresa).count() == 1


@pytest.mark.parametrize('empresa', make_empresas())
def test_empresaExistsByCnpj(empresa, db):
	EmpresaRepository.createEmpresa(empresa, db)
	result = EmpresaRepository.empresaAlredyExists(
		empresa.cnpj, empresa.nome_empresa, db
	)

	assert result
	assert db.query(Empresa).count() == 1


@pytest.mark.parametrize('empresa', make_empresas())
def test_nonExistentEmpresa_empresaExistsByCnpj(empresa, db):
	result = EmpresaRepository.empresaAlredyExists(
		empresa.cnpj, empresa.nome_empresa, db
	)

	assert not result
	assert db.query(Empresa).count() == 0


@pytest.mark.parametrize('empresa', make_empresas())
def test_getEmpresaById(empresa, db):
	created_empresa = EmpresaRepository.createEmpresa(empresa, db)
	id_created_user = created_empresa.id_empresa
	result = EmpresaRepository.getEmpresaById(id_created_user, db)

	assert result.nome_empresa == empresa.nome_empresa


def test_nonExistentEmpresa_getEmpresaById(db):
	result = EmpresaRepository.getEmpresaById(1, db)

	assert result is None


@pytest.mark.parametrize(
	'nova_descricao', ['Nova descrição 1', 'Nova descrição 2', 'Nova descrição 3']
)
def test_updateEmpresa(sample_empresa, nova_descricao, db):
	EmpresaRepository.createEmpresa(sample_empresa, db)
	sample_empresa.descricao = nova_descricao
	result = EmpresaRepository.updateEmpresa(sample_empresa, db)

	assert result.nome_empresa == sample_empresa.nome_empresa
	assert result.descricao == nova_descricao


@pytest.mark.parametrize('empresa', make_empresas())
def test_deleteEmpresa(empresa, db):
	EmpresaRepository.createEmpresa(empresa, db)
	result = EmpresaRepository.deleteEmpresa(empresa, db)

	assert result
	assert db.query(Empresa).count() == 0


@pytest.mark.parametrize('empresa', make_empresas())
def test_nonExistentEmpresa_deleteEmpresa(empresa, db):
	with pytest.raises(Exception):
		EmpresaRepository.deleteEmpresa(empresa, db)
