import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";
import "./landing.css";

export const metadata: Metadata = {
  title: { default: "Núcleo AI", template: "%s | Núcleo AI" },
  description: "Plataforma empresarial de conhecimento, automação e inteligência artificial com fontes verificáveis.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html
      lang="pt-BR"
      className="h-full antialiased"
    >
      <body className="min-h-full">{children}</body>
    </html>
  );
}
