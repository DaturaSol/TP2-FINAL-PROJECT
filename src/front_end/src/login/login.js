import api from '../utils/api.js'; // <-- Importação da configuração centralizada da API
import { setLoggedInUser } from '../utils/auth.js';

async function login() {
  const email = document.getElementById('login-email').value.trim();
  const senha = document.getElementById('login-senha').value.trim();
  const mensagem = document.getElementById('mensagem-login');

  if (!email || !senha) {
    mensagem.textContent = 'Preencha todos os campos.';
    return;
  }

  // =================================================================
  // EXEMPLO DE INTEGRAÇÃO COM BACKEND USANDO AXIOS
  // Descomente esse bloco quando a API estiver pronta!
  // =================================================================
  /*
  try {
    const response = await api.post('/login', {
      email: email,
      password: senha
    });

    // O backend geralmente devolve um token (JWT) e os dados do usuário
    const { token, usuario } = response.data;
    
    // Armazena o token para uso em requisições futuras
    localStorage.setItem('token', token);
    
    // Armazena os dados básicos para a UI do front-end
    setLoggedInUser(usuario);

    mensagem.textContent = 'Login realizado com sucesso! Redirecionando...';
    setTimeout(() => {
      window.location.href = '/src/dashboard/dashboard.html';
    }, 1000);

    return; // Encerra a função para não executar o código local abaixo
  } catch (error) {
    mensagem.textContent = error.response?.data?.message || 'E-mail ou senha inválidos.';
    console.error('Erro de login:', error);
    return;
  }
  */
  // =================================================================

  // -- Código atual baseado em Local Storage (Remover após ligar com API) --
  const usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
  const usuario = usuarios.find((u) => u.email === email && u.senha === senha);

  if (!usuario) {
    mensagem.textContent = 'Usuário não encontrado ou dados incorretos.';
    return;
  }

  mensagem.textContent = 'Login realizado com sucesso! Redirecionando...';
  setLoggedInUser(usuario);

  setTimeout(() => {
    window.location.href = '/src/dashboard/dashboard.html';
  }, 1000);
}

document.getElementById('fazerLogin').addEventListener('click', login);
