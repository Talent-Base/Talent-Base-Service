from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..database import engine, Base, getDatabase
from .repository import NotificacaoRepository
from .schema import NotificacaoBase
from ..models import Notificacao

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix = "/notificacoes",
    tags = ["notificacoes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def getNotificacoes(database: Session = Depends(getDatabase)):
    notificacoes = NotificacaoRepository.getAllNotificacaos(database)
    return notificacoes

@router.get("/{id_notificacao}")
async def getNotificacaoById(id_notificacao: int, database: Session = Depends(getDatabase)):
    notificacao = NotificacaoRepository.getNotificacaoById(id_notificacao, database)
    return notificacao

@router.post("/")
async def createNotificacao(new_notificacao: NotificacaoBase, database: Session = Depends(getDatabase)):
    new_notificacao = NotificacaoRepository.createNotificacao(Notificacao(**new_notificacao.model_dump()), database)
    return new_notificacao

@router.put("/{id_notificacao}")
async def updateNotificacaoById(id_notificacao: int, notificacao_data: NotificacaoBase, database: Session = Depends(getDatabase)):
    notificacao = NotificacaoRepository.getNotificacaoById(id_notificacao, database)
    if notificacao:
        updated_notificacao = NotificacaoRepository.updateNotificacao(Notificacao(id_usuario = id_notificacao, **notificacao_data.model_dump()), database)
        return updated_notificacao

@router.delete("/{id_notificacao}")
async def deleteNotificacao(id_notificacao: int, database: Session = Depends(getDatabase)):
    notificacao = NotificacaoRepository.getNotificacaoById(id_notificacao, database)
    if notificacao:
        response = NotificacaoRepository.deleteNotificacao(notificacao, database)
        return response