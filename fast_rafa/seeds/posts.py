import logging
from random import choice

from faker import Faker
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.posts.models import Post
from fast_rafa.modules.posts.schemas import CreatePost
from fast_rafa.modules.users.models import User

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker('pt_BR')


async def seed_posts(session: Session):
    # Obter IDs de categorias, organizações e usuários
    logger.info('Iniciando a geração de posts...')

    organizacoes = session.query(Organization).all()
    organizacao_ids = [org.id for org in organizacoes]

    usuarios = session.query(User).all()
    usuario_ids = [user.id for user in usuarios]

    if not organizacao_ids or not usuario_ids:
        logger.error('Não há organizações ou usuários cadastrados!')
        return 'Não há organizações ou usuários cadastrados!'

    logger.info(
        f'{len(organizacao_ids)} organizações e '
        f'{len(usuario_ids)} usuários encontrados.'
    )

    for _ in range(10):  # Gera 10 posts fictícios
        dados = {
            'item': fake.boolean(),
            'id_organizacao': choice(organizacao_ids),
            'id_usuario': choice(usuario_ids),
            'titulo': fake.sentence(nb_words=5),
            'descricao': fake.paragraph(nb_sentences=3),
            'quantidade': f'{fake.random_int(min=1, max=100)} unidades',
            'id_categoria': choice(range(1, 4)),
            # Alterando para URL fixa com ID único
            'url_imagem_post': 'https://picsum.photos/id/'
            f'{fake.random_int(min=1, max=1000)}/237/800.jpg',
            'data_validade': fake.date_between(
                start_date='today', end_date='+90d'
            ),
            'status': 1,
            'criado_em': fake.date_time_this_year(),
            'atualizado_em': fake.date_time_this_year(),
        }

        try:
            novo_post_data = CreatePost(**dados)  # Usando a função CreatePost
            novo_post = Post.create(novo_post_data)  # Criando o post

            db_post = session.scalar(
                select(Post).where(Post.titulo == novo_post.titulo)
            )

            if db_post is None:
                session.add(novo_post)
                session.commit()
                session.refresh(novo_post)
                logger.info(f'Post "{novo_post.titulo}" criado com sucesso.')
            else:
                logger.warning(
                    f'O post com o título "{novo_post.titulo}" já existe.'
                )

        except Exception as e:
            logger.error(f'Erro ao criar o post: {str(e)}')

    return 'Posts criados com sucesso!'


async def undo_posts(session: Session):
    logger.info('Iniciando a exclusão de posts...')
    try:
        posts = session.execute(select(Post)).scalars().all()
        for post in posts:
            session.delete(post)
        session.commit()
        logger.info('Posts removidas com sucesso.')

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f'Erro ao desfazer a seed de posts: {str(e)}')
