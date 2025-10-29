from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import Candidato, Experiencia

class CandidatoRepository:

    def getAllCandidatos(database: Session = Depends(getDatabase)):
        candidatos = database.query(Candidato).all()
        return candidatos 

    def getCandidatoById(id_candidato: int, database: Session = Depends(getDatabase)):
        candidato = database.query(Candidato).filter(Candidato.id_usuario == id_candidato).first()
        return candidato
        
    def candidatoExistsByEmail(email_candidato: int, database: Session = Depends(getDatabase)):
        candidato = database.query(Candidato).filter(Candidato.email == email_candidato).first()
        if candidato:
            return True
        else:
            return False

    def createCandidato(new_candidato: Candidato, database: Session = Depends(getDatabase)):
        database.add(new_candidato)
        database.commit()
        database.refresh(new_candidato)
        return new_candidato

    """ def createCandidato(new_Candidato: Candidato, database: Session = Depends(getDatabase)):
        candidato_already_exists = database.query(Candidato).filter(Candidato.email == new_Candidato.email).first()
        if candidato_already_exists:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        database.add(new_Candidato)
        database.commit()
        database.refresh(new_Candidato)
        return new_Candidato """
    
    def updateCandidato(candidato: Candidato, database: Session):
        database.merge(candidato)
        database.commit()
        return candidato

    def old_updateCandidatoById(id_candidato: int, candidato_data: Candidato, database: Session):

        candidato = database.query(Candidato).filter(Candidato.id_usuario == id_candidato).first()
        if not candidato:
            raise HTTPException(status_code=404, detail="Candidato not found")

        database.merge(candidato_data)
        database.commit()
        return candidato
        

    def deleteCandidato(candidato: Candidato, database: Session = Depends(getDatabase)):
        database.delete(candidato)
        database.commit()
        return True
        #return Response(status_code = status.HTTP_204_NO_CONTENT)

    def old_deleteCandidato(id_candidato: int, database: Session = Depends(getDatabase)):
        
        candidato = database.query(Candidato).filter(Candidato.id_usuario == id_candidato).first()
        if candidato:
            database.delete(candidato)
            database.commit()
        else:
            raise HTTPException(
                status_code=404,
                detail="Candidato not found"
            )
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    
    def getExperienciasByCandidatoId(id_candidato: int, database: Session = Depends(getDatabase)):
        candidato = database.query(Candidato).filter(Candidato.id_usuario == id_candidato).first()
        if not candidato:
            raise HTTPException(
                status_code=404,
                detail="Candidato not found"
            )
        experiencias = database.query(Experiencia).filter(Experiencia.id_usuario == id_candidato).first
        return experiencias
    
    def createExperienciaByCandidatoId(id_candidato: int, experiencia_data: Experiencia, database: Session = Depends(getDatabase)):
        new_experiencia = experiencia_data
        database.add(new_experiencia)
        database.commit()
        database.refresh(new_experiencia)
        return new_experiencia  