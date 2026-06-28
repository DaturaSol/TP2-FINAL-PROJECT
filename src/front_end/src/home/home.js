/** HOME (Página Inicial) */
/** Responsável por:
 * - Carregar o tema salvo;
 * - Atualizar os botões da navbar;
 * - Redirecionar usuário;
 * - Realizar logout. */

import { getLoggedInUser, logout } from '../utils/auth.js';
import { loadTheme, toggleTheme } from '../utils/theme.js';

/**
 * Carrega o tema salvo no navegador.
 *
 * Caso exista um tema salvo no localStorage, ele será aplicado.
 */
loadTheme();

/**
 * Configura o botão de troca de tema.
 *
 * O evento só é registrado caso o botão exista na página.
 */
const themeButton = document.getElementById('theme-toggle');

if (themeButton) {
  themeButton.addEventListener('click', toggleTheme);
}

/**
 * Recupera os dados do usuário autenticado.
 *
 * Retorna null caso não exista usuário logado.
 */
const user = getLoggedInUser();

/**
 * Obtém os botões principais da navbar.
 */
const loginBtn = document.getElementById('abrirLogin');
const registerBtn = document.getElementById('abrirCadastro');

/**
 * Caso exista um usuário autenticado,
 * altera os botões da navegação.
 */
if (user) {
  loginBtn.textContent = 'Minha Conta';
  loginBtn.href = '/src/dashboard/dashboard.html';

  registerBtn.textContent = 'Sair';
  registerBtn.href = '#';

  registerBtn.addEventListener('click', (e) => {
    e.preventDefault();

    logout();
  });
}

/**
 * Botão principal ("Criar Conta")
 *
 * - Usuário autenticado → Dashboard.
 * - Usuário não autenticado → Cadastro.
 */
document.getElementById('heroCadastro').addEventListener('click', () => {
  window.location.href = user
    ? '/src/dashboard/dashboard.html'
    : '/src/cadastro/cadastro.html';
});
