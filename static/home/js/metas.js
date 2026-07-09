// Botao adicionar atividade
const botaoAdicionar = document.getElementById("botao_adicionar");
botaoAdicionar.addEventListener("click", async() => {
    // Lógica para adicionar a atividade
    // Obtendo o nome
    const nome_atividade = document.getElementById("caixa_atividades").value;

    if (!nome_atividade) {
        alert("Todas as atividades possuem metas já definidas.");
        return;
    }

    const meta_horas = document.getElementById("caixa_meta").value;

    console.log("aaaaaaaaaa")

    const response = await fetch("/metas/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.csrftoken
        },
        body: JSON.stringify({
            operacao: "adicionar",
            nome_atividade: nome_atividade,
            meta_horas: meta_horas
        })
    });

    const data = await response.json();
    
    if (response.status != 200){
        alert("Erro " + data["erro"]);
        return;
    }
    
    // Resetando as entradas
    document.getElementById("caixa_meta").value = "";

    // Atualizando o painel de metas atingidas
    document.getElementById("metas_atingidas").textContent = data.metas_atingidas + "/" + data.total_metas;
    document.getElementById("progresso_medio").textContent = data.progresso_medio + "%";
    document.getElementById("status").textContent = data.status;

    // Atualizando as metas disponiveis para escolha
    const selectAtividades = document.getElementById("caixa_atividades");
    // Limpa todas as opções antigas
    selectAtividades.innerHTML = "";

    // Se não sobrou nenhuma atividade sem meta, deixa o select vazio
    if (data.atividades.length === 0) {
        const optionVazia = document.createElement("option");
        optionVazia.value = "";
        optionVazia.textContent = "";
        selectAtividades.appendChild(optionVazia);
    } else {
        // Preenche o select com as atividades que ainda não têm meta
        data.atividades.forEach(nome => {
            const option = document.createElement("option");
            option.value = nome;
            option.textContent = nome;
            selectAtividades.appendChild(option);
        });
    }

    // Adicionando a nova meta na interface
    const container_body = document.getElementById("div_metas");

    if (container_body.children[0] && container_body.children[0].tagName === "P") {
        container_body.children[0].remove();
    }

    // Criando a nova div    
    const novaMeta = document.createRange().createContextualFragment(`
        <div id="div_meta_${nome_atividade}" class="bg-white rounded-xl border border-gray-100 p-6 mt-4 shadow-lg">
            <div class="flex justify-between mb-3">
                <h4 class="font-semibold text-lg">${nome_atividade}</h4>	
                <div>${data.horas_semana}/${meta_horas}h</div>
            </div>

            <div class="w-full bg-gray-200 h-2 rounded-full">
                <div class="bg-blue-500 h-2 rounded-full w-[${data.percentual}%]"></div>
            </div>

            <p class="mt-2 text-sm text-gray-500">${data.percentual}% concluído</p>

            <div class="flex mt-4">
                <button id="botao_deletar_${nome_atividade}" type="submit" class="px-3 py-1 bg-red-500 text-white rounded">Deletar</button>
            </div>
        </div>
    `);
    // Adicionando a div no html
    container_body.appendChild(novaMeta);     
    
});


// Botao de deletar a meta
document.addEventListener("click", async (event) => {
        const botao = event.target.closest("[id^='botao_deletar_']");

        if (!botao) return; // clique não foi num botão deletar

        const nome_atividade = botao.id.split("_").pop();

        console.log("Deletar a meta da atividade " + nome_atividade);
        
        const response = await fetch("/metas/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": window.csrftoken
            },
            body: JSON.stringify({
                operacao: "deletar",
                nome_atividade: nome_atividade
            })
        });

        if (response.status != 200){
            alert("Erro: " + data["erro"]);
            return;
        }

        const data = await response.json();

        // Atualizando o painel de metas atingidas
        document.getElementById("metas_atingidas").textContent = data.metas_atingidas + "/" + data.total_metas;
        document.getElementById("progresso_medio").textContent = data.progresso_medio + "%";
        document.getElementById("status").textContent = data.status;

        // Atualizando as metas disponiveis para escolha
        const selectAtividades = document.getElementById("caixa_atividades");
        // Limpa todas as opções antigas
        selectAtividades.innerHTML = "";

        // Se não sobrou nenhuma atividade sem meta, deixa o select vazio
        if (data.atividades.length === 0) {
            const optionVazia = document.createElement("option");
            optionVazia.value = "";
            optionVazia.textContent = "";
            selectAtividades.appendChild(optionVazia);
        } else {
            // Preenche o select com as atividades que ainda não têm meta
            data.atividades.forEach(nome => {
                const option = document.createElement("option");
                option.value = nome;
                option.textContent = nome;
                selectAtividades.appendChild(option);
            });
        }

        // Remover a atividade da interface
        const atividadeDiv = document.getElementById(`div_meta_${nome_atividade}`);
        if (atividadeDiv) {
            atividadeDiv.remove();
        }

        // Colocar mensagem de vazio
        const container = document.getElementById("div_metas");
        if (container.children.length === 0) {
            const mensagem = document.createElement("p");
            mensagem.innerHTML = `<p class="text-gray-500">Nenhuma meta planejada.</p>`;
            container.appendChild(mensagem);
        }
});