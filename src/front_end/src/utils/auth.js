export function setLoggedInUser(usuario) {
  localStorage.setItem('currentUser', JSON.stringify(usuario));
}

export function getLoggedInUser() {
  const userStr = localStorage.getItem('currentUser');
  return userStr ? JSON.parse(userStr) : null;
}

export function logout() {
  localStorage.removeItem('currentUser');
  window.location.href = '/src/login/login.html';
}

export function checkAuth() {
  const user = getLoggedInUser();
  if (!user) {
    window.location.href = '/src/login/login.html';
  }
  return user;
}
