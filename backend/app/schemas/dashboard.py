from pydantic import BaseModel


class DashboardResumo(BaseModel):
    empresas: int
    usuarios: int
    documentos: int
    documentos_indexados: int
    convites_pendentes: int
