 document.addEventListener("DOMContentLoaded", function () {
    const formLogin = document.getElementById("formLogin");
    const feedbackElement = document.getElementById("mensagem-feedback");
    const feedbackText = document.getElementById("texto-feedback");
    const feedbackIcon = document.getElementById("icone-feedback");
    let feedbackTimeout;

    formLogin.addEventListener("submit", async function (e) {
      e.preventDefault(); // Evita o envio padrão do formulário

      const formData = new FormData(formLogin);

      try {
        const response = await fetch("/auth/login", {
          method: "POST",
          body: formData,
          headers: {
            Accept: "application/json", // Adiciona o cabeçalho para esperar uma resposta JSON
          },
        });

        // Se a resposta não for ok, tentamos extrair o JSON de erro
        const data = await response.json();

        if (response.ok) {
          // Exibe feedback de sucesso
          showFeedback(
            "Login realizado com sucesso! Redirecionando...",
            true,
            2000
          );
          // Após o feedback rediciona para a página inicial após alguns segundos
          setTimeout(() => {
            window.location.href = "/home"; // Altere conforme necessário
          }, 1500);
        } else {
          let errorMessage = "Erro ao fazer login. ";
          if (response.status === 401) {
            errorMessage += "Credenciais inválidas.";
          } else {
            // Aqui usamos o `data.message` para exibir a mensagem de erro
            errorMessage += data.message || "Tente novamente mais tarde.";
          }
          showFeedback(errorMessage, false, 5000);
        }
      } catch (error) {
        console.error("Erro:", error);
        showFeedback(
          "Erro ao conectar com o servidor. Tente novamente.",
          false,
          5000
        );
      }
    });

    function showFeedback(message, isSuccess = true, duration = 5000) {
      if (feedbackTimeout) {
        clearTimeout(feedbackTimeout);
      }

      feedbackText.textContent = message;
      feedbackIcon.className = isSuccess
        ? "fas fa-check-circle text-green-500 text-xl"
        : "fas fa-exclamation-circle text-red-500 text-xl";
      feedbackElement.style.display = "block";

      feedbackTimeout = setTimeout(() => {
        feedbackElement.style.display = "none";
        if (isSuccess) {
          // Redireciona após o feedback de sucesso
          window.location.href = "/home"; // Altere conforme necessário
        }
      }, duration);
    }
  });
