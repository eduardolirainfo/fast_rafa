from datetime import datetime

import pytz
from tzlocal import get_localzone


def get_local_time_native():
    """
    Retorna o horário local baseado no fuso horário do sistema,
    mas sem informações de fuso horário (naive datetime).
    """
    local_tz = get_localzone()  # Detecta o fuso horário local
    local_time = datetime.now(
        local_tz
    )  # Obtém o horário local com fuso horário
    return local_time.replace(
        tzinfo=None
    )  # Remove a informação de fuso horário


def set_local_time_native(utc_time: datetime) -> datetime:
    """
    Converte o horário UTC para o fuso horário local e retorna um naive datetime.

    :param utc_time: O horário em UTC que será convertido
    :return: O horário convertido para o fuso horário local sem tzinfo
    """
    local_tz = get_localzone()  # Detecta o fuso horário local
    utc_time = pytz.utc.localize(utc_time)  # Torna o horário UTC-aware
    local_time = utc_time.astimezone(local_tz)  # Converte para horário local
    return local_time.replace(tzinfo=None)  # Remove o fuso horário
