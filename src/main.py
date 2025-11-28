from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .usuario.router import router as usuario_router
from .candidato.router import router as candidato_router
from .experiencia.router import router as experiencia_router
from .empresa.router import router as empresa_router
from .gestor.router import router as gestor_router
from .vaga_de_emprego.router import router as vaga_de_emprego_router
from .candidatura.router import router as candidatura_router
from .auth.router import router as auth_router
from .admin.router import router as admin_router


app = FastAPI()

app.include_router(usuario_router)
app.include_router(candidato_router)
app.include_router(candidatura_router)
app.include_router(experiencia_router)
app.include_router(empresa_router)
app.include_router(gestor_router)
app.include_router(vaga_de_emprego_router)
app.include_router(auth_router)
app.include_router(admin_router)


app.add_middleware(
	CORSMiddleware,
	allow_origins=['http://localhost:3000'],
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)


@app.get('/')
async def root():
	return {'message': 'Hello there!'}
