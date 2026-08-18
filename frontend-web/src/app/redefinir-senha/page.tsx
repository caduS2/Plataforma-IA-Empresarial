"use client";

import Link from "next/link";
import { FormEvent, Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";

import { AuthShell } from "@/components/auth-shell";
import { Button } from "@/components/ui";
import { api } from "@/lib/api";

function ResetForm(){const params=useSearchParams();const token=params.get("token")??"";const[senha,setSenha]=useState("");const[confirmacao,setConfirmacao]=useState("");const[message,setMessage]=useState("");async function submit(e:FormEvent){e.preventDefault();if(senha!==confirmacao){setMessage("As senhas precisam ser iguais.");return}try{const data=await api<{mensagem:string}>("/senha/confirmar-redefinicao",{method:"POST",body:JSON.stringify({token,nova_senha:senha})});setMessage(data.mensagem)}catch(error){setMessage(error instanceof Error?error.message:"Link inválido ou expirado.")}}if(!token)return <p className="form-error">Link inválido. <Link href="/esqueci-minha-senha">Solicite outro link.</Link></p>;return <form className="form-stack" onSubmit={submit}><label>Nova senha<input type="password" minLength={12} maxLength={128} value={senha} onChange={(e)=>setSenha(e.target.value)} required/></label><label>Confirmar nova senha<input type="password" minLength={12} maxLength={128} value={confirmacao} onChange={(e)=>setConfirmacao(e.target.value)} required/></label><small className="muted">Use pelo menos 12 caracteres.</small>{message&&<p className="form-message">{message}</p>}<Button className="primary">Salvar nova senha</Button><Link className="back-link" href="/login">Voltar para entrar</Link></form>}

export default function ResetPasswordPage(){return <AuthShell eyebrow="NOVA SENHA" title="Proteja sua conta" description="Escolha uma senha longa e exclusiva para a Núcleo AI."><Suspense fallback={<p>Carregando...</p>}><ResetForm/></Suspense></AuthShell>}
