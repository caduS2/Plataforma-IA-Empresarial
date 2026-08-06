"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Company, listCompanies, login, registerUser } from "../lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [cadastro, setCadastro] = useState(false);
  const [nome, setNome] = useState("");
  const [empresas, setEmpresas] = useState<Company[]>([]);
  const [empresaId, setEmpresaId] = useState("");

  useEffect(() => { listCompanies().then(items => { setEmpresas(items); setEmpresaId(items[0]?.id ?? ""); }).catch(() => setErro("Não foi possível carregar as empresas.")); }, []);

  async function entrar(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setErro(""); setEnviando(true);
    try { if (cadastro) await registerUser({ nome, email, senha, empresa_id: empresaId }); const sessao = await login({ email, senha }); localStorage.setItem("nucleo-access-token", sessao.access_token); router.push("/dashboard"); }
    catch { setErro("Não foi possível entrar. Confira seu e-mail e senha."); }
    finally { setEnviando(false); }
  }

  return <main style={{minHeight:"100vh",display:"grid",placeItems:"center",background:"#f7f5fb"}}><form onSubmit={entrar} style={{width:"min(100% - 32px,390px)",padding:32,display:"grid",gap:14,background:"white",borderRadius:16}}><b style={{fontSize:22}}>núcleo.ai</b><small>ACESSO À PLATAFORMA</small><h1 style={{margin:0}}>{cadastro ? "Crie sua conta" : "Entre na sua conta"}</h1>{cadastro && <><label>Nome<input value={nome} onChange={e => setNome(e.target.value)} required /></label><label>Empresa<select value={empresaId} onChange={e => setEmpresaId(e.target.value)} required>{empresas.map(empresa => <option key={empresa.id} value={empresa.id}>{empresa.nome}</option>)}</select></label></>}<label>E-mail<input value={email} onChange={e => setEmail(e.target.value)} type="email" required /></label><label>Senha<input value={senha} onChange={e => setSenha(e.target.value)} type="password" minLength={8} required /></label>{erro && <p style={{color:"#bb3158",margin:0}}>{erro}</p>}<button disabled={enviando || (cadastro && !empresaId)} type="submit">{enviando ? "Aguarde..." : cadastro ? "Criar conta" : "Entrar"}</button><button type="button" onClick={()=>{setCadastro(value=>!value);setErro("");}}>{cadastro ? "Já tenho uma conta" : "Criar uma conta"}</button>{!cadastro && <Link href="/esqueci-minha-senha">Esqueci minha senha</Link>}</form></main>;
}
