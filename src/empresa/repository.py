from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import Candidatura, Empresa, VagaDeEmprego


class EmpresaRepository:
	def getAllEmpresas(database: Session = Depends(getDatabase)):
		return database.query(Empresa).all()

	def getEmpresaById(id_empresa: int, database: Session = Depends(getDatabase)):
		empresa = (
			database.query(Empresa).filter(Empresa.id_empresa == id_empresa).first()
		)
		return empresa

	def getStatisticsByEmpresaId(
		id_empresa: int, database: Session = Depends(getDatabase)
	):
		vagas_totais = (
			database.query(VagaDeEmprego)
			.filter(VagaDeEmprego.id_empresa == id_empresa)
			.count()
		)
		candidatos_totais = (
			database.query(Candidatura)
			.join(
				VagaDeEmprego,
				Candidatura.id_vaga_de_emprego == VagaDeEmprego.id_vaga_de_emprego,
			)
			.filter(VagaDeEmprego.id_empresa == id_empresa)
			.count()
		)
		candidaturas_pendentes = (
			database.query(Candidatura)
			.join(
				VagaDeEmprego,
				Candidatura.id_vaga_de_emprego == VagaDeEmprego.id_vaga_de_emprego,
			)
			.filter(
				VagaDeEmprego.id_empresa == id_empresa, Candidatura.status == 'Pendente'
			)
			.count()
		)

		return {
			'vagas_totais': vagas_totais,
			'candidatos_totais': candidatos_totais,
			'candidaturas_pendentes': candidaturas_pendentes,
		}

	def empresaAlredyExists(
		cnpj: str, nome_empresa: str, database: Session = Depends(getDatabase)
	):
		empresa = (
			database.query(Empresa)
			.filter(Empresa.cnpj == cnpj and Empresa.nome_empresa == nome_empresa)
			.first()
		)
		if empresa:
			return True
		else:
			return False

	def createEmpresa(new_empresa: Empresa, database: Session = Depends(getDatabase)):
		database.add(new_empresa)
		database.commit()
		database.refresh(new_empresa)
		return new_empresa

	def updateEmpresa(empresa: Empresa, database: Session = Depends(getDatabase)):
		database.merge(empresa)
		database.commit()
		return empresa

	def deleteEmpresa(empresa: Empresa, database: Session = Depends(getDatabase)):
		database.delete(empresa)
		database.commit()
		return True
