from random import choice

from faker import Faker
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from fast_rafa.models.organization import Organization
from fast_rafa.models.post import Post
from fast_rafa.models.user import User

fake = Faker()


def seed_posts(session: Session):
    # Obter IDs de categorias, organizações e usuários
    organizacoes = session.query(Organization).all()
    organizacao_ids = [org.id for org in organizacoes]

    usuarios = session.query(User).all()
    usuario_ids = [user.id for user in usuarios]

    if not organizacao_ids or not usuario_ids:
        return 'Não há organizações ou usuários cadastrados!'

    for _ in range(10):  # Gera 10 posts fictícios
        dados = {
            'item': fake.boolean(),
            'id_organizacao': choice(organizacao_ids),
            'id_usuario': choice(usuario_ids),
            'titulo': fake.sentence(nb_words=5),
            'descricao': fake.paragraph(nb_sentences=3),
            'quantidade': f'{fake.random_int(min=1, max=100)} unidades',
            'id_categoria': choice(range(1, 4)),
            'url_imagem_post': fake.image_url(),
            'data_validade': fake.date_between(
                start_date='today', end_date='+90d'
            ),
            'status': 1,
            'criado_em': fake.date_time_this_year(),
            'atualizado_em': fake.date_time_this_year(),
        }

        novo_post_data = Post.CreatePost(**dados)  # Usando a função CreatePost
        novo_post = Post.create(novo_post_data)  # Criando o post

        db_post = session.scalar(
            select(Post).where(Post.titulo == novo_post.titulo)
        )

        if db_post is None:
            session.add(novo_post)
            session.commit()
            session.refresh(novo_post)

    return 'Posts criados com sucesso!'


def undo_posts(session: Session):
    session.execute(text('DELETE FROM posts;'))
    session.execute(text('DELETE FROM sqlite_sequence WHERE name="posts";'))
    session.commit()
