/**
 * VALIDADORES DE ENTRADA
 * Funções simples e compreensíveis para validar email e senha
 */

/**
 * Valida se um email está no formato correto
 *
 * @param {string} email - Email a validar
 * @returns {Object} { isValid: boolean, message: string }
 *
 * Uso: const result = validateEmail('user@example.com');
 */
export function validateEmail(email) {
  // Entrada: deve ser string não vazia
  if (!email || typeof email !== 'string' || email.trim() === '') {
    return {
      isValid: false,
      message: 'Por favor, preencha o seu Email.',
    };
  }

  // Trim para remover espaços
  const emailTrimmed = email.trim();

  // Regex simples para validar email: algo@algo.algo
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Saída: objeto com status e mensagem
  if (emailRegex.test(emailTrimmed)) {
    return {
      isValid: true,
      message: '',
    };
  } else {
    return {
      isValid: false,
      message: 'Ops! Digite um Email válido (ex: seu.nome@email.com).',
    };
  }
}

/**
 * Valida se uma senha é forte
 * Critérios: mínimo 8 caracteres, pelo menos 1 número, 1 maiúscula, 1 minúscula
 *
 * @param {string} senha - Senha a validar
 * @returns {Object} { isValid: boolean, message: string, requirements: Object }
 *
 * Uso: const result = validatePassword('Senha123');
 */
export function validatePassword(senha) {
  // Entrada: deve ser string não vazia
  if (!senha || typeof senha !== 'string') {
    return {
      isValid: false,
      message: 'Por favor, preencha a sua Senha.',
      requirements: {
        minLength: false,
        hasNumber: false,
        hasUpperCase: false,
        hasLowerCase: false,
      },
    };
  }

  // Critérios de validação
  const minLength = senha.length >= 8;
  const hasNumber = /\d/.test(senha);
  const hasUpperCase = /[A-Z]/.test(senha);
  const hasLowerCase = /[a-z]/.test(senha);

  // Saída: objeto detalhado com status de cada critério
  const requirements = {
    minLength,
    hasNumber,
    hasUpperCase,
    hasLowerCase,
  };

  const isValid = minLength && hasNumber && hasUpperCase && hasLowerCase;

  if (isValid) {
    return {
      isValid: true,
      message: 'Senha forte.',
      requirements,
    };
  } else {
    const mensagens = [];
    if (!minLength) mensagens.push('mínimo 8 caracteres');
    if (!hasNumber) mensagens.push('pelo menos 1 número');
    if (!hasUpperCase) mensagens.push('pelo menos 1 letra maiúscula');
    if (!hasLowerCase) mensagens.push('pelo menos 1 letra minúscula');

    return {
      isValid: false,
      message: `Senha fraca. A senha deve conter ${mensagens.join(', ')}.`,
      requirements,
    };
  }
}

/**
 * Valida a senha para LOGIN
 * Apenas verifica se o campo foi preenchido.
 */
export function validateLoginPassword(senha) {
  if (!senha || typeof senha !== 'string' || senha.trim() === '') {
    return {
      isValid: false,
      message: 'Por favor, preencha a sua senha.',
    };
  }

  return {
    isValid: true,
    message: '',
  };
}

/**
 * Valida email e senha juntos
 *
 * @param {string} email - Email do usuário
 * @param {string} senha - Senha do usuário
 * @returns {Object} { isValid: boolean, errors: Object }
 *
 * Uso: const result = validateLoginForm('user@example.com', 'Senha123');
 */
export function validateLoginForm(email, senha) {
  // Entrada: ambos devem ser strings
  const emailValidation = validateEmail(email);
  const senhaValidation = validateLoginPassword(senha);

  // Saída: objeto com status geral e detalhes dos erros
  return {
    isValid: emailValidation.isValid && senhaValidation.isValid,
    errors: {
      email: emailValidation.isValid ? null : emailValidation.message,
      senha: senhaValidation.isValid ? null : senhaValidation.message,
    },
    details: {
      email: emailValidation,
      senha: senhaValidation,
    },
  };
}

/**
 * Gera hash SHA-256 da senha
 * Usa a API nativa SubtleCrypto (suportada em todos os navegadores modernos)
 *
 * @param {string} senha - Senha em texto plano
 * @returns {Promise<string>} Hash SHA-256 em hexadecimal
 *
 * Assertiva de entrada: senha deve ser string não vazia
 * Assertiva de saída: retorna Promise de string com hash hexadecimal (64 caracteres)
 *
 * Uso: const hashSenha = await hashPassword('Senha123');
 *      // 'a36e58e6b1d8b3c7f9e2d1a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3'
 */
export async function hashPassword(senha) {
  // Validar entrada
  if (!senha || typeof senha !== 'string' || senha.trim() === '') {
    throw new Error('Senha deve ser uma string não vazia.');
  }

  try {
    // Converter string para bytes (UTF-8)
    const encodedSenha = new TextEncoder().encode(senha);

    // Calcular hash SHA-256
    const hashBuffer = await crypto.subtle.digest('SHA-256', encodedSenha);

    // Converter bytes para hexadecimal
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
      .map((b) => b.toString(16).padStart(2, '0'))
      .join('');

    return hashHex;
  } catch (error) {
    console.error('Erro ao gerar hash da senha:', error);
    throw new Error('Não foi possível gerar hash da senha. Tente novamente.', {
      cause: error,
    });
  }
}
