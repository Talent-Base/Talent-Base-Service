from fastapi import FastAPI

from .user.router import router as user_router
from .candidato.router import router as candidato_router
from .experiencia.router import router as experiencia_router
from .empresa.router import router as empresa_router

app = FastAPI()

app.include_router(user_router)
app.include_router(candidato_router)
app.include_router(experiencia_router)
app.include_router(empresa_router)

@app.get("/")
async def root():
    return {"message":"Hello there!"}