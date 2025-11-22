from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import Candidatura


class CandidaturaRepository:
    def getAllCandidaturas(database: Session = Depends(getDatabase)):
        return database.query(Candidatura).all()

    def getCandidaturaById(
        id_candidatura: int, database: Session = Depends(getDatabase)
    ):
        candidatura = (
            database.query(Candidatura)
            .filter(Candidatura.id_candidatura == id_candidatura)
            .first()
        )
        return candidatura

    def getCandidaturasByCandidatoId(
        id_candidato: int, database: Session = Depends(getDatabase)
    ):
        candidaturas = (
            database.query(Candidatura)
            .filter(Candidatura.id_candidato == id_candidato)
            .all()
        )
        return candidaturas

    def getCandidaturasByVagaDeEmpregoId(
        id_vaga_de_emprego: int, database: Session = Depends(getDatabase)
    ):
        candidaturas = (
            database.query(Candidatura)
            .filter(Candidatura.id_vaga_de_emprego == id_vaga_de_emprego)
            .all()
        )
        return candidaturas

    def candidaturaExists(
        id_candidato: int,
        id_vaga_de_emprego: int,
        database: Session = Depends(getDatabase),
    ):
        candidatura = (
            database.query(Candidatura)
            .filter(
                Candidatura.id_candidato == id_candidato,
                Candidatura.id_vaga_de_emprego == id_vaga_de_emprego,
            )
            .first()
        )
        if candidatura:
            return True
        else:
            return False

    def createCandidatura(
        new_candidatura: Candidatura, database: Session = Depends(getDatabase)
    ):
        database.add(new_candidatura)
        database.commit()
        database.refresh(new_candidatura)
        return new_candidatura

    def updateCandidatura(candidatura: Candidatura, database: Session):
        database.merge(candidatura)
        database.commit()
        return candidatura

    def deleteCandidatura(
        candidatura: Candidatura, database: Session = Depends(getDatabase)
    ):
        database.delete(candidatura)
        database.commit()
        return True
