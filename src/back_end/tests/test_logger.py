# /workspace/src/back_end/tests/test_logger.py
"""Criação de testes unitários para o arquivo logger.

Verirfica se o programa monitora e registra corretamento os
eventos ocorridos no back end.
"""

import logging

from engine.logger import setup_logging


def test_setup_logging_adds_console_handler() -> None:
    """Criação de um console handler.

    Adiciona o handler ao logger raiz.
    Retornando True se não houver erros.
    """
    setup_logging(level="DEBUG", log_file=None)

    root = logging.getLogger()
    assert root.level == logging.DEBUG
    assert any(isinstance(h, logging.StreamHandler) for h in root.handlers)


def test_setup_logging_adds__file_handler() -> None:
    """Criação de um arquivo handler.

    Adiciona o arquivo handler no logger raiz.
    Retornando True se não houver erros.
    """
    setup_logging(level="INFO", log_file="app.log")

    root = logging.getLogger()
    assert root.level == logging.INFO
    assert any(isinstance(h, logging.FileHandler) for h in root.handlers)
