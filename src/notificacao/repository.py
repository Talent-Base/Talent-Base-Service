from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import Notificacao

class NotificacaoRepository:

    def getAllNotificacaos(database: Session = Depends(getDatabase)):
        notificacoes = database.query(Notificacao).all()
        return notificacoes

    def getNotificacaoById(id_notificacao: int, database: Session = Depends(getDatabase)):
            notificacao = database.query(Notificacao).filter(Notificacao.id_notificacao == id_notificacao).first()
            if not notificacao:
                raise HTTPException(
                    status_code=404,
                    detail="Notificacao not found"
                )
            return notificacao
    
    def createNotificacao(notificacao_data: Notificacao, database: Session = Depends(getDatabase)):
        new_notificacao = notificacao_data
        database.add(new_notificacao)
        database.commit()
        database.refresh(new_notificacao)
        return new_notificacao
    
    def deleteNotificacao(notificacao: Notificacao, database : Session = Depends(getDatabase)):
        database.delete(notificacao)
        database.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    
    def updateNotificacao(notificacao_data: Notificacao, database: Session):
        database.merge(notificacao_data)
        database.commit()
        return notificacao_data