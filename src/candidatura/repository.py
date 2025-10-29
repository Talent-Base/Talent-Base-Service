from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import Candidatura

class CandidaturaRepository:

    def getAllCandidaturas(database: Session = Depends(getDatabase)):
        return database.query(Candidatura).all()

    def getCandidaturaById(id_candidatura: int, database: Session = Depends(getDatabase)):
        candidatura = database.query(Candidatura).filter(Candidatura.id_candidatura == id_candidatura).first()
        if candidatura:
            return candidatura
        else:
            raise HTTPException(
                status_code=404,
                detail="Candidatura not found"
            )
        
    def candidaturaExists(id_candidato: int, id_vaga_de_emprego: int, database: Session = Depends(getDatabase)):
        candidatura = database.query(Candidatura).filter(Candidatura.id_candidato == id_candidato, Candidatura.id_vaga_de_emprego == id_vaga_de_emprego).first()
        if candidatura:
            return True
        else:
            return False

    def createCandidatura(new_candidatura: Candidatura, database: Session = Depends(getDatabase)):
        database.add(new_candidatura)
        database.commit()
        database.refresh(new_candidatura)
        return new_candidatura
    
    def updateCandidatura(candidatura: Candidatura, database: Session):
        database.merge(candidatura)
        database.commit()
        return candidatura
        

    def deleteCandidatura(candidatura: Candidatura, database: Session = Depends(getDatabase)):
        database.delete(candidatura)
        database.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)