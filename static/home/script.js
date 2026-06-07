const botaoNovaAtividade = document.getElementById("botao_nova_atividade");
const caixa_nova_atividade = document.getElementById("caixa_nova_atividade");

// Botao nova atividade
botaoNovaAtividade.addEventListener("click", () => {
    caixa_nova_atividade.classList.remove("hidden");
});

// Botao cancelar nova atividade
const botaoCancelar = document.getElementById("botao_adicionar_cancelar");

botaoCancelar.addEventListener("click", () => {
    caixa_nova_atividade.classList.add("hidden");
});

// Botao adicionar atividade
const botaoAdicionar = document.getElementById("botao_adicionar");

botaoAdicionar.addEventListener("click", () => {
    // Lógica para adicionar a atividade
    const nome = document.getElementById("caixa_nome").value;
    const dia = document.getElementById("caixa_dia_semana").value;
    const duracao = document.getElementById("caixa_horas").value;

    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            nome_atividade: nome,
            dia_semana: dia,
            duracao_minutos: duracao
        })
    });
});

// Função para obter o token CSRF do cookie
const csrftoken = getCookie("csrftoken");
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}