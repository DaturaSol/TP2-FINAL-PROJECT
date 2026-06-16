// ====== elementos da tela ======

const home = document.getElementById('home');
const loginSection = document.getElementById('login');
const cadastroSection = document.getElementById('cadastro');
const dashboard = document.getElementById('dashboard');

// ====== trocas de telas (controle de navagacao)======

function esconderTodas() {
  home.classList.add('hidden');
  loginSection.classList.add('hidden');
  cadastroSection.classList.add('hidden');
  dashboard.classList.add('hidden');
}

function mostrarHome() {
  esconderTodas();
  home.classList.remove('hidden');
}

function mostrarLogin() {
  esconderTodas();
  loginSection.classList.remove('hidden');
}

function mostrarCadastro() {
  esconderTodas();
  cadastroSection.classList.remove('hidden');
}

function mostrarDashboard(usuario) {
  esconderTodas();
  dashboard.classList.remove('hidden');

  document.getElementById('saudacao').textContent = `Olá, ${usuario.nome}!`;
}

// ====== regras de negocios e autenticacao ======

function cadastrar() {
  const nome = document.getElementById('nome').value.trim();
  const email = document.getElementById('email').value.trim();
  const senha = document.getElementById('senha').value.trim();

  const mensagem = document.getElementById('mensagem');
  //valicação de campos vazios
  if (!nome || !email || !senha) {
    mensagem.textContent = 'Preencha todos os campos.';
    return;
  }

  // Recupera usuários já cadastrados
  const usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];

  // Verifica email duplicado
  const emailExiste = usuarios.find(
    (usuario) => usuario.email.toLowerCase() === email.toLowerCase(),
  );

  if (emailExiste) {
    mensagem.textContent = 'Este e-mail já está cadastrado.';
    return;
  }

  const usuario = {
    nome,
    email,
    senha,
  };

  usuarios.push(usuario);

  localStorage.setItem('usuarios', JSON.stringify(usuarios));

  mensagem.textContent = 'Conta criada com sucesso!';

  setTimeout(() => {
    mostrarLogin();
  }, 1000);
}
// ====== login ======

function login() {
  const email = document.getElementById('login-email').value.trim();
  const senha = document.getElementById('login-senha').value.trim();

  const mensagem = document.getElementById('mensagem-login');

  const usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];

  const usuario = usuarios.find((u) => u.email === email && u.senha === senha);

  if (!usuario) {
    mensagem.textContent = 'usuário não encontrado ou dados incorretos.';
    return;
  }
  if (usuario.email === email && usuario.senha === senha) {
    mensagem.textContent = 'Login realizado com sucesso!';
    mostrarDashboard(usuario);
  } else {
    mensagem.textContent = 'E-mail ou senha inválidos.';
  }
}

//===== limpeza de campos ======
function limparCampos() {
  // Limpa os inputs de login
  document.getElementById('login-email').value = '';
  document.getElementById('login-senha').value = '';
  document.getElementById('mensagem-login').textContent = '';

  // Limpa os inputs de cadastro
  document.getElementById('nome').value = '';
  document.getElementById('email').value = '';
  document.getElementById('senha').value = '';
  document.getElementById('mensagem').textContent = '';
}

// ====== LOGOUT ======

function logout() {
  limparCampos(); // Zera todos os formulários
  mostrarHome(); // Volta para a página inicial
}

// ====== events ======

// Navegação para a Home
document.getElementById('logoHome').addEventListener('click', mostrarHome);
document.getElementById('voltarHome').addEventListener('click', (e) => {
  e.preventDefault();
  mostrarHome();
});

// Navegação para o Login
document.getElementById('abrirLogin').addEventListener('click', mostrarLogin);
document.getElementById('link-ir-login').addEventListener('click', (e) => {
  e.preventDefault();
  mostrarLogin();
});

// Navegação para o Cadastro
document
  .getElementById('abrirCadastro')
  .addEventListener('click', mostrarCadastro);
document
  .getElementById('heroCadastro')
  .addEventListener('click', mostrarCadastro);
document.getElementById('link-ir-cadastro').addEventListener('click', (e) => {
  e.preventDefault();
  mostrarCadastro();
});

// Ações Principais
document.getElementById('criarConta').addEventListener('click', cadastrar);
document.getElementById('fazerLogin').addEventListener('click', login);
document.getElementById('btn-sair').addEventListener('click', logout);

// =========================================================
// 6. INICIALIZAÇÃO
// =========================================================
mostrarHome();
