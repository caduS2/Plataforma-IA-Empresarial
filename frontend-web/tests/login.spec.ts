import { expect, test } from "@playwright/test";

test("exibe o acesso seguro da plataforma", async ({ page }) => {
  await page.goto("/login");
  await expect(page.getByRole("heading", { name: "Bem-vindo de volta" })).toBeVisible();
  await expect(page.getByLabel("E-mail profissional")).toBeVisible();
  await expect(page.getByLabel("Senha")).toBeVisible();
  await expect(page.getByRole("button", { name: /Entrar na plataforma/ })).toBeVisible();
});
