import api from '../utils/api.js';

async function cadastrar() {
  const nome = document.getElementById('nome').value.trim();
  const email = document.getElementById('email').value.trim();
  const senha = document.getElementById('senha').value.trim();

  const mensagem = document.getElementById('mensagem');

  if (!nome || !email || !senha) {
    mensagem.textContent = 'Preencha todos os campos.';
    return;
  }

  try {
    const response = await api.post('/webhook', {
      object: 'frontend_payload',
      entry: [
        {
          logging: {
            name: nome,
            email: email,
            password: senha,
          },
        },
      ],
    });

    console.log(response.data);

    mensagem.textContent = 'Conta criada com sucesso! Redirecionando...';

    setTimeout(() => {
      window.location.href = '/src/login/login.html';
    }, 1000);
  } catch (error) {
    console.error('Erro de cadastro:', error);

    mensagem.textContent =
      error.response?.data?.error || 'Erro ao criar conta. Tente novamente.';
  }
}

document.getElementById('criarConta').addEventListener('click', cadastrar);
