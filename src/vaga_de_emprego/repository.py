from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import VagaDeEmprego

class VagaDeEmpregoepository:

    def getAllVagasDeEmprego(database: Session = Depends(getDatabase)):
        return database.query(VagaDeEmprego).all()

    def getVagaDeEmpregoById(id_vaga_de_emprego: int, database: Session = Depends(getDatabase)):
        vaga_de_emprego = database.query(VagaDeEmprego).filter(id_vaga_de_emprego = id_vaga_de_emprego).first()
        if vaga_de_emprego:
            return vaga_de_emprego
        else:
            raise HTTPException(
                status_code=404,
                detail="Vaga de emprego not found"
            )

    def createVagaDeEmprego(new_vaga_de_emprego: VagaDeEmprego, database: Session = Depends(getDatabase)):
        database.add(new_vaga_de_emprego)
        database.commit()
        return new_vaga_de_emprego

    def deleteVagaDeEmprego(vaga_de_emprego: VagaDeEmprego, database: Session = Depends(getDatabase)):
        database.delete(vaga_de_emprego)
        database.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)

    def updateVagaDeEmprego(vaga_de_emprego: VagaDeEmprego, database: Session = Depends(getDatabase)):
        database.merge(vaga_de_emprego)
        database.commit()
        return vaga_de_emprego