function maskPhone(event) {
    let input = event.target;
    let value = input.value.replace(/\D/g, ''); // Remove tudo que não é dígito
    let formattedValue = '';

    // Aplica a máscara dependendo do tamanho do número
    if (value.length <= 11) {
        // Formato: (99) 99999-9999
        if (value.length > 2) {
            formattedValue += '(' + value.substring(0, 2) + ') ';
        } else {
            formattedValue += value;
        }

        if (value.length > 2) {
            if (value.length <= 7) {
                formattedValue += value.substring(2);
            } else {
                formattedValue += value.substring(2, 7) + '-' + value.substring(7, 11);
            }
        }
    }

    input.value = formattedValue;
}

// Função para impedir caracteres não numéricos
function validatePhone(event) {
    // Permite apenas números, backspace, delete e teclas de navegação
    if (!event.key.match(/\d/) &&
        !['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(event.key)) {
        event.preventDefault();
    }
}

// document.addEventListener('DOMContentLoaded', function() {

//     const form = document.getElementById('formRegistro');
//     const feedbackElement = document.getElementById('mensagem-feedback');
//     const feedbackText = document.getElementById('texto-feedback');
//     const feedbackIcon = document.getElementById('icone-feedback');
//     const voluntarioCheckbox = document.getElementById('eh_voluntario');
//     let feedbackTimeout;


//     const phoneInput = document.querySelector('input[name="telefone"]');
//     if (phoneInput) {
//         phoneInput.addEventListener('input', maskPhone);
//         phoneInput.addEventListener('keydown', validatePhone);

//         // Adiciona placeholder para indicar o formato
//         phoneInput.setAttribute('placeholder', '(99) 99999-9999');

//         // Limita o tamanho máximo
//         phoneInput.setAttribute('maxlength', '15');
//     }

//     // Substituir o input de URL por um container de imagem personalizado
//     const imageInputContainer = document.querySelector('div.relative:has(input[name="url_imagem_perfil"])');
//     const imageInput = document.querySelector('input[name="url_imagem_perfil"]');

//     // Configurar o preview da imagem
//     const previewImage = document.getElementById('preview-image');
//     const defaultImage = document.getElementById('default-image');
//     const fileInput = document.getElementById('profile-image-input');
//     const imageContainer = document.querySelector('.group');

//     imageContainer.addEventListener('click', () => fileInput.click());

//     fileInput.addEventListener('change', function(e) {
//         const file = e.target.files[0];
//         if (file) {
//             const reader = new FileReader();
//             reader.onload = function(e) {
//                 previewImage.src = e.target.result;
//                 previewImage.classList.remove('hidden');
//                 defaultImage.classList.add('hidden');
//             };
//             reader.readAsDataURL(file);
//         }
//     });

//     function showFeedback(message, isSuccess = true, duration = 5000) {
//         if (feedbackTimeout) {
//             clearTimeout(feedbackTimeout);
//         }

//         feedbackText.textContent = message;
//         feedbackIcon.className = isSuccess
//             ? 'fas fa-check-circle text-green-500 text-xl'
//             : 'fas fa-exclamation-circle text-red-500 text-xl';
//         feedbackElement.style.display = 'block';

//         feedbackTimeout = setTimeout(() => {
//             feedbackElement.style.display = 'none';
//             if (isSuccess) {
//                 window.location.href = '/auth/login';
//             }
//         }, duration);
//     }

//     // Modal de confirmação do voluntário
//     const modalHTML = `
//         <div id="volunteerModal" class="fixed inset-0 bg-base-600 bg-opacity-80 hidden flex items-center justify-center z-50">
//             <div class="bg-base-100 p-6 rounded-lg shadow-xl max-w-md w-full">
//                 <h3 class="text-lg font-bold mb-4">Termos do Voluntariado</h3>
//                 <div class="mb-4 text-sm text-base-600">
//                     <p>Ao se registrar como voluntário, você concorda em:</p>
//                     <ul class="list-disc pl-5 mt-2">
//                         <li>Dedicar tempo para ajudar outros membros da comunidade</li>
//                         <li>Seguir nosso código de conduta</li>
//                         <li>Participar de treinamentos quando necessário</li>
//                         <li>Manter confidencialidade sobre informações sensíveis</li>
//                     </ul>
//                 </div>
//                 <div class="flex justify-end space-x-3">
//                     <button id="cancelVolunteer" class="px-4 py-2 text-base-600 hover:bg-base-100 rounded">
//                         Cancelar
//                     </button>
//                     <button id="confirmVolunteer" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
//                         Aceito os Termos
//                     </button>
//                 </div>
//             </div>
//         </div>
//     `;
//     document.body.insertAdjacentHTML('beforeend', modalHTML);

//     const modal = document.getElementById('volunteerModal');
//     const confirmBtn = document.getElementById('confirmVolunteer');
//     const cancelBtn = document.getElementById('cancelVolunteer');

//     voluntarioCheckbox.addEventListener('change', function(e) {
//         if (this.checked) {
//             modal.classList.remove('hidden');
//         }
//     });

//     confirmBtn.addEventListener('click', function() {
//         modal.classList.add('hidden');
//         voluntarioCheckbox.checked = true;
//     });

//     cancelBtn.addEventListener('click', function() {
//         modal.classList.add('hidden');
//         voluntarioCheckbox.checked = false;
//     });

//     // Upload da imagem primeiro, então enviar o formulário
//     async function uploadImage(file) {
//         const imageFormData = new FormData();
//         imageFormData.append('file', file);

//         try {
//             const response = await fetch('/api/v1/uploads/profile-image', {
//                 method: 'POST',
//                 body: imageFormData
//             });

//             if (!response.ok) {
//                 throw new Error('Falha no upload da imagem');
//             }

//             const data = await response.json();
//             return data.url;
//         } catch (error) {
//             console.error('Erro no upload da imagem:', error);
//             throw error;
//         }
//     }

//     form.addEventListener('submit', async function(e) {
//         e.preventDefault();

//         const formData = new FormData(form);

//         try {
//             // Upload da imagem se existir
//             const imageFile = fileInput.files[0];
//             if (imageFile) {
//                 const imageUrl = await uploadImage(imageFile);
//                 formData.set('url_imagem_perfil', imageUrl);
//             }

//             // Handle checkboxes
//             const checkboxes = ['eh_voluntario', 'eh_gerente', 'deficiencia_auditiva',
//                                'usa_cadeira_rodas', 'deficiencia_cognitiva', 'lgbtq'];

//             checkboxes.forEach(checkbox => {
//                 if (!formData.has(checkbox)) {
//                     formData.set(checkbox, 'false');
//                 } else {
//                     formData.set(checkbox, 'true');
//                 }
//             });

//             // Validate password
//             const senha = formData.get('senha_hash');
//             const confirmarSenha = formData.get('confirmar_senha');

//             if (senha !== confirmarSenha) {
//                 showFeedback('As senhas não coincidem!', false);
//                 return;
//             }

//             // Remove confirmation password
//             formData.delete('confirmar_senha');

//             const response = await fetch('/api/v1/users/', {
//                 method: 'POST',
//                 body: formData
//             });

//             const data = await response.json();

//             if (response.ok) {
//                 showFeedback('Conta criada com sucesso! Redirecionando para o login...', true, 2000);
//             } else {
//                 let errorMessage = 'Erro ao criar conta. ';

//                 if (response.status === 409) {
//                     errorMessage += data.detail || 'Este usuário já existe.';
//                 } else if (response.status === 422) {
//                     errorMessage += 'Por favor, verifique os dados informados.';
//                 } else {
//                     errorMessage += data.detail || 'Tente novamente mais tarde.';
//                 }

//                 showFeedback(errorMessage, false, 5000);
//             }
//         } catch (error) {
//             console.error('Erro:', error);
//             showFeedback('Erro ao conectar com o servidor. Tente novamente.', false, 5000);
//         }
//     });

//     document.querySelector('#mensagem-feedback button').addEventListener('click', () => {
//         if (feedbackTimeout) {
//             clearTimeout(feedbackTimeout);
//         }
//         feedbackElement.style.display = 'none';
//     });
// });



document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('formRegistro');
    const feedbackElement = document.getElementById('mensagem-feedback');
    const feedbackText = document.getElementById('texto-feedback');
    const feedbackIcon = document.getElementById('icone-feedback');
    const voluntarioCheckbox = document.getElementById('eh_voluntario');
    let feedbackTimeout;


    const phoneInput = document.querySelector('input[name="telefone"]');

    if (phoneInput) {
        // Limpa configurações anteriores
        phoneInput.value = '';

        // Configura atributos básicos
        phoneInput.setAttribute('placeholder', '(99) 99999-9999');
        phoneInput.setAttribute('maxlength', '15');

        // Função simplificada para máscara
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value;

            // Remove tudo que não é número
            value = value.replace(/\D/g, '');

            // Aplica a máscara
            if (value.length <= 11) {
                value = value.replace(/(\d{2})(\d)/, '($1) $2');
                value = value.replace(/(\d)(\d{4})$/, '-$1$2');
            }

            e.target.value = value;
        });

        // Bloqueia teclas não numéricas
        phoneInput.addEventListener('keypress', function(e) {
            const char = String.fromCharCode(e.keyCode);

            // Se não for número, previne a digitação
            if (!/[0-9]/.test(char)) {
                e.preventDefault();
                return false;
            }
        });

        // Previne colar conteúdo não numérico
        phoneInput.addEventListener('paste', function(e) {
            e.preventDefault();
            let pastedText = (e.clipboardData || window.clipboardData).getData('text');
            pastedText = pastedText.replace(/\D/g, '');

            if (pastedText) {
                let value = this.value + pastedText;
                value = value.replace(/\D/g, '');

                if (value.length <= 11) {
                    value = value.replace(/(\d{2})(\d)/, '($1) $2');
                    value = value.replace(/(\d)(\d{4})$/, '-$1$2');
                }

                this.value = value;
            }
        });
    }

    // Substituir o input de URL por um container de imagem personalizado
    const imageInputContainer = document.querySelector('div.relative:has(input[name="url_imagem_perfil"])');
    const imageInput = document.querySelector('input[name="url_imagem_perfil"]');

    // Configurar o preview da imagem
    const previewImage = document.getElementById('preview-image');
    const defaultImage = document.getElementById('default-image');
    const fileInput = document.getElementById('profile-image-input');
    const imageContainer = document.querySelector('.group');

    imageContainer.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                previewImage.classList.remove('hidden');
                defaultImage.classList.add('hidden');
            };
            reader.readAsDataURL(file);
        }
    });

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
                window.location.href = '/auth/login';
            }
        }, duration);
    }

    // Modal de confirmação do voluntário
    const modalHTML = `
        <div id="volunteerModal" class="fixed inset-0 bg-base-600 bg-opacity-80 hidden flex items-center justify-center z-50">
            <div class="bg-base-100 p-6 rounded-lg shadow-xl max-w-md w-full">
                <h3 class="text-lg font-bold mb-4">Termos do Voluntariado</h3>
                <div class="mb-4 text-sm text-base-600">
                    <p>Ao se registrar como voluntário, você concorda em:</p>
                    <ul class="list-disc pl-5 mt-2">
                        <li>Dedicar tempo para ajudar outros membros da comunidade</li>
                        <li>Seguir nosso código de conduta</li>
                        <li>Participar de treinamentos quando necessário</li>
                        <li>Manter confidencialidade sobre informações sensíveis</li>
                    </ul>
                </div>
                <div class="flex justify-end space-x-3">
                    <button id="cancelVolunteer" class="px-4 py-2 text-base-600 hover:bg-base-100 rounded">
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

    // Upload da imagem primeiro, então enviar o formulário
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

        try {
            // Upload da imagem se existir
            const imageFile = fileInput.files[0];
            if (imageFile) {
                const imageUrl = await uploadImage(imageFile);
                formData.set('url_imagem_perfil', imageUrl);
            }

            // Handle checkboxes
            const checkboxes = ['eh_voluntario', 'eh_gerente', 'deficiencia_auditiva',
                               'usa_cadeira_rodas', 'deficiencia_cognitiva', 'lgbtq'];

            checkboxes.forEach(checkbox => {
                if (!formData.has(checkbox)) {
                    formData.set(checkbox, 'false');
                } else {
                    formData.set(checkbox, 'true');
                }
            });

            // Validate password
            const senha = formData.get('senha_hash');
            const confirmarSenha = formData.get('confirmar_senha');

            if (senha !== confirmarSenha) {
                showFeedback('As senhas não coincidem!', false);
                return;
            }

            // Remove confirmation password
            formData.delete('confirmar_senha');

            const response = await fetch('/api/v1/users/', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                showFeedback('Conta criada com sucesso! Redirecionando para o login...', true, 2000);
            } else {
                let errorMessage = 'Erro ao criar conta. ';

                if (response.status === 409) {
                    errorMessage += data.detail || 'Este usuário já existe.';
                } else if (response.status === 422) {
                    errorMessage += 'Por favor, verifique os dados informados.';
                } else {
                    errorMessage += data.detail || 'Tente novamente mais tarde.';
                }

                showFeedback(errorMessage, false, 5000);
            }
        } catch (error) {
            console.error('Erro:', error);
            showFeedback('Erro ao conectar com o servidor. Tente novamente.', false, 5000);
        }
    });

    document.querySelector('#mensagem-feedback button').addEventListener('click', () => {
        if (feedbackTimeout) {
            clearTimeout(feedbackTimeout);
        }
        feedbackElement.style.display = 'none';
    });
});


