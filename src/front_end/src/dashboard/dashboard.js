import { checkAuth, logout } from '../utils/auth.js';
import { loadTheme, toggleTheme } from '../utils/theme.js';

// Carrega tema (claro/escuro) salvo do localStorage ou padrão
loadTheme();

/**
 * Inicializa a página do Dashboard.
 *
 * Responsabilidades:
 * 1. Configurar o botão de troca de tema.
 * 2. Validar se o usuário está autenticado.
 * 3. Exibir a saudação personalizada.
 * 4. Configurar os botões de logout.
 */
function initializeDashboard() {
  //botao de troca de tema
  const themeButton = document.getElementById('theme-toggle');

  if (themeButton) {
    themeButton.addEventListener('click', toggleTheme);
  }

  // Get the user data and redirect if not logged in
  const user = checkAuth();

  if (user) {
    document.getElementById('saudacao').textContent = `Olá, ${user.name}!`;
  }
}

document.getElementById('btn-sair').addEventListener('click', logout);
document.getElementById('btn-sair-nav').addEventListener('click', logout);

initializeDashboard();
