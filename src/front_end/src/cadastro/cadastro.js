import api from '../utils/api.js'; // <-- Importação da configuração centralizada da API

async function cadastrar() {
  const nome = document.getElementById('nome').value.trim();
  const email = document.getElementById('email').value.trim();
  const senha = document.getElementById('senha').value.trim();

  const mensagem = document.getElementById('mensagem');

  if (!nome || !email || !senha) {
    mensagem.textContent = 'Preencha todos os campos.';
    return;
  }

  // =================================================================
  // EXEMPLO DE INTEGRAÇÃO COM BACKEND USANDO AXIOS
  // Descomente esse bloco quando a API estiver pronta!
  // =================================================================
  /*
  try {
    const response = await api.post('/register', {
      name: nome,
      email: email,
      password: senha
    });

    mensagem.textContent = 'Conta criada com sucesso! Redirecionando...';

    setTimeout(() => {
      window.location.href = '/src/login/login.html';
    }, 1000);

    return; // Encerra a função para não executar o código local abaixo
  } catch (error) {
    mensagem.textContent = error.response?.data?.message || 'Erro ao criar conta. Tente novamente.';
    console.error('Erro de cadastro:', error);
    return;
  }
  */
  // =================================================================

  // -- Código atual baseado em Local Storage (Remover após ligar com API) --
  const usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];

  const emailExiste = usuarios.find(
    (usuario) => usuario.email.toLowerCase() === email.toLowerCase(),
  );

  if (emailExiste) {
    mensagem.textContent = 'Este e-mail já está cadastrado.';
    return;
  }

  const usuario = { nome, email, senha };
  usuarios.push(usuario);

  localStorage.setItem('usuarios', JSON.stringify(usuarios));

  mensagem.textContent = 'Conta criada com sucesso! Redirecionando...';

  setTimeout(() => {
    window.location.href = '/src/login/login.html';
  }, 1000);
}

document.getElementById('criarConta').addEventListener('click', cadastrar);
