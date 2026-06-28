/*
 * Arquivo: cadastro.js
 * Responsável pelo cadastro de novos usuários
 *
 *Funcionalidades:
 * Validação de campos (nome, email, senha)
 * Exibição de mensagens de erro e sucesso
 * Envio de dados para o servidor via API
 * Geração de hash SHA-256 da senha
 * Redirecionamento para tela de login
 */

import api from '../utils/api.js';
import {
  validateEmail,
  validatePassword,
  hashPassword,
} from '../utils/validators.js';
import { loadTheme, toggleTheme } from '../utils/theme.js';

// Carrega tema (claro/escuro) salvo do localStorage ou padrão
loadTheme();

export function showFieldError(fieldId, message) {
  const errorElement = document.getElementById(fieldId);
  if (errorElement) {
    errorElement.textContent = message;
    errorElement.style.display = message ? 'block' : 'none';
  }
}

/**
 * Exibe mensagem de erro no campo específico
 *
 * @param {string} fieldId - ID do elemento para erro
 * @param {string} message - Mensagem a exibir
 */

/**
 * Limpa mensagens de erro de todos os campos
 */
function clearFieldErrors() {
  const errorElements = document.querySelectorAll('.mensagem-erro');
  errorElements.forEach((el) => {
    el.textContent = '';
    el.style.display = 'none';
  });
}

/**
 * Função de cadastro com validações
 * 1. Valida email e senha
 * 2. Valida nome não vazio
 * 3. Faz requisição ao servidor
 */
async function cadastrar() {
  const nome = document.getElementById('nome').value.trim();
  const email = document.getElementById('email').value.trim();
  const senha = document.getElementById('senha').value.trim();
  const mensagem = document.getElementById('mensagem');

  // Limpa erros anteriores
  clearFieldErrors();
  mensagem.textContent = '';
  mensagem.className = '';

  // Valida nome
  let hasError = false;

  if (!nome) {
    showFieldError('erro-nome', 'Por favor, preencha o seu Nome completo.');
    hasError = true;
  }

  // Valida email
  const emailValidation = validateEmail(email);
  if (!emailValidation.isValid) {
    showFieldError('erro-email', emailValidation.message);
    hasError = true;
  }

  // Valida senha
  const senhaValidation = validatePassword(senha);
  if (!senhaValidation.isValid) {
    showFieldError('erro-senha', senhaValidation.message);
    hasError = true;
  }

  if (hasError) {
    return;
  }

  try {
    // Gera hash SHA-256 da senha
    const senhaHash = await hashPassword(senha);

    const response = await api.post('/webhook', {
      object: 'frontend_payload',
      entry: [
        {
          logging: {
            name: nome,
            email: email,
            password: senhaHash, // Envia a senha com hash SHA-256
          },
        },
      ],
    });

    mensagem.className = 'sucesso';
    mensagem.textContent = 'Conta criada com sucesso! Redirecionando...';

    setTimeout(() => {
      window.location.href = '/src/login/login.html';
    }, 1000);
  } catch (error) {
    console.error('Erro de cadastro:', error);

    mensagem.className = 'erro';
    mensagem.textContent =
      error.response?.data?.error || 'Erro ao criar conta. Tente novamente.';
  }
}

document.getElementById('criarConta').addEventListener('click', cadastrar);
