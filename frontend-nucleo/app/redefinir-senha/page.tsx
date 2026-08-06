"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { confirmPasswordReset } from "../lib/api";

export default function RedefinirSenhaPage() {
  const parametros = useSearchParams();
  const [senha, setSenha] = useState("");
  const [confirmacao, setConfirmacao] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [enviando, setEnviando] = useState(false);
  const token = parametros.get("token") ?? "";

  async function enviar(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (senha !== confirmacao) { setMensagem("As senhas precisam ser iguais."); return; }
    setEnviando(true); setMensagem("");
    try { const resposta = await confirmPasswordReset(token, senha); setMensagem(resposta.mensagem); }
    catch { setMensagem("O link é inválido ou expirou. Solicite uma nova redefinição."); }
    finally { setEnviando(false); }
  }

  if (!token) return <main className="auth-page"><section className="auth-card"><h1>Link inválido</h1><p>Solicite uma nova redefinição de senha.</p><Link href="/esqueci-minha-senha">Solicitar redefinição</Link></section></main>;
  return <main className="auth-page"><form className="auth-card" onSubmit={enviar}><b>núcleo.ai</b><small>NOVA SENHA</small><h1>Escolha uma nova senha</h1><label>Nova senha<input type="password" value={senha} onChange={event => setSenha(event.target.value)} minLength={8} required /></label><label>Confirmar nova senha<input type="password" value={confirmacao} onChange={event => setConfirmacao(event.target.value)} minLength={8} required /></label>{mensagem && <p role="status">{mensagem}</p>}<button disabled={enviando} type="submit">{enviando ? "Salvando..." : "Salvar nova senha"}</button><Link href="/login">Voltar para entrar</Link></form></main>;
}
