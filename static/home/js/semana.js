// Paleta de cores (pares de classes Tailwind pra gradiente)
const CORES_ATIVIDADE = [
    ["from-red-300", "to-red-400"],
    ["from-orange-300", "to-orange-400"],
    ["from-amber-300", "to-amber-400"],
    ["from-yellow-300", "to-yellow-400"],
    ["from-lime-300", "to-lime-400"],
    ["from-green-300", "to-green-400"],
    ["from-emerald-300", "to-emerald-400"],
    ["from-teal-300", "to-teal-400"],
    ["from-cyan-300", "to-cyan-400"],
    ["from-sky-300", "to-sky-400"],
    ["from-blue-300", "to-blue-400"],
    ["from-indigo-300", "to-indigo-400"],
    ["from-violet-300", "to-violet-400"],
    ["from-purple-300", "to-purple-400"],
    ["from-fuchsia-300", "to-fuchsia-400"],
    ["from-pink-300", "to-pink-400"],
    ["from-rose-300", "to-rose-400"],
];

// Hash simples e determinístico a partir do nome da atividade
function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = (hash * 31 + str.charCodeAt(i)) >>> 0; // >>> 0 mantém unsigned
    }
    return hash;
}

function corAtividade(nome) {
    const indice = hashString(nome) % CORES_ATIVIDADE.length;
    return CORES_ATIVIDADE[indice]; // retorna [from, to]
}

// Aplica a cor em todos os cards de meta existentes na página
function aplicarCoresMetas() {
    document.querySelectorAll("[data-atividade]").forEach((card) => {
        const nome = card.dataset.atividade;
        const [de, para] = corAtividade(nome);
        card.classList.add(de, para);
    });
}

document.addEventListener("DOMContentLoaded", aplicarCoresMetas);

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


// Funções utilitárias para atualizar os cards de meta e total de horas
function atualizarCardMeta(id_meta, percentual, horas_da_meta) {
    if (id_meta === "None") return;

    // Atualiza barra de percentual
    const percentual_antigo = document.getElementById("percentual_meta_" + id_meta);
    const percentual_novo = document.createElement("div");
    percentual_novo.id = "percentual_meta_" + id_meta;
    percentual_novo.className = `bg-green-500 h-2 rounded-full w-[${percentual}%]`;
    percentual_antigo.replaceWith(percentual_novo);

    // Atualiza horas trabalhadas
    const horas_antigas = document.getElementById("horas_meta_" + id_meta);
    const horas_novas = document.createElement("span");
    horas_novas.id = "horas_meta_" + id_meta;
    horas_novas.className = "text-gray-500 ml-auto";
    horas_novas.textContent = fmtHoras(horas_da_meta);
    horas_antigas.replaceWith(horas_novas);
}

function atualizarTotalHoras(dia, soma_diaria) {
    const elem = document.getElementById("total_horas_" + dia);
    elem.innerText = "Total: " + fmtHoras(soma_diaria);
}



// Botao adicionar atividade
const botaoAdicionar = document.getElementById("botao_adicionar");
botaoAdicionar.addEventListener("click", async() => {
    // Lógica para adicionar a atividade
    console.log(csrftoken);
    const horas_feitas = document.getElementById("caixa_horas").value;

    if(horas_feitas === "" || isNaN(horas_feitas) || Number(horas_feitas) < 0 || Number(horas_feitas) > 24){
        alert("Erro: o valor de horas deve ser um número entre 0 e 24.");
        return;
    }

    const nome_atividade = document.getElementById("caixa_atividades").value;
    const dia_semana = document.getElementById("caixa_dia_semana").value;
    
    const response = await fetch("/atividade/associar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.csrftoken
        },
        body: JSON.stringify({
            nome_atividade: nome_atividade,
            dia_semana: dia_semana,
            horas_feitas: horas_feitas,
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
                <input type="number" data-vinculo="${data.id}" value="${horas_feitas}" min="0" max="24" step="0.5" class="ml-auto border-2 rounded-lg bg-gray-50 p-1">
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
    
    atualizarTotalHoras(dia_semana, data.soma_diaria);
    atualizarCardMeta(data.id_meta, data.percentual, data.horas_da_meta);
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
            "X-CSRFToken": window.csrftoken
        },
        body: JSON.stringify({
            vinculo_id: vinculo_id
        })
    });

    const data = await response.json();

    if (response.status != 200){
        alert("Erro: " + data["erro"]);
        return;
    }

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

    atualizarTotalHoras(data.dia, data.soma_diaria);
    atualizarCardMeta(data.id_meta, data.percentual, data.horas_da_meta);
});


// Objeto pra guardar os timers de cada input (já que tem vários na página)
const timers = {};

document.addEventListener("input", (event) => {
    const input = event.target;

    // Só executa se for um input de edição de horas
    if (!input.dataset.vinculo) return;

    const vinculo_id = input.dataset.vinculo;

    // Ignora inputs que nao sao de um vinculo real (ex: caixa_horas, caixa_meta_semanal)
    if (isNaN(Number(vinculo_id)) || vinculo_id === "") return;

    const novo_valor = input.value;

    // Cancela o timer anterior, se existir
    if (timers[vinculo_id]) {
        clearTimeout(timers[vinculo_id]);
    }

    // Cria um novo timer de 2 segundos
    timers[vinculo_id] = setTimeout(async () => {
        console.log(`Atualizando vínculo ${vinculo_id} para ${novo_valor}h`);

        try {
            const response = await fetch(`atividade/atualizar_horas/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"), // se usar proteção CSRF
                },
                body: JSON.stringify({
                    vinculo_id: vinculo_id,
                    horas_feitas: novo_valor
                })
            });

            const data = await response.json();
            console.log("Atualizado com sucesso:", data);
            atualizarTotalHoras(data.dia, data.soma_diaria);
            atualizarCardMeta(data.id_meta, data.percentual, data.horas_da_meta);

        } catch (error) {
            console.error("Erro ao atualizar horas:", error);
        }

    }, 2000); // 2000ms = 2 segundos
});