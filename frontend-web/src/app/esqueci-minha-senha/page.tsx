"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { ArrowLeft, Mail } from "lucide-react";

import { AuthShell } from "@/components/auth-shell";
import { Button, Spinner } from "@/components/ui";
import { api } from "@/lib/api";

export default function ForgotPasswordPage() {
  const [email,setEmail]=useState(""); const [message,setMessage]=useState(""); const [loading,setLoading]=useState(false);
  async function submit(event:FormEvent<HTMLFormElement>){event.preventDefault();setLoading(true);setMessage("");try{const data=await api<{mensagem:string}>("/senha/solicitar-redefinicao",{method:"POST",body:JSON.stringify({email})});setMessage(data.mensagem);}catch(error){setMessage(error instanceof Error?error.message:"Não foi possível enviar.");}finally{setLoading(false)}}
  return <AuthShell eyebrow="RECUPERAÇÃO DE ACESSO" title="Redefina sua senha" description="Se a conta existir, enviaremos um link seguro e temporário."><form className="form-stack" onSubmit={submit}><label>E-mail profissional<div className="input-wrap"><Mail size={17}/><input type="email" value={email} onChange={(e)=>setEmail(e.target.value)} required/></div></label>{message&&<p className="form-message" role="status">{message}</p>}<Button className="primary" disabled={loading}>{loading?<><Spinner/>Enviando...</>:"Enviar instruções"}</Button><Link className="back-link" href="/login"><ArrowLeft size={15}/>Voltar para entrar</Link></form></AuthShell>;
}
