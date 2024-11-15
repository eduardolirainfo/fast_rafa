from datetime import datetime

from fast_rafa.models.organization import Organization


def seed_organizations(session):
    dados_organizacoes = [
        {
            'id_federal': '12345678901',
            'nao_governamental': True,
            'url_logo': 'https://exemplo.com/logo_educacao.png',
            'url_imagem': 'https://exemplo.com/imagem_educacao.png',
            'abertura': '08:00',
            'fechamento': '18:00',
            'intervalo': '12:00 - 13:00',
            'nome': 'Instituto de Educação para Todos',
            'descricao': (
                'Organização não governamental focada em oferecer acesso '
                'à educação para comunidades carentes.'
            ),
            'rua': 'Rua do Aprendizado',
            'cep': '12345-678',
            'cidade': 'Cidade da Educação',
            'estado': 'Estado do Saber',
            'telefone': '(21) 1234-5678',
            'email': 'contato@educacaoparatodos.org',
            'criado_em': datetime.utcnow(),
            'atualizado_em': datetime.utcnow(),
        },
        {
            'id_federal': '10987654321',
            'nao_governamental': False,
            'url_logo': 'https://exemplo.com/logo_saude.png',
            'url_imagem': 'https://exemplo.com/imagem_saude.png',
            'abertura': '09:00',
            'fechamento': '17:00',
            'intervalo': '12:30 - 13:30',
            'nome': 'Centro de Saúde Pública',
            'descricao': (
                'Organização governamental dedicada a promover a saúde '
                'pública e bem-estar social.'
            ),
            'rua': 'Avenida da Saúde',
            'cep': '87654-321',
            'cidade': 'Cidade da Saúde',
            'estado': 'Estado do Cuidado',
            'telefone': '(21) 9876-5432',
            'email': 'contato@centrodesaude.gov',
            'criado_em': datetime.utcnow(),
            'atualizado_em': datetime.utcnow(),
        },
    ]

    for dados in dados_organizacoes:
        organizacao = Organization(**dados)
        session.add(organizacao)

    session.commit()

    return 'Organizações criadas com sucesso!'


def undo_organizations(session):
    session.execute('TRUNCATE organizations RESTART IDENTITY CASCADE;')
    session.commit()

    return 'Organizações deletadas com sucesso!'
