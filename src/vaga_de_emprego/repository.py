from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import VagaDeEmprego


class VagaDeEmpregoRepository:
    def getAllVagasDeEmprego(database: Session = Depends(getDatabase)):
        return database.query(VagaDeEmprego).all()

    def getVagaDeEmpregoById(
        id_vaga_de_emprego: int, database: Session = Depends(getDatabase)
    ):
        vaga_de_emprego = (
            database.query(VagaDeEmprego)
            .filter(id_vaga_de_emprego == id_vaga_de_emprego)
            .first()
        )
        return vaga_de_emprego

    def getVagaDeEmpregoByEmpresaId(
        id_empresa: int, database: Session = Depends(getDatabase)
    ):
        vaga_de_emprego = (
            database.query(VagaDeEmprego).filter(id_empresa == id_empresa).all()
        )
        return vaga_de_emprego

    def createVagaDeEmprego(
        new_vaga_de_emprego: VagaDeEmprego, database: Session = Depends(getDatabase)
    ):
        database.add(new_vaga_de_emprego)
        database.commit()
        return new_vaga_de_emprego

    def deleteVagaDeEmprego(
        vaga_de_emprego: VagaDeEmprego, database: Session = Depends(getDatabase)
    ):
        database.delete(vaga_de_emprego)
        database.commit()
        return True

    def updateVagaDeEmprego(
        vaga_de_emprego: VagaDeEmprego, database: Session = Depends(getDatabase)
    ):
        database.merge(vaga_de_emprego)
        database.commit()
        return vaga_de_emprego
