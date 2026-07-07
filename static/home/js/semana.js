// Funcao para formatar horas
window.fmtHoras = (valor) =>
    Number(valor).toLocaleString('pt-BR', {
        minimumFractionDigits: 1,
        maximumFractionDigits: 1,
    }) + 'h';

window.fmtNumero = (valor) =>
    Number(valor).toLocaleString('pt-BR', {
        minimumFractionDigits: 1,
        maximumFractionDigits: 1,
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

// Botao nova atividade
const botaoNovaAtividade = document.getElementById("botao_nova_atividade");
const caixa_nova_atividade = document.getElementById("caixa_nova_atividade");
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
botaoAdicionar.addEventListener("click", async() => {
    // Lógica para adicionar a atividade
    console.log(csrftoken);
    const nome_atividade = document.getElementById("caixa_atividades").value;
    const dia_semana = document.getElementById("caixa_dia_semana").value;
    const horas_feitas = document.getElementById("caixa_horas").value;
 
    const response = await fetch("/atividade/associar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            nome_atividade: nome_atividade,
            dia_semana: dia_semana,
            horas_feitas: horas_feitas
        })
    });

    const data = await response.json();
    
    if (response.status != 200){
        if(data["erro"].includes("UNIQUE constraint failed")){
            alert("Erro: a atividade " + nome_atividade + " já está registrada na " + dia_semana);
        }
        else{
            alert("Erro: " + data["erro"]);
        }
        return;
    }

    
    // Resetando as entradas
    document.getElementById("caixa_horas").value = "";

    // Adicionando a nova atividade na interface
    const container_body = document.getElementById("div_body_atividade_" + dia_semana);

    if (container_body.children[0] && container_body.children[0].tagName === "P") {
        container_body.children[0].remove();
    }

    // Criando a nova div    
    const novaAtividade = document.createRange().createContextualFragment(`
        <div class="flex items-center gap-3 bg-gray-50 border-gray-300 border-2 rounded-lg p-3 mb-2" id="div_atividade_${data.id}">
            <p>${nome_atividade}</p>
            <!-- Progresso feito -->
            <div class="flex justify-end items-center gap-1 ml-auto">
                <input type="number" id="${data.id}" value="${horas_feitas}" min="0" max="24" step="0.5" class="ml-auto border-2 rounded-lg bg-gray-50 p-1">
                <p>h</p>
                <!-- Botao deletar  -->
                <div id="botao_deletar_${data.id}" class="hover:scale-110 duration-200 ease-in-out bg-red-500 text-white rounded-lg px-3 pt-1 ml-3">
                    <input type="image" src="${TRASH_ICON}" alt="Lixeira" class="w-7 h-6"/>
                </div>
            </div>
        </div>
    `);
    // Adicionando a div no html
    container_body.appendChild(novaAtividade);   
    
    // Incrementando horas trabalhadas
    const elem_total_horas = document.getElementById("total_horas_" + dia_semana);
    elem_total_horas.innerText = "Total: " + fmtHoras(data.soma_diaria);

    // Atualizando o percentual da meta...
    if(data.id_meta != "None")
    {
        const percentual_antigo = document.getElementById("percentual_meta_" + data.id_meta); 
        // Cria a nova div (pode ser um elemento HTML criado via código)
        const percentual_novo = document.createElement("div");
        percentual_novo.id = "percentual_meta_" + data.id_meta;
        percentual_novo.className = `bg-green-500 h-2 rounded-full w-[${data.percentual}%]`; 
        percentual_antigo.replaceWith(percentual_novo);
        
        // Atualizando as horas totais trabalhadas na meta
        const horas_antigas = document.getElementById("horas_meta_" + data.id_meta); 
        const horas_novas = document.createElement("span");
        horas_novas.id = "horas_meta_" + data.id_meta;
        horas_novas.className = `text-gray-500 ml-auto`;
        horas_novas.textContent = fmtHoras(data.horas_da_meta);
        horas_antigas.replaceWith(horas_novas);
    }
});

// Botao deletar atividade
document.addEventListener("click", async (event) => {
    const botao = event.target.closest("[id^='botao_deletar_']");
    
    if (!botao) return; // clique não foi num botão deletar
    
    const vinculo_id = botao.id.split("_").pop();
    console.log("Deletar atividade com ID:", vinculo_id);

    const response = await fetch("/atividade/associar/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            vinculo_id: vinculo_id
        })
    });

    if (response.status != 200){
        alert("Erro: " + data["erro"]);
        return;
    }

    const data = await response.json();

    // Remover a atividade da interface
    const atividadeDiv = document.getElementById(`div_atividade_${vinculo_id}`);
    if (atividadeDiv) {
        atividadeDiv.remove();
    }

    // Colocar mensagem de vazio
    const container = document.getElementById("div_body_atividade_" + data.dia);
    if (container.children.length === 0) {
        const mensagem = document.createElement("p");
        mensagem.innerHTML = `<p class="text-gray-500">Nenhuma atividade planejada.</p>`;
        container.appendChild(mensagem);
    }

    // Decrementando horas trabalhadas
    const elem_total_horas = document.getElementById("total_horas_" + data.dia);
    elem_total_horas.innerText = "Total: " + fmtHoras(data.soma_diaria);
    
    console.log(data.dia)
    console.log(data.id_meta)
    console.log(data.soma_diaria)
    console.log(data.horas_da_meta)
    console.log(data.percentual)

    // Atualizando o card da meta (apenas se ela existir)
    if(data.id_meta != "None")
    {
        // Atualizando o percentual da meta...
        const percentual_antigo = document.getElementById("percentual_meta_" + data.id_meta); 
        // Cria a nova div (pode ser um elemento HTML criado via código)
        const percentual_novo = document.createElement("div");
        percentual_novo.id = "percentual_meta_" + data.id_meta;
        percentual_novo.className = `bg-green-500 h-2 rounded-full w-[${data.percentual}%]`; 
        percentual_antigo.replaceWith(percentual_novo);
        
        // Atualizando as horas totais trabalhadas na meta
        const horas_antigas = document.getElementById("horas_meta_" + data.id_meta); 
        const horas_novas = document.createElement("span");
        horas_novas.id = "horas_meta_" + data.id_meta;
        horas_novas.className = `text-gray-500 ml-auto`;
        horas_novas.textContent = fmtHoras(data.horas_da_meta);
        horas_antigas.replaceWith(horas_novas);
    }
    
});