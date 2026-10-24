# 🛡️ EPI Flow — Sistema de Gestão de EPIs

Sistema web para controle de entrega, empréstimo e conformidade de Equipamentos de Proteção Individual (EPIs), desenvolvido em Python e Django.

---

## 🚀 Principais Funcionalidades

- **👥 Colaboradores:** Gestão de funcionários com validação de CPF, busca inteligente, inativação e ordenação por colunas.
- **🪖 Equipamentos (EPIs):** Cadastro de EPIs com número de CA, data de validade, saldo em estoque e estoque mínimo. Alertas visuais automáticos para estoque crítico/esgotado e CA vencido.
- **📋 Controle de EPI (Empréstimos e Fornecimentos):**
  - **Integração com Estoque:** Baixa automática do saldo ao emprestar e retorno ao estoque ao registrar devolução.
  - **Ponto de Reposição:** Avisos de estoque mínimo para reposição sem interromper a proteção do colaborador.
  - **Validação de CA:** Bloqueio de novos empréstimos com CA vencido e alerta visual (`⚠️ CA Vencido`) caso o CA expire durante o uso.
- **📊 Relatório Gerencial & Exportação em PDF:**
  - Filtros cumulativos (AND) por Colaborador, Equipamento e Status com busca inteligente.
  - Exportação direta em PDF no padrão A4 paisagem.
- **↕️ Ordenação Dinâmica:** Ordenação em todas as tabelas do sistema, preservando as pesquisas ativas.

---

## 🛠️ Tecnologias

- **Backend:** Python 3.13 | Django 6.1 | SQLite3
- **Frontend:** Bootstrap 5 | Bootstrap Icons | FontAwesome
- **Bibliotecas:** Tom Select (busca inteligente em selects) | html2pdf.js (geração de PDF)

---

## 📋 Como Executar

```bash
# 1. Clone e acesse o repositório
git clone https://github.com/carvalhojonathan/epiflow.git
cd epiflow

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows (Linux/Mac: source .venv/bin/activate)

# 3. Instale as dependências e aplique as migrações
pip install -r requirements.txt
python manage.py migrate

# 4. Inicie o servidor
python manage.py runserver
```

Acesse: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
