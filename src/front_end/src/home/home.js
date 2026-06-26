// ====== main.js for index.html (Home) ======
import { getLoggedInUser, logout } from '../utils/auth.js';

const user = getLoggedInUser();

// If user is logged in, optionally show dashboard button instead of login
const loginBtn = document.getElementById('abrirLogin');
const registerBtn = document.getElementById('abrirCadastro');

if (user) {
  loginBtn.textContent = 'Meu Dashboard';
  loginBtn.href = '/src/dashboard/dashboard.html';

  registerBtn.textContent = 'Sair';
  registerBtn.href = '#';
  registerBtn.addEventListener('click', (e) => {
    e.preventDefault();
    logout();
  });
}

document.getElementById('heroCadastro').addEventListener('click', () => {
  window.location.href = user
    ? '/src/dashboard/dashboard.html'
    : '/src/cadastro/cadastro.html';
});
