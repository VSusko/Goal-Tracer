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
        alert("Erro " + data["erro"]);
        return;
    }
    
    // Resetando as entradas
    document.getElementById("caixa_dia_semana").value = "Segunda";
    document.getElementById("caixa_horas").value = "0";


    // Adicionando a nova atividade na interface
    const container = document.getElementById("div_body_atividade_" + dia_semana);

    if (container.children[0] && container.children[0].tagName === "P") {
        container.children[0].remove();
    }

    // Criando a nova div    
    const novaAtividade = document.createElement("div");
    novaAtividade.innerHTML = `
        <div class="flex items-center gap-3 bg-gray-50 border-gray-300 border-2 rounded-lg p-3 mb-2">
            <p>${nome_atividade}</p>
            <!-- Progresso feito -->
            <div class="flex justify-end items-center gap-1 ml-auto">
                <input type="number" id="${data.id}" value="${horas_feitas}" min="0" max="1000" step="0.5" class="ml-auto border-2 rounded-lg bg-gray-50 p-1">
                <p class="text-gray-500">/5h</p>
                <div id="botao_deletar_${data.id}" class="hover:scale-110 duration-200 ease-in-out bg-red-500 text-white rounded-lg px-3 pt-1 ml-10">
                    <input type="image" src="${TRASH_ICON}" alt="Lixeira" class="w-7 h-6"/>
                </div>
                <!-- Adicionar barra de progresso... -->
            </div>
        </div>
    `;

    container.appendChild(novaAtividade);   
    
});


// Botao deletar atividade
const botoesDeletar = document.querySelectorAll("[id^=botao_deletar_]");
botoesDeletar.forEach(botao => {
    botao.addEventListener("click", async () => {

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
        const atividadeDiv = document.getElementById(`div_atividade_${atividade_id}`);
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
    });
});



// Definindo que chama a funcao quando carrega a pagina
// document.addEventListener("DOMContentLoaded", async () => {
//     const dias = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"];

//     for (const dia of dias) {
//         const response = await fetch("/atividade/soma_horas/", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//                 "X-CSRFToken": csrftoken
//             },
//             body: JSON.stringify({
//                 dia_semana: dia,
//             })
//         });

//         const data = await response.json();

//         document.getElementById("horas-trabalhadas").textContent = `Horas Trabalhadas: ${data.soma}`;
//     }
// });  