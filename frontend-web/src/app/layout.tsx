import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "NÃºcleo AI", template: "%s | NÃºcleo AI" },
  description: "Plataforma empresarial de conhecimento, automaÃ§Ã£o e inteligÃªncia artificial com fontes verificÃ¡veis.",
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
