# 🚀 TaskAnalyzer — Sistema de Análise de Métricas e Produtividade

![CI Pipeline](https://github.com/JoaoCesarDev22/sdd-task-analyzer/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Docker](https://img.shields.io/badge/docker-containerized-brightgreen)
![Status](https://img.shields.io/badge/status-100%25%20passed-success)

> **Módulo avançado de métricas e produtividade desenvolvido para o Bootcamp III (DevOps, Testes Automatizados, Containerização e Governança Ética de IA).**

---

## 👤 Identificação do Autor

- **Nome Completo:** João César Netto Souza Castro
- **RA:** 22450460
- **Instituição / Polo:** UniCEUB — Asa Norte
- **Curso:** Análise e Desenvolvimento de Sistemas (ADS)
- **E-mail Institucional:** joao.cesar@sempreceub.com

---

## 🎯 Sobre o Projeto

O **TaskAnalyzer** é uma solução construída em **Python 3.11+** projetada para processar históricos de execução de tarefas corporativas. O sistema realiza cálculos de tempo médio de conclusão, identifica taxas percentuais de atraso em relação aos prazos limite e consolida indicadores segmentados por prioridade (`BAIXA`, `MEDIA`, `ALTA`).

O desenvolvimento seguiu rigorosamente o fluxo cumulativo em 3 fases:
1. **Fase 1 (Arquiteto de Especificações):** Elaboração do Contrato de Negócio (SDD) e especificação das regras de contexto (`CONTEXT_RULES.md`).
2. **Fase 2 (Piloto de IA & QA):** Geração assistida por IA, implementação da suíte BDD com `pytest` e fluxo colaborativo via Git/Pull Requests.
3. **Fase 3 (DevOps & Governança):** Esteira automatizada de CI/CD via GitHub Actions, containerização com Docker/Docker Compose e relatório ético de governança.

---

## 📂 Arquitetura do Repositório

```text
sdd-task-analyzer/
├── .github/
│   └── workflows/
│       └── ci.yml               # Pipeline de Integração Contínua (GitHub Actions)
├── specs/
│   └── requirements.yaml        # Especificação técnica dos requisitos e contrato SDD
├── src/
│   ├── __init__.py
│   └── task_analyzer.py         # Módulo principal com a classe TaskAnalyzer e regras de negócio
├── tests/
│   ├── __init__.py
│   └── test_harness.py          # Suíte de testes automatizados com pytest (Cenários 1, 2 e bordas)
├── .gitignore                   # Exclusão de arquivos temporários e caches
├── CONTEXT_RULES.md             # Regras de governança e restrições para IA
├── Dockerfile                   # Empacotamento da aplicação em imagem isolada (python:3.11-slim)
├── docker-compose.yml           # Orquestração para execução isolada dos testes via Docker
├── README.md                    # Documentação técnica e guia de execução
└── requirements.txt             # Dependências autorizadas do projeto (pytest>=8,<10)
⚙️ Como Executar o Projeto
1. Execução Local (Python 3.11+)
Clone o repositório:

Bash
git clone [https://github.com/JoaoCesarDev22/sdd-task-analyzer.git](https://github.com/JoaoCesarDev22/sdd-task-analyzer.git)
cd sdd-task-analyzer
Instale as dependências:

Bash
pip install -r requirements.txt
Execute a suíte de testes com o pytest:

Bash
pytest tests/test_harness.py -v
2. Execução via Docker (Containerização Isolada)
Garante que a suíte de testes rode em um ambiente idêntico, imutável e independente do sistema operacional local.

Usando Docker Compose (Recomendado):

Bash
docker compose run task-analyzer-tests
Usando Docker CLI diretamente:

Bash
docker build -t sdd-task-analyzer .
docker run --rm sdd-task-analyzer
🔄 Esteira CI/CD (GitHub Actions)
O repositório conta com um pipeline automatizado acionado a cada push ou pull_request nas branches main e develop:

Sistema Operacional: ubuntu-latest

Linguagem: Python 3.11

Verificação Automatizada: Instalação limpa de dependências e execução do comando pytest tests/test_harness.py -v.

🛡️ Governança Ética de IA e Modelo Critical-in-the-Loop
O código-fonte em src/task_analyzer.py foi construído com o apoio de assistentes virtuais de IA sob o estrito controle do arquivo CONTEXT_RULES.md:

Prevenção de Alucinações: Bloqueio de uso de bibliotecas externas não autorizadas e imposição do padrão ISO 8601 (YYYY-MM-DDTHH:MM:SS).

Validação Temporal: Disparo obrigatorio de InvalidTaskDataException em caso de incongruência cronológica (data_conclusao < data_criacao).

Tratamento de Borda: Mitigação de erro de divisão por zero na ausência de tarefas concluídas, garantindo o retorno de taxas zeradas (0.0) com emissão de log estruturado.