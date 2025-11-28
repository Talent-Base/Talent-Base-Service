from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import Usuario


class UsuarioRepository:
	def getAllUsuarios(database: Session = Depends(getDatabase)):
		return database.query(Usuario).all()

	def getUsuarioById(id_usuario: int, database: Session = Depends(getDatabase)):
		usuario = database.query(Usuario).filter(Usuario.id == id_usuario).first()
		return usuario

	def getUsuarioByEmail(email_usuario: int, database: Session = Depends(getDatabase)):
		usuario = database.query(Usuario).filter(Usuario.email == email_usuario).first()
		return usuario

	def usuarioExistsByEmail(email: str, database: Session = Depends(getDatabase)):
		usuario = database.query(Usuario).filter(Usuario.email == email).first()
		if usuario:
			return True
		else:
			return False

	def createUsuario(new_usuario: Usuario, database: Session = Depends(getDatabase)):
		database.add(new_usuario)
		database.commit()
		database.refresh(new_usuario)
		return new_usuario

	def updateUsuario(usuario_data: Usuario, database: Session = Depends(getDatabase)):
		database.merge(usuario_data)
		database.commit()
		return usuario_data

	def deleteUsuario(usuario: Usuario, database: Session = Depends(getDatabase)):
		database.delete(usuario)
		database.commit()
		return True
