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
            "X-CSRFToken": window.csrftoken
        },
        body: JSON.stringify({
            operacao:"create",
            nome_atividade: nome,
        })
    });

    // Coletando a resposta do servidor
    const data = await response.json();
    
    // Caso de erro
    if (response.status != 200){
        if(data["erro"].includes("UNIQUE constraint failed")){
            alert("Erro: uma atividade já foi cadastrada com esse nome.");
        }
        else{
            alert("Erro: " + data["erro"]);
        }
        return;
    }

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
            <!-- Div para deletar e editar -->
            <button id="botao_editar_${data.id}" type="submit" class="hover:scale-110 duration-200 ease-in-out ml-auto px-3 py-1 bg-yellow-500 text-white rounded-lg">Editar</button>
            <button id="botao_deletar_${data.id}" class="hover:scale-110 duration-200 ease-in-out bg-red-500 text-white rounded-lg px-3 py-1 ml-2">Deletar</button>
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
    
    const confirmar = confirm(`Tem certeza que deseja deletar essa atividade? Todas as metas associadas e atividades planejadas também serão removidas.`);
    if (!confirmar) {
        return; 
    }
    
    console.log("Deletar atividade com ID:", atividade_id);
    
    const response = await fetch("/atividade/gerenciar/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.csrftoken
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

const popUpEdicao = document.getElementById("popUpEdicao");
var nome_editavel = "";

// Botao editar atividade
document.addEventListener("click", async (event) => {
    const botao = event.target.closest("[id^='botao_editar_']");

    if (!botao) return; // clique não foi num botão editar
    
    // Abre o pop-up de edição
    popUpEdicao.classList.remove("hidden");
    
    const atividade_id = botao.id.split("_").pop();

    nome_editavel = document.getElementById(`atividade_${atividade_id}`).querySelector("p").textContent;

    const caixaEditar = document.getElementById("caixa_editar");
    caixaEditar.placeholder = nome_editavel;
});


// Fecha ao clicar em cancelar
document.getElementById("botao_cancelar").addEventListener("click", () => {
    const caixaEditar = document.getElementById("caixa_editar");
    caixaEditar.value = "";
    popUpEdicao.classList.add("hidden");
});


// Ação do confirmar
document.getElementById("botao_confirmar").addEventListener("click", async () => {
    
    const novo_nome = document.getElementById("caixa_editar").value;

    console.log("Editar atividade :", nome_editavel);
    
    const response = await fetch("/atividade/gerenciar/", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.csrftoken
        },
        body: JSON.stringify({
            atividade_nome: nome_editavel,
            novo_nome: novo_nome
        })
    });

    if (response.status != 200){
        alert("Erro ao editar atividade. Tente novamente.");
        return;
    }

    const data = await response.json();

    // Trocar o nome da atividade para o atualizado
    const atividadeDiv = document.getElementById(`atividade_${data.id}`);
    if (atividadeDiv) {
        atividadeDiv.querySelector("p").textContent = novo_nome;
    }
    
    const caixaEditar = document.getElementById("caixa_editar");
    caixaEditar.value = "";
    popUpEdicao.classList.add("hidden");
});