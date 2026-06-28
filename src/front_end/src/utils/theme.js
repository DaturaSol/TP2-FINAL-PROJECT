const THEME_KEY = 'theme';

/**
 * Aplica o tema
 */
export function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  document.documentElement.style.colorScheme = theme;

  localStorage.setItem(THEME_KEY, theme);

  updateThemeIcon(theme);
}

/**
 * Alterna entre claro e escuro
 */
export function toggleTheme() {
  const current =
    document.documentElement.getAttribute('data-theme') || 'light';

  const next = current === 'light' ? 'dark' : 'light';

  setTheme(next);
}

/**
 * Carrega tema salvo
 */
export function loadTheme() {
  const savedTheme = localStorage.getItem(THEME_KEY) || 'light';

  setTheme(savedTheme);
}

/**
 * Atualiza o ícone
 */
function updateThemeIcon(theme) {
  const button = document.getElementById('theme-toggle');

  if (!button) return;

  button.textContent = theme === 'dark' ? '☀️' : '🌙';
}
