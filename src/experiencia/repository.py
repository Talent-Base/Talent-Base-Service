from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import Experiencia


class ExperienciaRepository:
	def getExperienciasByCandidatoId(
		id_candidato: int, database: Session = Depends(getDatabase)
	):
		experiencias = (
			database.query(Experiencia)
			.filter(Experiencia.id_candidato == id_candidato)
			.all()
		)
		return experiencias

	def getExperienciaById(
		id_experiencia: int, database: Session = Depends(getDatabase)
	):
		experiencia = (
			database.query(Experiencia)
			.filter(Experiencia.id_experiencia == id_experiencia)
			.first()
		)
		return experiencia

	def createExperiencia(
		experiencia_data: Experiencia, database: Session = Depends(getDatabase)
	):
		new_experiencia = experiencia_data
		database.add(new_experiencia)
		database.commit()
		database.refresh(new_experiencia)
		return new_experiencia

	def deleteExperiencia(
		experiencia: Experiencia, database: Session = Depends(getDatabase)
	):
		database.delete(experiencia)
		database.commit()
		return True

	def updateExperiencia(experiencia_data: Experiencia, database: Session):
		database.merge(experiencia_data)
		database.commit()
		return experiencia_data
