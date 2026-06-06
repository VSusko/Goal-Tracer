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

