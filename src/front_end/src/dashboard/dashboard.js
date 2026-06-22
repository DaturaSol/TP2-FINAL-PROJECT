import { checkAuth, logout } from '../utils/auth.js';

// Get the user data and redirect if not logged in
const user = checkAuth();

if (user) {
  document.getElementById('saudacao').textContent = `Olá, ${user.nome}!`;
}

document.getElementById('btn-sair').addEventListener('click', logout);
document.getElementById('btn-sair-nav').addEventListener('click', logout);
