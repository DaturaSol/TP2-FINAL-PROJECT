import api from '../utils/api.js'; // <-- Importação da configuração centralizada da API
import { setLoggedInUser, setSessionToken } from '../utils/auth.js';
import { validateLoginForm, hashPassword } from '../utils/validators.js';

/**
 * Exibe mensagem de erro no campo específico
 *
 * @param {string} fieldId - ID do elemento para erro (ex: 'erro-login-email')
 * @param {string} message - Mensagem a exibir
 */
function showFieldError(fieldId, message) {
  const errorElement = document.getElementById(fieldId);

  if (errorElement) {
    errorElement.textContent = message;
    errorElement.style.display = message ? 'block' : 'none';
  }
}

/**
 * Limpa mensagens de erro de todos os campos
 */
function clearFieldErrors() {
  showFieldError('erro-login-email', '');
  showFieldError('erro-login-senha', '');
}

/**
 * Função de login com validações
 * 1. Valida email e senha
 * 2. Faz requisição ao servidor
 * 3. Armazena token e dados do usuário
 */
async function login() {
  const email = document.getElementById('login-email').value.trim();
  const senha = document.getElementById('login-senha').value.trim();
  const mensagem = document.getElementById('mensagem-login');

  // Limpa erros anteriores
  clearFieldErrors();
  mensagem.textContent = '';

  // Valida email e senha antes de enviar
  const validation = validateLoginForm(email, senha);

  if (!validation.isValid) {
    // Exibe erros nos campos específicos
    if (validation.errors.email) {
      showFieldError('erro-login-email', validation.errors.email);
    }
    if (validation.errors.senha) {
      showFieldError('erro-login-senha', validation.errors.senha);
    }
    return;
  }

  // =================================================================
  // INTEGRAÇÃO COM BACKEND USANDO AXIOS
  // Descomente esse bloco quando a API estiver pronta!
  // =================================================================
  try {
    // Gera hash SHA-256 da senha
    const senhaHash = await hashPassword(senha);

    const response = await api.post('/login', {
      email: email,
      password: senhaHash, // Envia a senha com hash SHA-256
    });

    // O backend geralmente devolve um token (JWT) e os dados do usuário
    const { token, usuario } = response.data;

    // Armazena o token de sessão para uso em requisições futuras
    setSessionToken(token);

    // Armazena os dados básicos para a UI do front-end
    setLoggedInUser(usuario);

    mensagem.textContent = 'Login realizado com sucesso! Redirecionando...';
    setTimeout(() => {
      window.location.href = '/src/dashboard/dashboard.html';
    }, 1000);

    return; // Encerra a função para não executar o código local abaixo
  } catch (error) {
    mensagem.textContent =
      error.response?.data?.message || 'E-mail ou senha inválidos.';
    console.error('Erro de login:', error);
    return;
  }

  // =================================================================

  // -- Código alternativo com Local Storage (para desenvolvimento local) --
  /*
  const usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
  const usuario = usuarios.find((u) => u.email === email && u.senha === senha);

  if (!usuario) {
    mensagem.textContent = 'Usuário não encontrado ou dados incorretos.';
    return;
  }

  // Gera token fictício para desenvolvimento
  const fakeToken = 'dev_token_' + Date.now();
  setSessionToken(fakeToken);
  setLoggedInUser(usuario);

  mensagem.textContent = 'Login realizado com sucesso! Redirecionando...';
  setTimeout(() => {
    window.location.href = '/src/dashboard/dashboard.html';
  }, 1000);
  */
}

document.getElementById('fazerLogin').addEventListener('click', login);
