# 🛡️ EPI Flow — Sistema de Gestão de EPIs

Sistema corporativo para gerenciamento e empréstimo de Equipamentos de Proteção Individual (EPIs), desenvolvido em Python e Django.

---

## 🚀 Funcionalidades Implementadas (Módulo Colaboradores)

- **Cadastro de Colaboradores:** Formulário completo com validação de campos obrigatórios e feedback visual (Bootstrap Alerts).
- **Permanência de Tela:** Após o cadastro com sucesso, o sistema permanece na tela de cadastro pronto para novo registro.
- **Listagem Dinâmica:** Tabela com listagem de colaboradores e filtros de pesquisa por nome em tempo real.
- **Edição Cadastral:** Formulário pré-carregado com os dados do colaborador existente para atualização.
- **Inativação Lógica:** Alternância de status (Ativo / Inativo) para conformidade com a NR-06.
- **Exclusão Segura:** Modal de confirmação do Bootstrap antes de remover registros definitivamente.
- **Interface Moderna:** Sidebar vertical de navegação e componentes estilizados com Bootstrap 5.

pip install -r requirements.txt

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.13+
- **Framework Web:** Django
- **Banco de Dados:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript e Bootstrap 5

---

## 📋 Como Executar o Projeto Localmente

### 1. Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd epiflow
