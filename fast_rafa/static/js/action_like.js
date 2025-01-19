document.addEventListener('DOMContentLoaded', function () {
    // Seleciona todos os botões de like e imagens de post
    const likeButtons = document.querySelectorAll('.likes');
    const feedbackElement = document.getElementById('mensagem-feedback');
    const feedbackText = document.getElementById('texto-feedback');
    const feedbackIcon = document.getElementById('icone-feedback');
    let feedbackTimeout;

    function showFeedback(message, isSuccess = true, duration = 5000) {
        if (feedbackTimeout) {
            clearTimeout(feedbackTimeout);
        }

        feedbackText.textContent = message;
        feedbackIcon.className = isSuccess
            ? 'fas fa-check-circle text-green-500 text-xl'
            : 'fas fa-exclamation-circle text-red-500 text-xl';
        feedbackElement.style.display = 'block';

        feedbackTimeout = setTimeout(() => {
            feedbackElement.style.display = 'none';
        }, duration);
    }

    // Função para adicionar evento de like
    function addLikeEvent(element, postId, userId, likeIcon, likesCount) {
        async function toggleLike() {
            try {
                if (!userId) {
                    showFeedback('Por favor, faça login para curtir esta postagem');
                    return;
                }

                const isCurrentlyLiked = likeIcon.classList.contains('fas');
                const url = isCurrentlyLiked
                    ? `/api/v1/favorites/${postId}`
                    : `/api/v1/favorites/${userId}/${postId}`;

                const method = isCurrentlyLiked ? 'DELETE' : 'POST';

                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (response.ok) {
                    const data = await response.json();

                    // Atualiza o ícone
                    likeIcon.classList.toggle('far');
                    likeIcon.classList.toggle('fas');

                    // Atualiza o contador com o número exato de likes
                    likesCount.textContent = data.total_likes;

                    // Atualiza também o like na listagem e no modal, se existirem
                    updateRelatedLikeButtons(postId, data.total_likes, isCurrentlyLiked);
                } else {
                    const errorData = await response.json();
                    showFeedback(`Erro: ${errorData.detail}`);
                    return;
                }
            } catch (error) {
                console.error('Erro ao alternar like:', error);
                showFeedback('Ocorreu um erro ao processar seu like');
                return;
            }
        }
        if  (element){
            element.addEventListener('click', toggleLike);
        }
    }

    // Função para atualizar likes relacionados
    function updateRelatedLikeButtons(postId, totalLikes, wasLiked) {
        const relatedLikeButtons = document.querySelectorAll(`.likes[data-post-id="${postId}"]`);
        relatedLikeButtons.forEach(button => {
            const likeIcon = button.querySelector('i');
            const likesCountSpan = button.querySelector('span');

            if (wasLiked) {
                likeIcon.classList.remove('fas');
                likeIcon.classList.add('far');
            } else {
                likeIcon.classList.remove('far');
                likeIcon.classList.add('fas');
            }

            likesCountSpan.textContent = totalLikes;
        });
    }

    // Adiciona evento de like para todos os botões de like
    likeButtons.forEach(likeButton => {
         let postId = likeButton.dataset.postId;
        let userId = likeButton.dataset.userId;

         if (!postId || !userId) {
            const modalImage = document.getElementById('modal-large-image');
            if (modalImage) {
                postId = modalImage.dataset.postid;
                userId = modalImage.dataset.userid;
            }
        }

        const likeIcon = likeButton.querySelector('i');
        const likesCount = likeButton.querySelector('span');

        if (postId && userId) {
            addLikeEvent(likeButton, postId, userId, likeIcon, likesCount);
        }
    });

    // Função para verificar status inicial de like
    async function checkInitialLikeStatus() {
        likeButtons.forEach(async (likeButton) => {
            let postId = likeButton.dataset.postId;
            let userId = likeButton.dataset.userId;

            // Se não encontrar, tenta buscar do modal
            if (!postId || !userId) {
                const modalImage = document.getElementById('modal-large-image');
                if (modalImage) {
                    postId = modalImage.dataset.postid;
                    userId = modalImage.dataset.userid;
                }
            }

            const likeIcon = likeButton.querySelector('i');

            try {
                const response = await fetch(`/api/v1/favorites/user/${userId}`);
                if (response.ok) {
                    const favorites = await response.json();
                    const isLiked = favorites.some(fav => fav.id_postagem === parseInt(postId));

                    if (isLiked) {
                        likeIcon.classList.remove('far');
                        likeIcon.classList.add('fas');
                    }
                }
            } catch (error) {
                console.error('Erro ao verificar status de like:', error);
            }
        });
    }

    // checkInitialLikeStatus();
});
