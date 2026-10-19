# 🛡️ EPI Flow — Sistema de Gestão de EPIs

Sistema web para gestão e controle de entrega/empréstimo de Equipamentos de Proteção Individual (EPIs), desenvolvido em Python e Django.

---

## 🚀 Principais Módulos

- **👥 Colaboradores:** Cadastro com validação dos dados, busca inteligente e inativação/exclusão com modal de confirmação.
- **🪖 Equipamentos (EPIs):** Cadastro com número e validade de CA, estoque mínimo e busca inteligente.
- **📋 Controle de EPI:** Registro de empréstimos e fornecimentos com busca por colaborador e EPI, alerta visual de CA vencido e dados dinâmicos de baixa (devolvido, danificado, perdido).

---

## 📌 Status

- ⚠️ **Integração com Estoque:** O registro de empréstimos/fornecimentos ainda não realiza baixa automática no saldo de estoque dos equipamentos.
- 📊 **Relatórios e Autenticação:** As telas de relatórios gerenciais e login de usuários serão desenvolvidas em atualizações futuras.

---

## 🛠️ Tecnologias

Python 3.13 | Django 6.1 | SQLite3 | Bootstrap 5 | Tom Select

---

## 📋 Como Executar

```bash
# 1. Clone e acesse o repositório
git clone https://github.com/carvalhojonathan/epiflow.git
cd epiflow

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows (Linux/Mac: source .venv/bin/activate)

# 3. Instale dependências e aplique migrações
pip install -r requirements.txt
python manage.py migrate

# 4. Inicie o servidor
python manage.py runserver
```

Acesse: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
