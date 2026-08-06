from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.usuario import Usuario
from app.routers.assistente import perguntar
from app.schemas.assistente import PerguntaAssistente
from app.schemas.automacao import AutomacaoGerada, GerarAutomacao
from app.security import get_current_user


router = APIRouter(prefix="/automacoes", tags=["Automacoes"])
INSTRUCOES = {
    "email": "Crie um e-mail comercial objetivo, com assunto e corpo, usando somente fontes internas.",
    "followup": "Crie um follow-up comercial curto, com proximo passo claro, usando somente fontes internas.",
    "proposta": "Crie uma proposta comercial estruturada, indicando onde faltam dados, usando somente fontes internas.",
}


@router.post("/gerar", response_model=AutomacaoGerada)
def gerar_automacao(
    dados: GerarAutomacao,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AutomacaoGerada:
    resposta = perguntar(PerguntaAssistente(pergunta=f"{INSTRUCOES[dados.tipo]}\n\nContexto: {dados.contexto}"), usuario, db)
    return AutomacaoGerada(tipo=dados.tipo, conteudo=resposta.resposta, fontes=resposta.fontes, modo=resposta.modo)
