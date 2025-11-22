from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import Notificacao

class NotificacaoRepository:

    def getAllNotificacaos(database: Session = Depends(getDatabase)):
        notificacoes = database.query(Notificacao).all()
        return notificacoes

    def getNotificacaoById(id_notificacao: int, database: Session = Depends(getDatabase)):
            notificacao = database.query(Notificacao).filter(Notificacao.id_notificacao == id_notificacao).first()
            return notificacao
    
    def getNotificacoesByCandidatoId(id_candidadto: int, database: Session = Depends(getDatabase)):
        notificacoes = database.query(Notificacao).filter(Notificacao.id_candidato == id_candidadto).all()
        return notificacoes

    def createNotificacao(notificacao: Notificacao, database: Session = Depends(getDatabase)):
        database.add(notificacao)
        database.commit()
        database.refresh(notificacao)
        return notificacao
    
    def deleteNotificacao(notificacao: Notificacao, database : Session = Depends(getDatabase)):
        database.delete(notificacao)
        database.commit()
        return True
    
    def updateNotificacao(notificacao_data: Notificacao, database: Session):
        database.merge(notificacao_data)
        database.commit()
        return notificacao_data