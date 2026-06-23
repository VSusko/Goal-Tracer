# Documentação da Arquitetura do Sistema — Goal Tracer

Esta documentação detalha a organização estrutural, os componentes e o fluxo de comunicação do sistema **Goal Tracer**, servindo como guia técnico para o entendimento global da solução desenvolvida.

---

## 1. Visão Geral do Sistema
O **Goal Tracer** é uma plataforma projetada para o gerenciamento, monitoramento e rastreamento de metas pessoais ou organizacionais. O sistema adota o modelo clássico **Cliente-Servidor** executado de forma monolítica sob o padrão arquitetural **MVT (Model-View-Template)** nativo do framework Django.

A separação de responsabilidades foi projetada em três macro-camadas essenciais: Apresentação (Interface), Lógica de Negócios (Backend) e Persistência (Banco de Dados).

---

## 2. Componentes e Módulos do Sistema

O sistema é dividido em componentes específicos interconectados que segregam as funcionalidades da plataforma:

### 2.1. Camada de Apresentação (Frontend)
Responsável por toda a interface gráfica que coleta os comandos do usuário e exibe as informações processadas. É composta por:
* **HTML5:** Responsável pela estrutura semântica das telas e garantia de acessibilidade da plataforma.
* **CSS3 & Tailwind CSS:** Framework focado em classes utilitárias que elimina a necessidade de folhas de estilo infladas, agilizando o carregamento de páginas e entregando uma interface responsiva, fluida e moderna.

### 2.2. Camada de Lógica de Negócios (Backend)
O motor central do ecossistema, implementado em **Python** utilizando o ecossistema **Django**. Suas principais subdivisões internas englobam:
* **Roteador de URLs:** Captura as requisições enviadas pelo cliente e encaminha para a lógica de visualização correta.
* **Views (Visualizações):** Onde estão centralizadas as regras de negócio e validações lógicas (como o cálculo matemático do avanço de uma meta, prazos e controle de usuários).
* **Templates:** Estruturas dinâmicas em HTML que servem para acoplar os dados gerados em Python e enviá-los prontos para o navegador.

### 2.3. Camada de Persistência (Banco de Dados)
* **Banco de Dados Relacional:** Base estruturada encarregada pelo armazenamento íntegro das entidades (Contas de usuários, Metas cadastrados, Histórico de evolução).
* **Django ORM (Object-Relational Mapping):** Componente que abstrai as interações com o banco de dados. Em vez de escrever códigos SQL puros no backend, utiliza-se a própria sintaxe Python, protegendo nativamente o projeto contra vulnerabilidades críticas como *SQL Injection*.

---

## 3. Mecanismos de Comunicação entre Componentes

A troca de mensagens e dados entre as camadas segue o fluxo de ciclo de vida padrão de transações na Web:

1.  **Entrada do Usuário:** O usuário realiza uma ação na interface gráfica (ex: clica em "Adicionar Nova Meta").
2.  **Disparo HTTP:** O Frontend intercepta a ação e emite uma requisição através dos protocolos `HTTP/HTTPS` (utilizando os métodos semânticos adequados, como `GET` ou `POST`) em direção ao servidor Backend.
3.  **Processamento da Regra:** O roteador do Django recebe a chamada e aciona a `View` correspondente. A `View` processa os dados, se comunica com o Banco de Dados através do `Django ORM`, e recebe o retorno dos registros armazenados.
4.  **Montagem da Resposta (Renderização SSR):** O Django injeta esses dados dinâmicos no `Template` estruturado com o `Tailwind CSS`, gerando uma página HTML final estática.
5.  **Resposta ao Cliente:** O servidor devolve essa página pronta para o navegador do usuário que simplesmente renderiza a tela final estruturada.

---

## 4. Matriz de Tecnologias Utilizadas

A tabela abaixo consolida o papel estratégico de cada tecnologia integrada à arquitetura descrita no diagrama do projeto:

| Tecnologia / Ferramenta | Categoria | Função Prática no Projeto Goal Tracer |
| :--- | :--- | :--- |
| **Python** | Linguagem de Programação | Base tecnológica estável, legível e tipada dinamicamente responsável pelo código de backend. |
| **Django** | Framework Web (Backend) | Acelera o desenvolvimento fornecendo segurança embutida, mapeamento de banco de dados (ORM) e arquitetura estruturada. |
| **Tailwind CSS** | Framework de Estilização | Garante design responsivo e moderno por meio de classes utilitárias pré-definidas diretamente no HTML. |
| **HTML5 & CSS3** | Linguagens Web Base | Padrões universais que sustentam a interface e formatação visual expostas ao usuário final. |
| **Banco de Dados Relacional** | Persistência de Dados | Armazenamento seguro de todas as tabelas essenciais (Usuários, Metas, Progresso) assegurando transações confiáveis. |