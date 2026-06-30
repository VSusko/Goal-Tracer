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


// Botao adicionar atividade
const botaoAdicionar = document.getElementById("botao_adicionar");
botaoAdicionar.addEventListener("click", async() => {
    // Lógica para adicionar a atividade
    const nomeInput = document.getElementById("caixa_nome");
    const nome = nomeInput.value;
 
    const response = await fetch("/atividade/gerenciar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            operacao:"create",
            nome_atividade: nome,
        })
    });

    // Caso de erro
    if (response.status != 200){
        alert("Erro ao adicionar atividade. Tente novamente.");
        return;
    }

    // Coletando a resposta do servidor
    const data = await response.json();
    
    // Resetando as entradas
    nomeInput.value = "";

    // Adicionando a nova atividade na interface
    const container = document.getElementById("div_atividades");

    // Se tem a mensagem de vazio, remove
    if (container.children[0] && container.children[0].tagName === "P") {
        container.children[0].remove();
    }

    // Criando a nova div    
    const novaAtividade = document.createRange().createContextualFragment(`
        <div id="atividade_${data.id}" class="flex bg-gradient-to-r from-red-100 to-red-200 text-black rounded-lg pl-5 pr-4 py-4 w-[75vw] shadow-lg">
            <p class="text-lg">${nome}</p>
            <!-- Div para deletar -->
            <div id="botao_deletar_${data.id}" class="hover:scale-110 duration-200 ease-in-out bg-red-500 text-white rounded-lg px-3 py-1 ml-auto">
                <button>Deletar</button>
            </div>
        </div>
    `);
    // Adicionando a div nova na pagina
    container.appendChild(novaAtividade);   
    
});




// Botao deletar atividade
document.addEventListener("click", async (event) => {
    const botao = event.target.closest("[id^='botao_deletar_']");

    if (!botao) return; // clique não foi num botão deletar

    const atividade_id = botao.id.split("_").pop();

    console.log("Deletar atividade com ID:", atividade_id);
    
    const response = await fetch("/atividade/gerenciar/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            atividade_id: atividade_id
        })
    });

    if (response.status != 200){
        alert("Erro ao remover atividade. Tente novamente.");
        return;
    }

    const data = await response.json();

    // Remover a atividade da interface
    const atividadeDiv = document.getElementById(`atividade_${atividade_id}`);
    if (atividadeDiv) {
        atividadeDiv.remove();
    }

    // Colocar mensagem de vazio
    const container = document.getElementById("div_atividades");
    if (container.children.length === 0) {
        const mensagem = document.createElement("p");
        mensagem.innerHTML = `<p class="text-gray-500">Nenhuma atividade planejada.</p>`;
        container.appendChild(mensagem);
    }
});

