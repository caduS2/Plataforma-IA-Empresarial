import { expect, test } from "@playwright/test";

/**
 * Fluxo E2E de autenticação (P0).
 *
 * Credenciais de demonstração locais — não são secrets de produção.
 * Podem ser sobrescritas por E2E_EMAIL / E2E_SENHA.
 */
const EMAIL = process.env.E2E_EMAIL ?? "admin@demo.com";
const SENHA = process.env.E2E_SENHA ?? "DemoSenha@123";

test.describe("Autenticação (P0)", () => {
  test("bloqueia acesso ao dashboard sem sessão e redireciona para login", async ({ page }) => {
    await page.goto("/dashboard");
    await expect(page).toHaveURL(/\/login/);
    await expect(page.getByRole("heading", { name: "Bem-vindo de volta" })).toBeVisible();
  });

  test("login com senha incorreta exibe erro amigável", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("E-mail profissional").fill(EMAIL);
    await page.getByLabel("Senha").fill("senha-incorreta-123");
    await page.getByRole("button", { name: /Entrar na plataforma/ }).click();
    const erro = page.locator("p.form-error");
    await expect(erro).toBeVisible();
    await expect(erro).toContainText(/inválidos|credenciais|e-mail ou senha/i);
    await expect(page).toHaveURL(/\/login/);
  });

  test("login com sucesso leva ao dashboard e mantém sessão", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("E-mail profissional").fill(EMAIL);
    await page.getByLabel("Senha").fill(SENHA);
    await page.getByRole("button", { name: /Entrar na plataforma/ }).click();
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 15_000 });
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test("logout encerra a sessão e volta a bloquear o dashboard", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("E-mail profissional").fill(EMAIL);
    await page.getByLabel("Senha").fill(SENHA);
    await page.getByRole("button", { name: /Entrar na plataforma/ }).click();
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 15_000 });

    await page.goto("/dashboard");
    await expect(page).toHaveURL(/\/dashboard/);

    await page.request.post("/api/auth/logout");
    await page.goto("/");
    await page.goto("/dashboard");
    await expect(page).toHaveURL(/\/login/);
  });
});
