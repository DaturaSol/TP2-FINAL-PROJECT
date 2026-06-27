/**
 * GERENCIAMENTO DE AUTENTICAÇÃO E TOKENS
 * Funções para gerenciar usuário logado e token de sessão
 */

// Tipo de armazenamento: 'local' (persiste) ou 'session' (até fechar aba)
const STORAGE_TYPE = 'local'; // Altere para 'session' se preferir

/**
 * Obtém o storage a ser utilizado
 *
 * @returns {Storage} localStorage ou sessionStorage
 *
 * Uso interno: getStorage()
 */
function getStorage() {
  return STORAGE_TYPE === 'session' ? sessionStorage : localStorage;
}

/**
 * Armazena o token de sessão
 *
 * @param {string} token - JWT ou token de autenticação
 * @returns {void}
 *
 * Assertiva de entrada: token deve ser string não vazia
 * Uso: setSessionToken('eyJhbGc...');
 */
export function setSessionToken(token) {
  if (!token || typeof token !== 'string') {
    console.error('Token deve ser uma string não vazia.');
    return;
  }
  getStorage().setItem('sessionToken', token);
}

/**
 * Recupera o token de sessão armazenado
 *
 * @returns {string|null} Token se existir, null caso contrário
 *
 * Assertiva de saída: retorna string ou null
 * Uso: const token = getSessionToken();
 */
export function getSessionToken() {
  return getStorage().getItem('sessionToken');
}

/**
 * Verifica se existe um token de sessão válido
 *
 * @returns {boolean} true se token existe e não está vazio
 *
 * Assertiva de saída: retorna boolean
 * Uso: if (isSessionTokenValid()) { ... }
 */
export function isSessionTokenValid() {
  const token = getSessionToken();
  return token !== null && token !== '';
}

/**
 * Remove o token de sessão
 *
 * @returns {void}
 *
 * Uso: removeSessionToken();
 */
export function removeSessionToken() {
  getStorage().removeItem('sessionToken');
}

/**
 * Armazena dados do usuário logado
 *
 * @param {Object} usuario - Dados do usuário
 * @returns {void}
 *
 * Assertiva de entrada: usuario deve ser um objeto
 * Uso: setLoggedInUser({ id: 1, email: 'user@example.com', nome: 'João' });
 */
export function setLoggedInUser(usuario) {
  if (!usuario || typeof usuario !== 'object') {
    console.error('Usuário deve ser um objeto.');
    return;
  }
  getStorage().setItem('currentUser', JSON.stringify(usuario));
}

/**
 * Recupera dados do usuário logado
 *
 * @returns {Object|null} Dados do usuário se existir, null caso contrário
 *
 * Assertiva de saída: retorna Object ou null
 * Uso: const user = getLoggedInUser();
 */
export function getLoggedInUser() {
  const userStr = getStorage().getItem('currentUser');
  return userStr ? JSON.parse(userStr) : null;
}

/**
 * Verifica se um usuário está autenticado
 *
 * @returns {boolean} true se usuário existe e token é válido
 *
 * Assertiva de saída: retorna boolean
 * Uso: if (isAuthenticated()) { ... }
 */
export function isAuthenticated() {
  return getLoggedInUser() !== null && isSessionTokenValid();
}

/**
 * Realiza logout do usuário
 * Remove token, dados do usuário e redireciona para login
 *
 * @returns {void}
 *
 * Uso: logout();
 */
export function logout() {
  removeSessionToken();
  getStorage().removeItem('currentUser');
  window.location.href = '/src/login/login.html';
}

/**
 * Verifica se está autenticado e redireciona se não estiver
 * Deve ser chamado no carregamento das páginas protegidas
 *
 * @returns {Object|null} Dados do usuário se autenticado, null caso contrário
 *
 * Assertiva de saída: retorna Object ou null; redireciona se não autenticado
 * Uso: const user = checkAuth(); // Chame no inicio da página
 */
export function checkAuth() {
  const user = getLoggedInUser();
  const token = getSessionToken();

  if (!user || !token) {
    window.location.href = '/src/login/login.html';
    return null;
  }

  return user;
}
