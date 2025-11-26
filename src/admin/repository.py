from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from ..database import getDatabase
from ..models import Candidato, Usuario, Empresa, VagaDeEmprego, Candidatura
from .schema import StatsBase


class AdminRepository:
    def getStatistics(database: Session = Depends(getDatabase)):
        usuarios_totais = database.query(Usuario).count()
        candidatos_totais = database.query(Candidato).count()
        empresas_totais = database.query(Empresa).count()
        vagas_totais = database.query(VagaDeEmprego).count()
        candidaturas_totais = database.query(Candidatura).count()

        return {
            "usuarios_totais": usuarios_totais,
            "candidatos_totais": candidatos_totais,
            "empresas_totais": empresas_totais,
            "vagas_totais": vagas_totais,
            "candidaturas_totais": candidaturas_totais,
        }

    def toggleUserStatus(
        new_status: bool, usuario: Usuario, database: Session = Depends(getDatabase)
    ):
        usuario.ativo = new_status
        database.commit()
        database.refresh(usuario)
        return True
