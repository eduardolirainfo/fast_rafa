from datetime import datetime, timedelta

from fast_rafa.models.event import Event

# IDs das organizações e usuários já existentes
organizacoes = [1, 2]  # IDs das organizações
usuarios = [1, 2, 3]  # IDs dos usuários

events_seed = [
    {
        'id_organizacao': organizacoes[0],
        'id_usuario': usuarios[0],
        'fechado': datetime.utcnow() + timedelta(days=1),
        'titulo': 'Feira de Sustentabilidade',
        'descricao': (
            'Evento voltado para práticas sustentáveis e educação ambiental.'
        ),
        'data': datetime.utcnow() + timedelta(days=15),
        'url_imagem': 'http://imagem.com/feira-sustentabilidade.jpg',
        'criado_em': datetime.utcnow(),
        'atualizado_em': datetime.utcnow(),
    },
    {
        'id_organizacao': organizacoes[1],
        'id_usuario': usuarios[1],
        'fechado': datetime.utcnow() + timedelta(days=3),
        'titulo': 'Oficina de Compostagem',
        'descricao': ('Aprenda a transformar resíduos orgânicos em adubo.'),
        'data': datetime.utcnow() + timedelta(days=20),
        'url_imagem': 'http://imagem.com/oficina-compostagem.jpg',
        'criado_em': datetime.utcnow(),
        'atualizado_em': datetime.utcnow(),
    },
    {
        'id_organizacao': organizacoes[0],
        'id_usuario': usuarios[2],
        'fechado': datetime.utcnow() + timedelta(days=5),
        'titulo': 'Campanha de Doação de Alimentos',
        'descricao': (
            'Doação de alimentos para famílias em situação de vulnerabilidade.'
        ),
        'data': datetime.utcnow() + timedelta(days=25),
        'url_imagem': 'http://imagem.com/doacao-alimentos.jpg',
        'criado_em': datetime.utcnow(),
        'atualizado_em': datetime.utcnow(),
    },
]


# Função para criar eventos
def seed_events(session):
    for event_data in events_seed:
        new_event = Event(**event_data)
        session.add(new_event)
    session.commit()

    return 'Dados de eventos inseridos com sucesso!'


def undo_events(session):
    session.execute('TRUNCATE events RESTART IDENTITY CASCADE;')
    session.commit()

    return 'Dados de eventos removidos com sucesso!'
