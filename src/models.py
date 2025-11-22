from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    Numeric,
    String,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
import enum
from .database import Base


class Papel(str, enum.Enum):
    candidato = "candidato"
    gestor = "gestor"
    admin = "admin"


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    papel = Column(Enum(Papel), nullable=False)
    disabled = Column(Boolean, default=False)

    candidato = relationship(
        "Candidato",
        back_populates="usuario",
        cascade="all, delete-orphan",
        uselist=False,
    )
    gestor = relationship(
        "Gestor", back_populates="usuario", cascade="all, delete-orphan", uselist=False
    )


class Candidato(Base):
    __tablename__ = "candidato"

    id_candidato = Column(
        Integer, ForeignKey("usuario.id"), primary_key=True, index=True
    )
    nome = Column(String(100), index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    estado = Column(String(3), nullable=True)
    cidade = Column(String(50), nullable=True)
    resumo = Column(String(500), nullable=True)
    situacao_empregaticia = Column(String(20), nullable=True)

    usuario = relationship(
        "Usuario",
        back_populates="candidato",
        cascade="all, delete-orphan",
        single_parent=True,
    )


class Experiencia(Base):
    __tablename__ = "experiencia"

    id_experiencia = Column(Integer, primary_key=True, index=True, nullable=False)
    id_usuario = Column(
        Integer, ForeignKey("candidato.id_candidato"), index=True, nullable=False
    )
    nome_instituicao = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)
    periodo_experiencia = Column(Integer, nullable=False)
    descricao = Column(String(500), nullable=True)
    nome_curso = Column(String(100), nullable=True)
    grau_obtido = Column(String(50), nullable=True)


class Empresa(Base):
    __tablename__ = "empresa"

    id_empresa = Column(Integer, primary_key=True, index=True, nullable=False)
    nome_empresa = Column(String(100), unique=True, nullable=False)
    cnpj = Column(String(20), unique=True, nullable=False)
    cidade = Column(String(50), nullable=False)
    estado = Column(String(3), nullable=False)
    descricao = Column(String(500), nullable=True)


class VagaDeEmprego(Base):
    __tablename__ = "vagaDeEmprego"

    id_vaga_de_emprego = Column(Integer, primary_key=True, index=True, nullable=False)
    id_empresa = Column(
        Integer, ForeignKey("empresa.id_empresa"), index=True, nullable=False
    )
    nome_vaga_de_emprego = Column(String(100), nullable=False)
    data = Column(Date, nullable=False)
    cidade = Column(String(50), nullable=False)
    estado = Column(String(3), nullable=False)
    salario = Column(Numeric, nullable=False)
    cargo = Column(String(50), nullable=False)
    nivel = Column(String(50), nullable=False)
    tipo_contrato = Column(String(50), nullable=False)
    modalidade = Column(String(50), nullable=False)
    descricao = Column(String(200), nullable=False)


class Candidatura(Base):
    __tablename__ = "candidatura"

    id_candidatura = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(Integer, ForeignKey("candidato.id_candidato"), index=True)
    id_vaga_de_emprego = Column(
        Integer, ForeignKey("vagaDeEmprego.id_vaga_de_emprego"), index=True
    )
    status = Column(String(50), nullable=False)
    data = Column(DateTime, nullable=False)


class Notificacao(Base):
    __tablename__ = "notificacao"

    id_notificacao = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(Integer, ForeignKey("candidato.id_candidato"), index=True)
    id_candidatura = Column(
        Integer, ForeignKey("candidatura.id_candidatura"), index=True, nullable=True
    )
    id_vaga_de_emprego = Column(
        Integer,
        ForeignKey("vagaDeEmprego.id_vaga_de_emprego"),
        index=True,
        nullable=True,
    )
    titulo = Column(String(50), nullable=False)
    mensagem = Column(String(500), nullable=False)
    visualizada = Column(Boolean, nullable=False)
    data = Column(DateTime, nullable=False)


class Gestor(Base):
    __tablename__ = "gestor"

    id_gestor = Column(
        Integer, ForeignKey("usuario.id"), primary_key=True, index=True, nullable=False
    )
    nome = Column(String(100), index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    id_empresa = Column(
        Integer, ForeignKey("empresa.id_empresa"), index=True, nullable=True
    )

    usuario = relationship(
        "Usuario",
        back_populates="gestor",
        cascade="all, delete-orphan",
        single_parent=True,
    )
