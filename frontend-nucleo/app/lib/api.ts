const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8002";

export type LoginCredentials = {
  email: string;
  senha: string;
};

export type LoginResult = {
  access_token: string;
  token_type: "bearer";
};

export type HealthStatus = {
  status: string;
  mensagem: string;
};

export type User = {
  id: string;
  nome: string;
  email: string;
  perfil: "admin" | "gestor" | "usuario";
  ativo: boolean;
  empresa_id: string;
};

export type Company = { id: string; nome: string };
export type DocumentRecord = { id: string; nome_original: string; tipo_mime: string; tamanho_bytes: number; status: string; criado_em: string };
export type AssistantAnswer = { resposta: string; fontes: { documento_id: string; nome: string; trecho: string; relevancia: number }[]; modo: string };

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });

  if (!response.ok) {
    throw new Error("Não foi possível concluir a solicitação.");
  }

  return response.json() as Promise<T>;
}

export function checkApiHealth(): Promise<HealthStatus> {
  return request<HealthStatus>("/health");
}

export function login(credentials: LoginCredentials): Promise<LoginResult> {
  return request<LoginResult>("/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}

export function listCompanies(): Promise<Company[]> {
  return request<Company[]>("/empresas/");
}

export function registerUser(data: { nome: string; email: string; senha: string; empresa_id: string }): Promise<User> {
  return request<User>("/auth/cadastro", { method: "POST", body: JSON.stringify(data) });
}

export function currentUser(token: string): Promise<User> {
  return request<User>("/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

function sessionHeaders(): HeadersInit {
  const token = typeof window === "undefined" ? "" : localStorage.getItem("nucleo-access-token") ?? "";
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export function listMembers(empresaId: string): Promise<User[]> {
  void empresaId;
  return request<User[]>("/usuarios/", { headers: sessionHeaders() });
}

export function listDocuments(empresaId: string): Promise<DocumentRecord[]> {
  void empresaId;
  return request<DocumentRecord[]>("/documentos/", { headers: sessionHeaders() });
}

export async function uploadDocument(empresaId: string, file: File): Promise<DocumentRecord> {
  void empresaId;
  const form = new FormData(); form.append("arquivo", file);
  const response = await fetch(`${API_URL}/documentos/upload`, { method: "POST", headers: sessionHeaders(), body: form });
  if (!response.ok) throw new Error("Não foi possível enviar o documento.");
  return response.json() as Promise<DocumentRecord>;
}

export function askAssistant(pergunta: string): Promise<AssistantAnswer> {
  return request<AssistantAnswer>("/assistente/perguntar", {
    method: "POST",
    headers: sessionHeaders(),
    body: JSON.stringify({ pergunta }),
  });
}

export function requestPasswordReset(email: string): Promise<{ mensagem: string }> {
  return request<{ mensagem: string }>("/senha/solicitar-redefinicao", { method: "POST", body: JSON.stringify({ email }) });
}

export function confirmPasswordReset(token: string, novaSenha: string): Promise<{ mensagem: string }> {
  return request<{ mensagem: string }>("/senha/confirmar-redefinicao", { method: "POST", body: JSON.stringify({ token, nova_senha: novaSenha }) });
}
