from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import Empresa

class EmpresaRepository:

    def getAllEmpresas(database: Session = Depends(getDatabase)):
        return database.query(Empresa).all()

    def getEmpresaById(id_empresa: int, database: Session = Depends(getDatabase)):
        empresa = database.query(Empresa).filter(Empresa.id_empresa == id_empresa).first()
        if empresa:
            return empresa
        else:
            raise HTTPException(
                status_code=404,
                detail="Empresa not found"
            )

    def empresaExistsByName(empresa_name: str, database: Session = Depends(getDatabase)):
        empresa = database.query(Empresa).filter(nome_empresa = empresa_name).first()
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
        return Response(status_code = status.HTTP_204_NO_CONTENT)