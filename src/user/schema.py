from pydantic import BaseModel

class Candidato(BaseModel):
    name: str
    email: str