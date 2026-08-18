import { expect, test } from "@playwright/test";

test("exibe o acesso seguro da plataforma", async ({ page }) => {
  const response = await page.goto("/login");
  expect(response?.headers()["content-security-policy"]).toContain("frame-ancestors 'none'");
  expect(response?.headers()["x-content-type-options"]).toBe("nosniff");
  expect(response?.headers()["referrer-policy"]).toBe("strict-origin-when-cross-origin");
  await expect(page.getByRole("heading", { name: "Bem-vindo de volta" })).toBeVisible();
  await expect(page.getByLabel("E-mail profissional")).toBeVisible();
  await expect(page.getByLabel("Senha")).toBeVisible();
  await expect(page.getByRole("button", { name: /Entrar na plataforma/ })).toBeVisible();
});

test("redireciona raiz e dashboard sem sessão para o login", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveURL(/\/login$/);
  await page.goto("/dashboard");
  await expect(page).toHaveURL(/\/login$/);
});

test("exibe recuperação de senha sem consultar o backend", async ({ page }) => {
  await page.goto("/esqueci-minha-senha");
  await expect(page.getByRole("heading", { name: "Redefina sua senha" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Enviar instruções" })).toBeVisible();
});

test("trata links sem token de forma segura", async ({ page }) => {
  await page.goto("/redefinir-senha");
  await expect(page.getByText("Link inválido.")).toBeVisible();
  await page.goto("/aceitar-convite");
  await expect(page.getByText(/não contém um token válido/)).toBeVisible();
});

test("valida payload de login e encerra sessão pelas APIs internas", async ({ request }) => {
  const invalidLogin = await request.post("/api/auth/login", { data: { email: "invalido", senha: "curta" } });
  expect(invalidLogin.status()).toBe(422);
  const protectedInvite = await request.post("/api/backend/convites", {
    data: { email: "convidado@example.com", perfil: "usuario" },
  });
  expect([401, 403]).toContain(protectedInvite.status());
  const logout = await request.post("/api/auth/logout");
  expect(logout.status()).toBe(200);
});
