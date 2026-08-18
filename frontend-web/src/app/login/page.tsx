"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, LockKeyhole, Mail } from "lucide-react";

import { AuthShell } from "@/components/auth-shell";
import { Button, Spinner } from "@/components/ui";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  async function entrar(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setErro(""); setLoading(true);
    try {
      const response = await fetch("/api/auth/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, senha }) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail ?? "E-mail ou senha inválidos.");
      router.replace("/dashboard"); router.refresh();
    } catch (error) { setErro(error instanceof Error ? error.message : "Erro inesperado."); }
    finally { setLoading(false); }
  }

  return <AuthShell eyebrow="ACESSO SEGURO" title="Bem-vindo de volta" description="Entre com a conta criada pelo administrador da sua empresa."><form className="form-stack" onSubmit={entrar}><label>E-mail profissional<div className="input-wrap"><Mail size={17}/><input aria-label="E-mail profissional" type="email" autoComplete="email" value={email} onChange={(event)=>setEmail(event.target.value)} placeholder="voce@empresa.com" required/></div></label><label><span className="label-row">Senha <Link href="/esqueci-minha-senha">Esqueci minha senha</Link></span><div className="input-wrap"><LockKeyhole size={17}/><input aria-label="Senha" type="password" autoComplete="current-password" minLength={8} value={senha} onChange={(event)=>setSenha(event.target.value)} required/></div></label>{erro && <p className="form-error" role="alert">{erro}</p>}<Button className="primary" disabled={loading} type="submit">{loading ? <><Spinner/>Entrando...</> : <>Entrar na plataforma <ArrowRight size={17}/></>}</Button></form><p className="auth-help">Precisa de acesso? Solicite um convite ao administrador da sua empresa.</p></AuthShell>;
}
