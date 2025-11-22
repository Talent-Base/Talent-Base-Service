from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from ..auth.repository import requireCandidato

from ..database import engine, Base, getDatabase
from .repository import CandidatoRepository
from .schema import CandidatoBase
from ..models import Candidato, Candidatura, Experiencia, Notificacao

from ..experiencia.repository import ExperienciaRepository
from ..experiencia.schema import ExperienciaBase

from ..candidatura.repository import CandidaturaRepository
from ..candidatura.schema import CandidaturaBase

from ..notificacao.repository import NotificacaoRepository
from ..notificacao.schema import NotificacaoBase

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/candidatos",
    tags=["candidatos"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def getCandidatos(database: Session = Depends(getDatabase)):
    candidatos = CandidatoRepository.getAllCandidatos(database)
    return candidatos


@router.get("/{id_candidato}")
async def getCandidatoById(id_candidato: int, database: Session = Depends(getDatabase)):
    candidato = CandidatoRepository.getCandidatoById(id_candidato, database)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return candidato


@router.post("/")
async def createCandidato(
    new_candidato: CandidatoBase, database: Session = Depends(getDatabase)
):
    candidato_already_exists = CandidatoRepository.candidatoExistsByEmail(
        new_candidato.email, database
    )
    if candidato_already_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        new_candidato = CandidatoRepository.createCandidato(
            Candidato(**new_candidato.model_dump()), database
        )
        return new_candidato


@router.put("/{id_candidato}")
async def updateCandidatoById(
    id_candidato: int,
    candidato_data: CandidatoBase,
    database: Session = Depends(getDatabase),
    current_candidato: Candidato = Depends(requireCandidato),
):
    if id_candidato != current_candidato.id:
        raise HTTPException(
            status_code=403, detail="Você não pode editar outro usuário."
        )
    candidato = CandidatoRepository.getCandidatoById(id_candidato, database)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    updated_candidato = CandidatoRepository.updateCandidato(
        Candidato(id_usuario=id_candidato, **candidato_data.model_dump()), database
    )
    return updated_candidato


@router.delete("/{id_candidato}")
async def deleteCandidato(id_candidato: int, database: Session = Depends(getDatabase)):
    candidato = CandidatoRepository.getCandidatoById(id_candidato, database)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    success = CandidatoRepository.deleteCandidato(candidato, database)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar candidato")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{id_candidato}/experiencias")
async def getCandidatosExperiencias(
    id_candidato: int, database: Session = Depends(getDatabase)
):
    experiencias = ExperienciaRepository.getExperienciasByCandidatoId(
        id_candidato, database
    )
    if not experiencias:
        raise HTTPException(status_code=404, detail="Experiências não encontradas")
    return experiencias


@router.post("/{id_candidato}/experiencias")
async def createCandidatosExperiencia(
    id_candidato: int,
    experiencia_data: ExperienciaBase,
    database: Session = Depends(getDatabase),
):
    new_experiencia = ExperienciaRepository.createExperiencia(
        Experiencia(**experiencia_data.model_dump()), database
    )
    return new_experiencia


@router.put("/{id_candidato}/experiencias/{id_experiencia}")
async def updateCandidatosExperienciaById(
    id_candidato: int, id_experiencia: int, database: Session = Depends(getDatabase)
):
    experiencia = ExperienciaRepository.getExperienciaById(id_experiencia, database)
    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia não encontrada")
    updated_experiencia = ExperienciaRepository.updateExperiencia(experiencia, database)
    return updated_experiencia


@router.delete("/{id_candidato}/experiencias/{id_experiencia}")
async def deleteCandidatosExperiencia(
    id_candidato: int, id_experiencia: int, database: Session = Depends(getDatabase)
):
    experiencia = ExperienciaRepository.getExperienciaById(id_experiencia, database)
    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia não encontrado")
    success = ExperienciaRepository.deleteExperiencia(experiencia, database)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar experiencia")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{id_candidato}/candidaturas")
async def getCandidatosCandidaturas(
    id_candidato: int, database: Session = Depends(getDatabase)
):
    candidaturas = CandidaturaRepository.getCandidaturasByCandidatoId(
        id_candidato, database
    )
    if not candidaturas:
        raise HTTPException(status_code=404, detail="Candidaturas não encontradas")
    return candidaturas


@router.post("/{id_candidato}/candidaturas")
async def createCanditadosCandidatura(
    id_candidato: int,
    candidatura_data: CandidaturaBase,
    database: Session = Depends(getDatabase),
):
    candidatura_already_exists = CandidaturaRepository.candidaturaExists(
        id_candidato, candidatura_data.id_vaga_de_emprego, database
    )
    if candidatura_already_exists:
        raise HTTPException(status_code=404, detail="Candidatura já realizada")
    candidatura = CandidaturaRepository.createCandidatura(
        Candidatura(**candidatura_data.model_dump()), database
    )
    return candidatura


@router.delete("/{id_candidato}/candidaturas/{id_candidatura}")
async def deleteCandidatoCandidatura(
    id_candidato: int, id_candidatura: int, database: Session = Depends(getDatabase)
):
    candidatura = CandidaturaRepository.getCandidaturaById(id_candidatura, database)
    if not candidatura:
        raise HTTPException(status_code=404, detail="Candidatura não encontrado")
    success = CandidaturaRepository.deleteExperiencia(candidatura, database)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao deletar candidatura")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{id_candidato}/notificacoes")
async def getCandidatosNotificacoes(
    id_candidato: int, database: Session = Depends(getDatabase)
):
    notificacoes = NotificacaoRepository.getNotificacoesByCandidatoId(
        id_candidato, database
    )
    if not notificacoes:
        raise HTTPException(status_code=404, detail="NOtificacoes não encontradas")
    return notificacoes


@router.put("/{id_candidato}/notificacoes/{id_notificacao}")
async def updateNotificacaoById(
    id_candidato: int,
    id_notificacao: int,
    notificacao_data: NotificacaoBase,
    database: Session = Depends(getDatabase),
):
    notificacao = NotificacaoRepository.getNotificacaoById(id_notificacao, database)
    if notificacao:
        updated_notificacao = NotificacaoRepository.updateNotificacao(
            Notificacao(id_usuario=id_notificacao, **notificacao_data.model_dump()),
            database,
        )
        return updated_notificacao
