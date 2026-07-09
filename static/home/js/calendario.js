// Cores por atividade (geradas automaticamente)
const CORES = [
    { bg: '#dbeafe', text: '#1d4ed8' }, // azul
    { bg: '#dcfce7', text: '#15803d' }, // verde
    { bg: '#fae8ff', text: '#7e22ce' }, // roxo
    { bg: '#ffedd5', text: '#c2410c' }, // laranja
    { bg: '#fce7f3', text: '#be185d' }, // rosa
    { bg: '#e0f2fe', text: '#0369a1' }, // azul claro
];

function corParaAtividade(nome) {
    let hash = 0;
    for (let i = 0; i < nome.length; i++) hash += nome.charCodeAt(i);
    return CORES[hash % CORES.length];
}

// Eventos mockados — substituir pelo fetch quando o banco tiver datas
const eventosMock = [
    { title: 'Estudar React', date: '2026-07-07', horas: 2 },
    { title: 'Exercícios',    date: '2026-07-07', horas: 1 },
    { title: 'Leitura',       date: '2026-07-09', horas: 1.5 },
    { title: 'Yoga',          date: '2026-07-10', horas: 1 },
    { title: 'Projeto',       date: '2026-07-14', horas: 3 },
];

const eventos = eventosMock.map(e => {
    const cor = corParaAtividade(e.title);
    return {
        title: e.title,
        date: e.date,
        extendedProps: { horas: e.horas },
        backgroundColor: cor.bg,
        textColor: cor.text,
    };
});

// Inicializa o FullCalendar
const calendarEl = document.getElementById('calendario');
const calendar = new FullCalendar.Calendar(calendarEl, {
    locale: 'pt-br',
    initialView: 'dayGridMonth',
    headerToolbar: {
        left: 'prev',
        center: 'title',
        right: 'next'
    },
    events: eventos,
    eventContent: (arg) => {
        return {
            html: `<span style="padding: 1px 6px; border-radius: 4px;">
                        ${arg.event.title}
                   </span>`
        };
    },
    dateClick: (info) => {
        window.location.href = `/dia/${info.dateStr}/`;
    },
    dayCellContent: (arg) => {
        const eventosNoDia = eventos.filter(e => e.date === arg.date.toISOString().split('T')[0]);
        const totalHoras = eventosNoDia.reduce((acc, e) => acc + e.extendedProps.horas, 0);
        return {
            html: `<div class="flex justify-between w-full px-1 pt-1">
                        <span class="text-sm text-gray-600">${arg.dayNumberText}</span>
                        ${totalHoras > 0 ? `<span class="text-xs text-blue-500 font-medium">${fmtHoras(totalHoras)}</span>` : ''}
                   </div>`
        };
    }
});

calendar.render();