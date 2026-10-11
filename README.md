# 🛡️ EPI Flow — Sistema de Gestão de EPIs

Projeto acadêmico de sistema para gerenciamento e empréstimo de Equipamentos de Proteção Individual (EPIs), desenvolvido em Python e Django.

---

## 🚀 Funcionalidades Implementadas (Módulo Colaboradores)

- **Cadastro de Colaboradores:** Formulário completo com validação de campos obrigatórios e feedback visual (Bootstrap Alerts).
- **Permanência de Tela:** Após o cadastro com sucesso, o sistema permanece na tela de cadastro pronto para um novo registro.
- **Validações Avançadas:**
  - Verificação de algoritmo matemático e unicidade de CPF.
  - Matrícula com padrão obrigatório iniciado em `F` + 5 dígitos (ex: `F12345`).
  - Máscaras de digitação em tempo real para CPF, Telefone e Matrícula.
- **Listagem Dinâmica & Busca:** Tabela responsiva com busca integrada por **Nome**, **CPF** ou início de **Matrícula**.
- **Edição Cadastral:** Formulário pré-carregado com os dados do colaborador existente para atualização.
- **Inativação Lógica:** Alternância de status (*Ativo* / *Inativo*) preservando o histórico para auditoria e conformidade com a NR-06.
- **Exclusão Segura:** Modal de confirmação do Bootstrap antes de remover registros definitivamente via requisição POST.
- **Interface Moderna:** Sidebar vertical de navegação e componentes estilizados com Bootstrap 5.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.13+
- **Framework Web:** Django 6.1+
- **Banco de Dados:** SQLite3 (nativo de desenvolvimento)
- **Frontend:** HTML5, CSS3, JavaScript e Bootstrap 5

---

## 📋 Como Executar o Projeto Localmente

Siga o passo a passo abaixo para rodar o projeto em sua máquina:

### 1. Clonar o Repositório
```bash
git clone https://github.com/carvalhojonathan/epiflow.git
cd epiflow
```

### 2. Criar e Ativar o Ambiente Virtual (`.venv`)

**No Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**No Windows (Prompt de Comando / CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**No Linux ou macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as Dependências
Com o ambiente virtual ativado:
```bash
pip install -r requirements.txt
```

### 4. Executar as Migrações do Banco de Dados
Crie as tabelas do banco SQLite executando:
```bash
python manage.py migrate
```

### 5. Iniciar o Servidor de Desenvolvimento
```bash
python manage.py runserver
```

Agora acesse no seu navegador:
- 🏠 **Página Inicial:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 👥 **Módulo Colaboradores:** [http://127.0.0.1:8000/colaboradores/](http://127.0.0.1:8000/colaboradores/)
