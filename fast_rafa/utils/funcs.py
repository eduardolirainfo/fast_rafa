import locale
import re
import unicodedata
from datetime import datetime

from faker import Faker
from sqlalchemy import or_

fake = Faker()


def gerar_slug(nome: str) -> str:
    """Gera um slug a partir do nome da categoria."""
    slug = unicodedata.normalize('NFKD', nome)
    slug = slug.encode('ascii', 'ignore').decode('utf-8')
    slug = re.sub(r'[^\w\s-]', '', slug).strip().lower()
    return re.sub(r'[-\s]+', '-', slug)


def check_url_exists(session, model, url_logo=None, url_imagem=None):
    query = session.query(model)
    conditions = []

    if url_logo:
        conditions.append(model.url_logo == url_logo)
    if url_imagem:
        conditions.append(model.url_imagem == url_imagem)

    if conditions:
        return query.filter(or_(*conditions)).first() is not None
    return False


def generate_unique_url(session, model, is_logo=True, max_attempts=10):
    for _ in range(max_attempts):
        # Usando placeimg.com para gerar URLs de imagens aleatórias
        url = f'https://unsplash.it/800/600?random={fake.random_int(min=1, max=1000)}'

        # Verificar se a URL já existe no banco de dados
        if is_logo:
            if not check_url_exists(session, model, url_logo=url):
                return url
        elif not check_url_exists(session, model, url_imagem=url):
            return url

    raise ValueError(
        f'Não foi possível gerar uma URL única após {max_attempts} tentativas'
    )


def iniciais(nome):
    """Retorna as iniciais do nome"""

    preposicoes_verbos_ligacao = ['da', 'de', 'do', 'e', 'ou', 'para', 'com']
    palavras = [
        palavra.capitalize()
        for palavra in nome.split()
        if palavra.lower() not in preposicoes_verbos_ligacao
    ]
    return ''.join([palavra[0] for palavra in palavras])


def formatar_data(date: datetime, language: str) -> str:
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except locale.Error:
        print(
            'Warning: Locale não suportado. Usando locale padrão (en_US.UTF-8).'
        )

    now = datetime.utcnow()
    delta = now - date

    if delta.days == 0:
        # Mostrar "Horas atrás"
        hours = delta.seconds // 3600
        if hours == 0:
            minutes = delta.seconds // 60
            return f'{minutes} minuto{"s" if minutes > 1 else ""} atrás'
        return f'{hours} hora{"s" if hours > 1 else ""} atrás'
    else:
        # Mostrar data por extenso
        return date.strftime('%d de %B de %Y')
