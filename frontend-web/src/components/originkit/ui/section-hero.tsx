import type { ReactNode } from "react";
import { ArrowRight, BrainCircuit, ShieldCheck, Sparkles } from "lucide-react";

type Cta = { label: string; href?: string; onClick?: () => void; variant?: "primary" | "ghost"; icon?: ReactNode };

const VARIANT_CLASS: Record<string, string> = {
  assistant: "section-hero--assistant",
  cards: "section-hero--cards",
};

export function SectionHero({
  variant,
  eyebrow = "INTELIGÊNCIA QUE VENDE COM EVIDÊNCIAS",
  title = "Conhecimento empresarial transformado em ação.",
  description = "Centralize documentos, equipe e automações em uma experiência segura, rápida e mensurável, com respostas sustentadas por fontes internas.",
  primaryCta = { label: "Entrar na plataforma", variant: "primary", icon: <ArrowRight size={17} /> },
  secondaryCta,
  badges = ["Dados isolados por empresa", "Respostas com fontes internas", "Fluxos prontos para produção"],
  children,
}: {
  variant?: "assistant" | "cards";
  eyebrow?: string;
  title?: string;
  description?: string;
  primaryCta?: Cta;
  secondaryCta?: Cta;
  badges?: string[];
  children?: ReactNode;
}) {
  const variantClass = variant ? VARIANT_CLASS[variant] ?? "" : "";
  return (
    <section className={`section-hero ${variantClass}`.trim()}>
      <div className="section-hero__glow" aria-hidden="true" />
      <div className="section-hero__grid" aria-hidden="true" />
      <div className="section-hero__inner">
        <div className="section-hero__content">
          <p className="section-hero__eyebrow">
            <span className="section-hero__dot" aria-hidden="true" />
            {eyebrow}
          </p>
          <h1 className="section-hero__title">{title}</h1>
          <p className="section-hero__description">{description}</p>
          <div className="section-hero__cta">
            {primaryCta &&
              (primaryCta.href ? (
                <a className={`button ${primaryCta.variant ?? "primary"}`} href={primaryCta.href}>
                  {primaryCta.label}
                  {primaryCta.icon}
                </a>
              ) : (
                <button className={`button ${primaryCta.variant ?? "primary"}`} onClick={primaryCta.onClick}>
                  {primaryCta.label}
                  {primaryCta.icon}
                </button>
              ))}
            {secondaryCta &&
              (secondaryCta.href ? (
                <a className={`button ${secondaryCta.variant ?? "ghost"}`} href={secondaryCta.href}>
                  {secondaryCta.label}
                  {secondaryCta.icon}
                </a>
              ) : (
                <button className={`button ${secondaryCta.variant ?? "ghost"}`} onClick={secondaryCta.onClick}>
                  {secondaryCta.label}
                  {secondaryCta.icon}
                </button>
              ))}
          </div>
          {badges.length > 0 && (
            <ul className="section-hero__badges">
              {badges.map((badge) => (
                <li key={badge}>
                  <ShieldCheck size={15} />
                  {badge}
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="section-hero__visual" aria-hidden="true">
          <div className="section-hero__card">
            <span className="section-hero__card-icon">
              <BrainCircuit size={30} />
            </span>
            <p className="section-hero__card-eyebrow">ASSISTENTE EMPRESARIAL</p>
            <h2>Pergunte. Receba. Com fontes.</h2>
            <p>Respostas diretas baseadas nos documentos e dados da sua empresa, com citações verificáveis.</p>
            <div className="section-hero__card-chips">
              <span>
                <Sparkles size={13} /> Resumo executivo
              </span>
              <span>
                <Sparkles size={13} /> Proposta comercial
              </span>
              <span>
                <Sparkles size={13} /> Análise de mercado
              </span>
            </div>
          </div>
        </div>
      </div>
      {children}
    </section>
  );
}
