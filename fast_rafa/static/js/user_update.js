function recreateDeletedFields() {
    const form = document.getElementById('formEditProfile');

    // Recriar o campo de confirmação de senha
    const senhaConfirmacaoField = document.createElement('input');
    senhaConfirmacaoField.type = 'password';
    senhaConfirmacaoField.name = 'confirmar_senha';
    senhaConfirmacaoField.id = 'confirmar_senha';
    senhaConfirmacaoField.classList.add('hidden'); // Opcional: manter oculto
    form.appendChild(senhaConfirmacaoField);

    // Recriar o campo de upload de arquivo
    const fileInputField = document.createElement('input');
    fileInputField.type = 'file';
    fileInputField.name = 'file';
    fileInputField.id = 'fileInput';
    fileInputField.accept = 'image/*';
    fileInputField.classList.add('hidden'); // Manter oculto
    form.appendChild(fileInputField);

    // Reativar os event listeners de upload de imagem
    const imageContainer = document.querySelector('.group');
    if (imageContainer && fileInputField) {
        imageContainer.addEventListener('click', () => fileInputField.click());

        fileInputField.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const profileImage = document.getElementById('profile-image');
                    const previewImage = document.getElementById('preview-image');
                    const defaultImage = document.getElementById('default-image');

                    if (profileImage) {
                        profileImage.src = e.target.result;
                    }

                    if (previewImage && defaultImage) {
                        previewImage.src = e.target.result;
                        previewImage.classList.remove('hidden');
                        defaultImage.classList.add('hidden');
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

function getCookieValue(cookieName) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(`${cookieName}=`)) {
            return cookie.substring(cookieName.length + 1);
        }
    }
    return null;
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formEditProfile');
    const feedbackElement = document.getElementById('mensagem-feedback');
    const feedbackText = document.getElementById('texto-feedback');
    const feedbackIcon = document.getElementById('icone-feedback');
    const voluntarioCheckbox = document.getElementById('eh_voluntario');
    const phoneInput = document.querySelector('input[name="telefone"]');

    const userId = document.getElementById('user_id').value;

    let feedbackTimeout;

const previewImage = document.getElementById('preview-image');
const defaultImage = document.getElementById('default-image');
const fileInput = document.getElementById('fileInput');
const imageContainer = document.querySelector('.group');
const profileImage = document.getElementById('profile-image');

if (imageContainer && fileInput) {
    imageContainer.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                // Atualizar a imagem existente
                if (profileImage) {
                    profileImage.src = e.target.result;
                } else {
                    // Criar um novo elemento de imagem e adicioná-lo ao DOM
                    profileImage = document.createElement('img');
                    profileImage.id = 'profile-image';
                    profileImage.src = e.target.result;
                    profileImage.alt = 'Foto de Perfil';
                    profileImage.classList.add('w-full', 'h-full', 'object-cover');

                    // Inserir o novo elemento de imagem no mesmo lugar da antiga
                    const imageContainer = document.querySelector('.relative.group.cursor-pointer.w-32.h-32.rounded-full.overflow-hidden.bg-primary-100.flex.items-center.justify-center.border-2.border-primary\\/30.hover\\:border-secondary\\/50');
                    imageContainer.insertBefore(profileImage, defaultImage);
                }

                if (previewImage && defaultImage) {
                    previewImage.src = e.target.result;
                    previewImage.classList.remove('hidden');
                    defaultImage.classList.add('hidden');
                }
            };
            reader.readAsDataURL(file);
        }
    });
}
     // Feedback display function
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
            if (isSuccess) {
                 setTimeout(() => {
                    window.location.assign('/profile');
                }, 500);
            }
        }, duration);
    }

    // Volunteer terms modal
    const modalHTML = `
        <div id="volunteerModal" class="fixed inset-0 bg-neutral-600 bg-opacity-80 hidden flex items-center justify-center z-50">
            <div class="bg-neutral-100 p-6 rounded-lg shadow-xl max-w-md w-full">
                <h3 class="text-lg font-bold mb-4">Termos do Voluntariado</h3>
                <div class="mb-4 text-sm text-neutral-600">
                    <p>Ao se registrar como voluntário, você concorda em:</p>
                    <ul class="list-disc pl-5 mt-2">
                        <li>Dedicar tempo para ajudar outros membros da comunidade</li>
                        <li>Seguir nosso código de conduta</li>
                        <li>Participar de treinamentos quando necessário</li>
                        <li>Manter confidencialidade sobre informações sensíveis</li>
                    </ul>
                </div>
                <div class="flex justify-end space-x-3">
                    <button id="cancelVolunteer" class="px-4 py-2 text-neutral-600 hover:bg-neutral-100 rounded">
                        Cancelar
                    </button>
                    <button id="confirmVolunteer" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                        Aceito os Termos
                    </button>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    const modal = document.getElementById('volunteerModal');
    const confirmBtn = document.getElementById('confirmVolunteer');
    const cancelBtn = document.getElementById('cancelVolunteer');

    voluntarioCheckbox.addEventListener('change', function(e) {
        if (this.checked) {
            modal.classList.remove('hidden');
        }
    });

    confirmBtn.addEventListener('click', function() {
        modal.classList.add('hidden');
        voluntarioCheckbox.checked = true;
    });

    cancelBtn.addEventListener('click', function() {
        modal.classList.add('hidden');
        voluntarioCheckbox.checked = false;
    });

    // Image upload function
    async function uploadImage(file) {
        const imageFormData = new FormData();
        imageFormData.append('file', file);

        try {
            const response = await fetch('/api/v1/uploads/profile-image', {
                method: 'POST',
                body: imageFormData
            });

            if (!response.ok) {
                throw new Error('Falha no upload da imagem');
            }

            const data = await response.json();
            return data.url;
        } catch (error) {
            console.error('Erro no upload da imagem:', error);
            throw error;
        }
    }

 form.addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(form);
    const fileInputSubmit = document.getElementById('fileInput');
    const imagePath = document.getElementById('imagePath');

    formData.set('id_organizacao', parseInt(formData.get('id_organizacao'), 10));

    try {
        const imageFile = fileInputSubmit.files[0];
        if (imageFile) {
            const imageUrl = await uploadImage(imageFile);
            imagePath.value = imageUrl;
            formData.set('url_imagem_perfil', imageUrl);
        }

        const checkboxes = [
            'eh_deletado',
            'eh_voluntario',
            'eh_gerente',
            'deficiencia_auditiva',
            'usa_cadeira_rodas',
            'deficiencia_cognitiva',
            'lgbtq'
        ];

        checkboxes.forEach(checkbox => {
            const checkboxElement = document.querySelector(`input[name="${checkbox}"]`);
            formData.set(checkbox, checkboxElement.checked ? 'true' : 'false');
        });

        const senha = formData.get('senha_hash');
        const senhaConfirmacao = formData.get('confirmar_senha');

        if (senha && senha !== senhaConfirmacao) {
            showFeedback('As senhas não coincidem!', false);
            return;
        } else if (!senha && senhaConfirmacao) {
            showFeedback('Por favor, preencha a senha corretamente.', false);
            return;
        }

        const accessToken = document.getElementById('access_token').value;

        if (!accessToken) {
            showFeedback('Erro ao obter o token de acesso. Tente novamente.', false, 5000);
            return;
        }

        formData.delete('confirmar_senha');
        formData.delete('file');
        if (fileInputSubmit) {
            fileInputSubmit.remove();
        }

        const userData = Object.fromEntries(formData);
        if (!userData.url_imagem_perfil) {
            delete userData.url_imagem_perfil;
        }

        const response = await fetch(`/api/v1/users/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`,
            },
            credentials: 'include',
            body: JSON.stringify(userData)
        });

        const data = await response.json();

        if (response.ok) {
            showFeedback(data.message || 'Perfil atualizado com sucesso!', true, 2000);
        } else {
            let errorMessage = 'Erro ao atualizar perfil. ';

            if (data.detail && Array.isArray(data.detail)) {
                const firstError = data.detail[0];
                if (firstError.msg) {
                    errorMessage += firstError.msg.split('Value error,')[1].trim();
                }
            } else if (response.status === 422) {
                errorMessage += 'Por favor, verifique os dados informados.';
            } else if (response.status === 409) {
                errorMessage += 'Já existe um usuário com este email ou username.';
            } else {
                errorMessage += data.detail || 'Tente novamente mais tarde.';
            }

            showFeedback(errorMessage, false, 5000);
        }
    } catch (error) {
        showFeedback('Erro ao conectar com o servidor. Tente novamente.', false, 5000);
    }

    recreateDeletedFields();
});

    document.querySelector('#mensagem-feedback button').addEventListener('click', () => {
        if (feedbackTimeout) {
            clearTimeout(feedbackTimeout);
        }
        feedbackElement.style.display = 'none';
    });
});
