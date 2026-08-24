export type ApiProblem = { detail?: string | Array<{ msg?: string }> };

function problemMessage(problem: ApiProblem): string {
  if (typeof problem.detail === "string") return problem.detail;
  if (Array.isArray(problem.detail)) return problem.detail.map((item) => item.msg).filter(Boolean).join(" ");
  return "Não foi possível concluir a solicitação.";
}

export async function api<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const isForm = options.body instanceof FormData;
  const response = await fetch(`/api/backend${endpoint}`, {
    ...options,
    cache: "no-store",
    headers: { Accept: "application/json", ...(isForm ? {} : { "Content-Type": "application/json" }), ...options.headers },
  });
  if (response.status === 401) {
    // Sessão expirada ou inválida: o BFF já removeu o cookie. Os componentes redirecionam ao login
    // quando detectam este erro via `err.name === "SessionExpiredError"`.
    const err = new Error("Sua sessão expirou. Entre novamente para continuar.");
    err.name = "SessionExpiredError";
    throw err;
  }
  if (!response.ok) {
    const problem = (await response.json().catch(() => ({}))) as ApiProblem;
    throw new Error(problemMessage(problem));
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
