
document.addEventListener("DOMContentLoaded", () => {
    // Pega os dados que o Django injetou nos scripts JSON
    const labelsElement = document.getElementById("grafico_labels");
    const dadosElement = document.getElementById("grafico_dados");

    if (!labelsElement || !dadosElement) return; // Evita erros se os elementos não existirem

    const labels = JSON.parse(labelsElement.textContent);
    const dados  = JSON.parse(dadosElement.textContent);

    // 2. Renderiza o gráfico
    new Chart(document.getElementById("grafico_horas"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Horas feitas",
                data: dados,
                backgroundColor: "rgba(0, 149, 255, 0.7)",
                borderColor: "rgb(0, 106, 106)",
                borderWidth: 2,
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => fmtHoras(ctx.raw)
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (val) => fmtHoras(val)
                    }
                }
            }
        }
    });
});