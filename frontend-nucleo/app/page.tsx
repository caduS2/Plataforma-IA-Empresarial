import {
  ArrowRight, BarChart3, BookOpenCheck, Bot, Check, Database,
  LockKeyhole, Play, ShieldCheck, Sparkles, Workflow, Zap,
} from "lucide-react";
import Link from "next/link";

const outcomes = [
  ["37", "reuniões influenciadas", "+18% no mês"],
  ["R$ 1,84 mi", "pipeline assistido", "com fontes rastreáveis"],
  ["86h", "de trabalho recuperadas", "pela equipe comercial"],
];

export default function Home() {
  return (
    <main className="landing">
      <header className="landing-nav">
        <a className="landing-brand" href="#top" aria-label="Núcleo AI"><span><Sparkles size={18}/></span>núcleo<i>.</i>ai</a>
        <nav aria-label="Navegação principal"><a href="#produto">Produto</a><a href="#agentes">Agentes</a><a href="#seguranca">Segurança</a><a href="#resultados">Resultados</a></nav>
        <div><Link className="link-login" href="/login">Entrar</Link><Link className="button-dark" href="/dashboard">Explorar plataforma <ArrowRight size={15}/></Link></div>
      </header>

      <section className="hero" id="top">
        <div className="hero-glow" />
        <div className="hero-copy">
          <div className="hero-badge"><span>Nova geração</span> Copiloto comercial com fontes verificáveis <ArrowRight size={13}/></div>
          <h1>Menos busca.<br/><em>Mais vendas.</em></h1>
          <p>A Núcleo AI conecta documentos, conversas e processos para sua equipe vender melhor — com agentes especializados, governança e impacto mensurável.</p>
          <div className="hero-actions"><Link className="button-primary" href="/dashboard">Conhecer a plataforma <ArrowRight size={16}/></Link><Link className="button-ghost" href="/assistant"><span><Play size={13} fill="currentColor"/></span> Ver copiloto em ação</Link></div>
          <small><Check size={14}/> Sem cartão &nbsp; <Check size={14}/> Configuração guiada &nbsp; <Check size={14}/> Dados protegidos</small>
        </div>

        <div className="hero-product" aria-label="Prévia da plataforma Núcleo AI">
          <div className="hp-top"><span className="hp-logo"><Sparkles size={13}/></span><b>Núcleo AI</b><span className="hp-search">Pesquisar <kbd>⌘ K</kbd></span><span className="hp-avatar">MC</span></div>
          <div className="hp-body">
            <div className="hp-side"><i/><i/><i className="selected"/><i/><i/></div>
            <div className="hp-content">
              <div className="hp-label">CENTRAL DE COMANDO</div><h3>Operação comercial</h3>
              <div className="hp-metrics"><div><span>Receita influenciada</span><strong>R$ 1,84 mi</strong><em>↑ 24,8%</em></div><div><span>Reuniões marcadas</span><strong>37</strong><em>↑ 18,2%</em></div><div><span>Taxa de aprovação</span><strong>92,4%</strong><em>↑ 4,1%</em></div></div>
              <div className="hp-grid"><div className="hp-chart"><span>Pipeline influenciado pela IA</span><b>R$ 1.842.900</b><div>{[44,58,50,72,64,86,78,93].map((h,i)=><i key={i} style={{height:`${h}%`}}/>)}</div></div><div className="hp-insight"><Sparkles size={17}/><small>PRÓXIMA MELHOR AÇÃO</small><b>5 oportunidades precisam de follow-up hoje.</b><button>Preparar mensagens <ArrowRight size={12}/></button></div></div>
              <div className="hp-ai"><span><Bot size={16}/></span><div><b>Copiloto de Vendas</b><p>Posso comparar as oportunidades em risco e preparar os próximos passos com base no seu playbook.</p></div><button>Perguntar →</button></div>
            </div>
          </div>
        </div>
      </section>

      <section className="outcome-strip" id="resultados"><p>Resultados que a liderança consegue medir</p>{outcomes.map(([value,label,note])=><div key={value}><strong>{value}</strong><span>{label}<small>{note}</small></span></div>)}</section>

      <section className="product-section" id="produto">
        <div className="section-kicker">UMA PLATAFORMA. TODO O CICLO COMERCIAL.</div><h2>Da informação dispersa à<br/><em>próxima melhor ação.</em></h2><p>A IA encontra, explica e transforma o conhecimento da empresa em trabalho concluído.</p>
        <div className="feature-grid">
          <article className="feature-large"><span className="feature-icon"><Bot/></span><div><small>COPILOTO COMERCIAL</small><h3>Respostas confiáveis,<br/>prontas para agir.</h3><p>Converse com sua base, valide cada fonte e transforme respostas em e-mails, propostas ou tarefas no CRM.</p><Link href="/assistant">Explorar o assistente <ArrowRight size={14}/></Link></div><div className="mini-chat"><p>Como responder à objeção de preço da Acme?</p><div><span><Sparkles size={12}/></span><p>Reposicione a conversa em valor e use o case Vitta, que reduziu o ciclo comercial em 22%.<small><BookOpenCheck size={11}/> Playbook · pág. 18 &nbsp; 96% confiança</small></p></div></div></article>
          <article><span className="feature-icon mint"><Database/></span><small>CONHECIMENTO</small><h3>Uma fonte de verdade viva.</h3><p>Organize, versione e governe tudo que seus agentes podem consultar.</p><div className="doc-stack"><i>PDF</i><i>DOCX</i><i>XLSX</i><span>+152</span></div></article>
          <article><span className="feature-icon amber"><Workflow/></span><small>AUTOMAÇÃO</small><h3>Da resposta ao resultado.</h3><p>Conecte CRM, e-mail e calendário para concluir tarefas sem trocar de tela.</p><div className="flow-line"><span>IA</span><i/><span>CRM</span><i/><span>E-mail</span></div></article>
        </div>
      </section>

      <section className="agents-section" id="agentes"><div><div className="section-kicker">AGENTES ESPECIALIZADOS</div><h2>Uma equipe de IA que<br/><em>conhece o seu negócio.</em></h2><p>Cada agente combina um objetivo, fontes autorizadas e ações seguras.</p><Link className="button-primary" href="/assistant">Conhecer os agentes <ArrowRight size={15}/></Link></div><div className="agent-orbit"><span className="orbit-core"><Sparkles/></span>{[["Objeções","#8b5cf6"],["Propostas","#f59e0b"],["Reuniões","#10b981"],["CRM","#3b82f6"],["E-mails","#ec4899"],["Coach","#14b8a6"]].map(([n,c],i)=><div key={n} className={`orbit-agent a${i}`}><i style={{background:c}}/><span>{n}</span></div>)}</div></section>

      <section className="security-section" id="seguranca"><div className="security-card"><ShieldCheck/><span>SEGURANÇA POR PRINCÍPIO</span><h2>Seu conhecimento protegido.<br/>Sua equipe no controle.</h2><p>Isolamento por empresa, permissões granulares, fontes rastreáveis e trilha de auditoria em cada ação.</p><div><span><LockKeyhole/> Controle de acesso</span><span><Database/> Dados segregados</span><span><BarChart3/> Auditoria completa</span><span><Zap/> Monitoramento contínuo</span></div></div></section>

      <section className="final-cta"><div><Sparkles/><span>NÚCLEO AI</span></div><h2>Seu próximo melhor resultado<br/>começa com a pergunta certa.</h2><p>Explore a nova experiência da plataforma e veja como a IA pode acelerar sua operação comercial.</p><Link className="button-light" href="/dashboard">Entrar na plataforma <ArrowRight size={16}/></Link></section>
      <footer><a className="landing-brand" href="#top"><span><Sparkles size={16}/></span>núcleo<i>.</i>ai</a><p>Inteligência que move negócios.</p><small>© 2026 Núcleo AI · Produto em evolução</small></footer>
    </main>
  );
}
