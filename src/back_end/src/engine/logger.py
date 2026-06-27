# /workspace/src/back_end/src/engine/logger.py
"""Sistema de Logging.

Criado para facilitar o registro e monitoramento dos
eventos ocorridos no back-end.
"""

import logging
import sys


def setup_logging(level: str = "INFO", log_file: str | None = "app.log"):
    """Configurações gerais do logger.

    As configuração definidas abaixo serão herdadas por todos os môdulos que
    chamarem a função 'logging.getLogger(__name__)'.

    """
    # 1.Criação do logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # 2. Evita a criação de loggers duplicados.
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 3. Definição do formato
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 4. Criar um handler para o console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 5. Opcionalmente, criar um handler para arquivo
    if log_file:
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
