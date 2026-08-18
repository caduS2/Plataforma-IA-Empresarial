"use client";

import Link from "next/link";
import { FormEvent, Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { UserPlus } from "lucide-react";

import { AuthShell } from "@/components/auth-shell";
import { Button, Spinner } from "@/components/ui";
import { api } from "@/lib/api";

function InviteForm() {
  const router = useRouter(); const params = useSearchParams(); const token = params.get("token") ?? "";
  const [nome,setNome]=useState(""); const [senha,setSenha]=useState(""); const [confirmacao,setConfirmacao]=useState(""); const [error,setError]=useState(""); const [loading,setLoading]=useState(false);
  async function submit(event:FormEvent){event.preventDefault();setError("");if(senha!==confirmacao){setError("As senhas precisam ser iguais.");return}setLoading(true);try{await api("/convites/aceitar",{method:"POST",body:JSON.stringify({token,nome,senha})});router.replace("/login")}catch(e){setError(e instanceof Error?e.message:"Não foi possível aceitar o convite.")}finally{setLoading(false)}}
  if(!token)return <p className="form-error">Este convite não contém um token válido. <Link href="/login">Voltar ao login</Link></p>;
  return <form className="form-stack" onSubmit={submit}><label>Seu nome<input value={nome} onChange={e=>setNome(e.target.value)} minLength={2} maxLength={150} autoComplete="name" required/></label><label>Crie uma senha<input type="password" value={senha} onChange={e=>setSenha(e.target.value)} minLength={8} maxLength={128} autoComplete="new-password" required/></label><label>Confirme a senha<input type="password" value={confirmacao} onChange={e=>setConfirmacao(e.target.value)} minLength={8} maxLength={128} autoComplete="new-password" required/></label>{error&&<p className="form-error" role="alert">{error}</p>}<Button className="primary" disabled={loading}>{loading?<Spinner/>:<UserPlus size={16}/>}Aceitar convite</Button></form>;
}

export default function AcceptInvitePage(){return <AuthShell eyebrow="CONVITE SEGURO" title="Entre para a equipe" description="Complete seu perfil para ativar o acesso ao workspace."><Suspense fallback={<p>Validando convite...</p>}><InviteForm/></Suspense></AuthShell>}
