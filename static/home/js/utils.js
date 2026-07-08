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

if (!window.getCookie) {
    window.getCookie = function(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    };
}

// 2. Blindando o csrftoken no escopo global
if (!window.csrftoken) {
    window.csrftoken = window.getCookie("csrftoken");
}