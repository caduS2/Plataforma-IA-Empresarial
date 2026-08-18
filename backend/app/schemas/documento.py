from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DocumentoResponse(BaseModel):
    id: UUID
    nome_original: str
    tipo_mime: str
    tamanho_bytes: int
    status: str
    criado_em: datetime
    model_config = ConfigDict(from_attributes=True)
