"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { requestPasswordReset } from "../lib/api";

export default function EsqueciMinhaSenhaPage() {
  const [email, setEmail] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [enviando, setEnviando] = useState(false);

  async function enviar(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setEnviando(true); setMensagem("");
    try { const resposta = await requestPasswordReset(email); setMensagem(resposta.mensagem); }
    catch { setMensagem("Não foi possível concluir a solicitação agora. Tente novamente."); }
    finally { setEnviando(false); }
  }

  return <main className="auth-page"><form className="auth-card" onSubmit={enviar}><b>núcleo.ai</b><small>RECUPERAÇÃO DE ACESSO</small><h1>Redefina sua senha</h1><p>Informe seu e-mail. Se houver uma conta ativa, enviaremos as instruções.</p><label>E-mail<input type="email" value={email} onChange={event => setEmail(event.target.value)} required /></label>{mensagem && <p role="status">{mensagem}</p>}<button disabled={enviando} type="submit">{enviando ? "Enviando..." : "Enviar instruções"}</button><Link href="/login">Voltar para entrar</Link></form></main>;
}
