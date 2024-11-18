import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
LOG_RETENTION_DAYS = 30  # Manter logs por no máximo 30 dias


def setup_logger():
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    log_filename_base = datetime.now().strftime('%Y-%m-%d') + '.log'
    check_filename = 'log_check_done.txt'

    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        log_file = get_log_file(log_filename_base, log_dir)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    # Função para verificar e excluir logs antigos
    # Se o arquivo de log não for o arquivo atual, ele será excluído
    # se tiver mais de LOG_RETENTION_DAYS dias
    def cleanup_old_logs():
        current_time = datetime.now()
        logger.info(
            f'Iniciando limpeza de logs antigos. Hora atual: {current_time}'
        )
        for log in log_dir.glob('*.log'):
            # Verifique se o arquivo é mais antigo
            # que LOG_RETENTION_DAYS (30 dias)
            log_mod_time = datetime.fromtimestamp(log.stat().st_mtime)
            logger.info(
                f'Arquivo encontrado: {log.name}, '
                f'Data de modificação: {log_mod_time}'
            )

            if log != log_file and (current_time - log_mod_time) > timedelta(
                days=LOG_RETENTION_DAYS
            ):
                try:
                    os.remove(log)
                    logger.info(
                        f'Arquivo de log {log.name} excluído, '
                        'pois está com mais de {LOG_RETENTION_DAYS} dias.'
                    )
                except Exception as e:
                    logger.error(
                        'Erro ao excluir o arquivo de log '
                        f'{log.name}: {str(e)}'
                    )
            else:
                logger.info(
                    f'O arquivo {log.name} não foi excluído. '
                    'Está dentro do limite de {LOG_RETENTION_DAYS} dias.'
                )

    # Função para verificar se já foi feita a verificação hoje
    def has_checked_today():
        check_file = log_dir / check_filename
        if check_file.exists():
            with open(
                check_file, 'r', encoding='utf-8'
            ) as f:  # Adicionando o encoding
                last_checked = f.read().strip()
                if last_checked == datetime.now().strftime('%Y-%m-%d'):
                    return True
        return False

    # Se não tiver verificado hoje,
    # faz a limpeza e registra a data de verificação
    if not has_checked_today():
        cleanup_old_logs()
        with open(log_dir / check_filename, 'w', encoding='utf-8') as f:
            f.write(datetime.now().strftime('%Y-%m-%d'))

    return logger


def get_log_file(log_filename_base, log_dir):
    """
    Função para garantir que o arquivo de log tenha um nome único e
    que o tamanho máximo não seja excedido.
    """
    log_file = log_dir / log_filename_base
    count = 1

    while log_file.exists() and log_file.stat().st_size >= MAX_LOG_SIZE:
        log_file = log_dir / f'{log_filename_base.stem}_{count}.log'
        count += 1

    return log_file
