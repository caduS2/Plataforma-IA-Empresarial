import Link from "next/link";
import type { ReactNode } from "react";
import { BrainCircuit, CheckCircle2, ShieldCheck, Sparkles } from "lucide-react";

export function AuthShell({ eyebrow, title, description, children }: { eyebrow: string; title: string; description: string; children: ReactNode }) {
  return <main className="auth-layout"><section className="auth-brand"><Link href="/" className="brand"><span><BrainCircuit size={22}/></span>Núcleo AI</Link><div><p className="eyebrow">INTELIGÊNCIA QUE VENDE COM EVIDÊNCIAS</p><h1>Conhecimento empresarial transformado em ação.</h1><p>Centralize documentos, equipe e automações em uma experiência segura, rápida e mensurável.</p><ul><li><ShieldCheck size={18}/>Dados isolados por empresa</li><li><Sparkles size={18}/>Respostas com fontes internas</li><li><CheckCircle2 size={18}/>Fluxos prontos para produção</li></ul></div><small>Projeto full stack autoral · Next.js + FastAPI + PostgreSQL</small></section><section className="auth-panel"><div className="auth-card"><p className="eyebrow">{eyebrow}</p><h2>{title}</h2><p className="muted">{description}</p>{children}</div></section></main>;
}
