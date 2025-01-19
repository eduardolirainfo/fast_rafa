document.addEventListener("DOMContentLoaded", function () {
    const postImages = document.querySelectorAll(".post-image");
    const modalToggle = document.getElementById("image-modal-toggle");
    const modalImage = document.getElementById("modal-large-image");
    const modalTitle = document.getElementById("modal-title");
    const modalDescription = document.getElementById("modal-description");
    const modalCategory = document.getElementById("modal-category");
    const modalLikes = document.getElementById("modal-likes-count");
    const modalComments = document.getElementById("modal-comments-count");
    const modalCriado = document.getElementById("modal-date");
    const modalUsername = document.getElementById("modal-username");
    const modalAvatar = document.getElementById("modal-user-avatar");
    const likeButtons = document.querySelectorAll(".likes");
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

    // Verifica se as imagens existem
    if (!postImages || postImages.length === 0) {
        console.error("Nenhuma imagem com a classe .post-image encontrada.");
        return;
    }

    // Adiciona evento de clique nas imagens
    postImages.forEach((img) => {
        img.addEventListener("click", function () {
            modalPostId = img.dataset.postid;
            modalUserId = img.dataset.userid;
            modalFavoritado = img.dataset.favoritado;
            modalImage.src = img.src;
            modalTitle.textContent = img.dataset.title || "Sem título";
            modalDescription.textContent = img.dataset.description || "Sem descrição";
            modalCriado.textContent = img.dataset.date
                ? new Date(img.dataset.date).toLocaleDateString('pt-BR', {
                      day: '2-digit',
                      month: 'long',
                      year: 'numeric',
                  })
                : "Sem data";
            modalUsername.textContent = img.dataset.username || "Sem usuário";
            modalAvatar.src = img.dataset.avatar && img.dataset.avatar !== "None"
                ? "/static" + img.dataset.avatar
                : "/static/img/default-profile.png";
            modalCategory.textContent = img.dataset.category || "Sem categoria";
            modalCategory.className = `px-3 py-1 rounded-full ${img.dataset.categoryslug || "sem-categoria"}`;
            modalLikes.textContent = img.dataset.likes || "0";
            modalComments.textContent = img.dataset.comments || "0";

            // Exibe o modal
            modalToggle.checked = true;


            // Função de likes - Ajustar contexto do modal
            likeButtons.forEach((likeButton) => {
                  if (modalPostId && modalUserId) {
                    const likeIcon = likeButton.querySelector("i");
                    const likesCount = likeButton.querySelector("span");
                     if (modalFavoritado) {
                        likeIcon.classList.remove('fas');
                        likeIcon.classList.add('far');
                    } else {
                        likeIcon.classList.remove('far');
                        likeIcon.classList.add('fas');
                    }

                    likeButton.addEventListener("click", () => {
                        console.log("Clicou no botão de like");
                        addLikeEvent(likeButton, modalPostId, modalUserId, likeIcon, likesCount);
                    });
                }
            });
        });
    });

    // Lógica para fechar o modal ao clicar fora
    function closeModal(event) {
        const modalBox = document.querySelector(".modal-box");
        if (modalBox && !modalBox.contains(event.target) && event.target !== modalToggle) {
            modalToggle.checked = false;
            document.removeEventListener("click", closeModal);
        }
    }
    document.addEventListener("click", closeModal);

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

        element.addEventListener('click', toggleLike);
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
    // // Função para verificar status inicial de like
    // async function checkInitialLikeStatus() {
    //     likeButtons.forEach(async (likeButton) => {
    //         let postId = likeButton.dataset.postId;
    //         let userId = likeButton.dataset.userId;

    //         // Se não encontrar, tenta buscar do modal
    //         if (!postId || !userId) {
    //             const modalImage = document.getElementById('modal-large-image');
    //             if (modalImage) {
    //                 postId = modalImage.dataset.postid;
    //                 userId = modalImage.dataset.userid;
    //             }
    //         }

    //         const likeIcon = likeButton.querySelector('i');

    //         try {
    //             const response = await fetch(`/api/v1/favorites/user/${userId}`);
    //             if (response.ok) {
    //                 const favorites = await response.json();
    //                 const isLiked = favorites.some(fav => fav.id_postagem === parseInt(postId));

    //                 if (isLiked) {
    //                     likeIcon.classList.remove('far');
    //                     likeIcon.classList.add('fas');
    //                 }
    //             }
    //         } catch (error) {
    //             console.error('Erro ao verificar status de like:', error);
    //         }
    //     });
    // }

    // checkInitialLikeStatus();
});
