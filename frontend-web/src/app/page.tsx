import Link from "next/link";
import { ArrowRight, BarChart3, BrainCircuit, FileText, Layers, ShieldCheck, Users } from "lucide-react";

import { SectionHero } from "@/components/originkit/ui/section-hero";
import { DemoButton } from "@/components/demo-button";

const features = [
  {
    icon: FileText,
    title: "Centralize documentos",
    description: "PDFs, planilhas e textos em um só lugar, com extração e organização automáticas por empresa.",
  },
  {
    icon: BrainCircuit,
    title: "Assistente com fontes",
    description: "Pergunte e receba respostas sustentadas por citações dos próprios documentos internos.",
  },
  {
    icon: Users,
    title: "Colaboração por convite",
    description: "Times e perfis com permissões claras, sem compartilhar senhas ou expor dados de outras empresas.",
  },
  {
    icon: BarChart3,
    title: "Decisões com dados",
    description: "Métricas, resumos e análises de mercado para embasar decisões com evidências reais.",
  },
  {
    icon: Layers,
    title: "Automações e fluxos",
    description: "Processos prontos para produção: relatórios, propostas, e-mails e brainstorm empresarial.",
  },
  {
    icon: ShieldCheck,
    title: "Segurança por design",
    description: "Isolamento multiempresa, autenticação JWT, rate limiting e uploads validados por padrão.",
  },
];

const stack = ["Next.js", "FastAPI", "PostgreSQL", "SQLAlchemy", "Alembic", "JWT", "Argon2", "TypeScript"];

export default function Home() {
  return (
    <>
      <header className="landing-nav">
        <Link href="/" className="brand">
          <span>
            <BrainCircuit size={22} />
          </span>
          Núcleo AI
        </Link>
        <nav aria-label="Principal">
          <a href="#recursos">Recursos</a>
          <a href="#arquitetura">Arquitetura</a>
        </nav>
        <Link href="/login" className="button ghost">
          Entrar
        </Link>
      </header>

      <main>
        <SectionHero
          primaryCta={{ label: "Entrar na plataforma", href: "/login", icon: <ArrowRight size={17} /> }}
          secondaryCta={{ label: "Ver arquitetura", href: "#arquitetura" }}
        />

        <section id="recursos" className="landing-section">
          <div className="landing-section__head">
            <p className="eyebrow">O QUE O NÚCLEO FAZ</p>
            <h2>Uma base central de conhecimento para o seu negócio.</h2>
            <p className="muted">
              O Núcleo AI reúne documentos, equipe e inteligência artificial em um workspace empresarial
              seguro, com respostas sempre referenciadas.
            </p>
          </div>
          <div className="landing-features">
            {features.map((feature) => (
              <article className="landing-feature" key={feature.title}>
                <span>
                  <feature.icon size={22} />
                </span>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section id="arquitetura" className="landing-section landing-section--dark">
          <div className="landing-section__head">
            <p className="eyebrow">ARQUITETURA REAL</p>
            <h2>Full stack de ponta a ponta, sem mágica.</h2>
            <p className="muted">
              Browser → Next.js (BFF) → FastAPI → PostgreSQL. Autenticação por JWT com cookies httpOnly e
              isolamento por empresa em toda a camada de dados.
            </p>
          </div>
          <div className="landing-flow">
            <span>Browser</span>
            <span>Next.js BFF</span>
            <span>FastAPI</span>
            <span>PostgreSQL</span>
          </div>
          <div className="landing-stack">
            {stack.map((tech) => (
              <span key={tech}>{tech}</span>
            ))}
          </div>
        </section>

        <section className="landing-cta">
          <div>
            <h2>Pronto para testar?</h2>
            <p>Entre na plataforma ou abra a demonstração e explore o workspace empresarial com dados reais.</p>
          </div>
          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap", alignItems: "center" }}>
            <DemoButton />
            <Link href="/login" className="button ghost">
              Entrar <ArrowRight size={17} />
            </Link>
          </div>
        </section>
      </main>

      <footer className="landing-footer">
        <span>
          <BrainCircuit size={18} /> Núcleo AI
        </span>
        <small>Projeto full stack autoral · Next.js + FastAPI + PostgreSQL</small>
      </footer>
    </>
  );
}
