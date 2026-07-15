# 🎯 Goal Tracer

## 💡 Ideia geral do projeto

A ideia do projeto é criar um sistema que permita ao usuário planejar sua rotina e ter um controle do tempo gasto em cada atividade. A principal utilidade do projeto é permitir que os usuários tomem ciência dos tempos gastos em cada atividade e consigam ajustá-las de acordo com suas metas.

Dessa forma, espera-se que ao final do projeto:

- [x] O usuário consiga registrar suas atividades para o dia ou semana
- [x] O usuário consiga marcar as atividades como feitas
- [x] O usuário consiga depositar uma quantidade de horas empreendidas em uma atividade
- [x] O usuário consiga estabelecer metas para a semana (em horas ou atividades)
- [x] O sistema calcule automaticamente o somatório de todas as horas empreendidas em cada atividade da meta
- [x] O sistema mostre se a meta para a semana foi atingida ou não

---

## 📋 Descrição geral do sistema

O **Goal Tracer** é um sistema web de acompanhamento de rotina e metas pessoais. Após o login, o usuário pode cadastrar atividades e vinculá-las a dias específicos da semana, registrando quantas horas dedicou a cada uma.

### ✨ O sistema oferece:

| Funcionalidade | Descrição |
|---|---|
| 📅 **Tela "Hoje"** | Exibe as atividades planejadas para o dia atual, permitindo registrar as horas cumpridas e visualizar o percentual de progresso em relação à meta diária |
| 🎯 **Gestão de metas semanais** | O usuário define metas de horas por atividade; o sistema divide automaticamente a meta entre os dias em que a atividade está cadastrada e calcula o progresso individual e geral |
| 🗓️ **Calendário** | Integração com FullCalendar para visualização das atividades ao longo do mês |
| 📊 **Relatórios** | Página que mostra o andamento das metas e exibe um gráfico com as horas realizadas durante a semana, dia a dia |
| ⚙️ **Painel administrativo** | Interface Django Admin para gestão direta dos dados (atividades, vínculos diários e metas) |

> Dessa forma, o sistema permite que o usuário tenha visibilidade clara de quanto tempo está investindo em cada área de sua rotina e o quão perto está de atingir seus objetivos semanais.

---

## 👥 Integrantes

- Cristiano Augusto Dias Mafuz
- Victor Emmanuel Susko Guimarães

## 🗂️ Quadro Kanban

🔗 [Ver quadro no GitHub Projects](https://github.com/users/VSusko/projects/1/views/1)

---

## 🛠️ Tecnologias

- 🐍 **Backend:** Django (Python)
- 🎨 **Frontend:** HTML, Tailwind CSS, JavaScript vanilla (com FullCalendar para o calendário)
- 🗃️ **Banco de dados:** SQLite
- 🐳 **Infraestrutura:** Docker e Docker Compose

---

## 🚀 Instruções para execução da aplicação

### ✅ Pré-requisitos

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) instalados

### 📖 Passo a passo

**1. Clone o repositório:**
```bash
git clone https://github.com/VSusko/Goal-Tracer.git
cd Goal-Tracer
```

**2. Suba os containers:**
```bash
docker compose up -d --build
```
ou
```bash
make
```

**3. Rode as migrações do banco de dados:**
```bash
docker compose exec web python manage.py migrate
```
ou
```bash
make migrate
```

**4. Crie um superusuário para acessar o painel administrativo:**
```bash
docker compose exec web python manage.py createsuperuser
```

**5. Acesse a aplicação no navegador:**

🌐 http://localhost:8000

**6. (Opcional) Acesse o painel administrativo:**

🔐 http://localhost:8000/admin

### 🛑 Parar a aplicação

```bash
docker compose down
```
ou
```bash
make leave
```

## 📘 Manual do sistema

### 1. 🔑 Faça login

Acesse `http://localhost:8000` e entre com seu usuário e senha. Caso ainda não tenha uma conta, cadastre-se pela tela de registro.

### 2. ➕ Cadastre suas atividades

No menu, acesse a área de **Atividades** e crie uma nova atividade (ex: "Estudar", "Academia", "Ler"). Ao cadastrar, você vincula a atividade aos dias da semana em que pretende realizá-la na área de **Semana**.

### 3. 🎯 Defina suas metas

Na área de **Metas**, escolha uma atividade já cadastrada e defina quantas horas semanais você deseja dedicar a ela. Alternativamente, é possivel adicionar a meta assim que a atividade é vinculada a um dia da semana. Vale ressaltar que uma meta não pode ser adicionada duas vezes a uma atividade.

### 4. ✅ Acompanhe o dia a dia

Na tela **Hoje**, você verá todas as atividades planejadas para o dia atual. Para cada uma:
- É possível digitar quantas horas você já dedicou no campo correspondente
- Clique em **Salvar**
- A barra de progresso é atualizada automaticamente, mostrando o quanto da meta diária foi cumprido

Quando o percentual atinge 100%, a atividade é marcada como **concluída**, mostrando círculo verde ao lado da atividade.

### 5. 🗓️ Visualize no calendário

Acesse a tela de **Calendário** para ver todas as suas atividades organizadas ao longo do mês, com o FullCalendar.

### 6. 📊 Consulte os relatórios

Na tela de **Relatórios**, acompanhe o progresso geral das suas metas e visualize um gráfico com as horas realizadas em cada dia da semana, comparando o planejado com o executado.

### 7. ⚙️ (Opcional) Gerencie os dados pelo admin

Se precisar editar, corrigir ou remover dados diretamente, acesse o painel administrativo em `http://localhost:8000/admin` com um usuário superusuário.

---