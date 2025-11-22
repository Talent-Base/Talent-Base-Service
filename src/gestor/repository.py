from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import Gestor


class GestorRepository:
    def getAllGestores(database: Session = Depends(getDatabase)):
        gestores = database.query(Gestor).all()
        return gestores

    def getGestorById(id_gestor: int, database: Session = Depends(getDatabase)):
        gestor = database.query(Gestor).filter(Gestor.id_gestor == id_gestor).first()
        return gestor

    def getGestoresByEmpresaId(
        id_empresa: int, database: Session = Depends(getDatabase)
    ):
        gestores = database.query(Gestor).filter(Gestor.id_empresa == id_empresa).all()
        return gestores

    def gestorExistsByEmail(
        email_gestor: int, database: Session = Depends(getDatabase)
    ):
        gestor = database.query(Gestor).filter(Gestor.email == email_gestor).first()
        if gestor:
            return True
        else:
            return False

    def createGestor(new_gestor: Gestor, database: Session = Depends(getDatabase)):
        database.add(new_gestor)
        database.commit()
        database.refresh(new_gestor)
        return new_gestor

    def updateGestor(gestor: Gestor, database: Session):
        database.merge(gestor)
        database.commit()
        return gestor

    def deleteGestor(gestor: Gestor, database: Session = Depends(getDatabase)):
        database.delete(gestor)
        database.commit()
        return True
