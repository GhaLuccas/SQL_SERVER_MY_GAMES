# 🎮 Projeto Steam Game Tracker

## 📘 Descrição

Este projeto consome a **API pública da Steam** e armazena os dados localmente em um banco **SQLite**.  
Ele gera automaticamente uma **interface HTML** para visualizar e filtrar os jogos.

- Sincroniza os dados da conta Steam.
- Atualiza automaticamente o banco de dados.
- Gera `data.json` e `index.html` com os dados prontos para visualização.

---

## 🧱 Estrutura do Banco de Dados

### Tabela `game`

| Coluna              | Tipo       | Descrição |
|---------------------|------------|-----------|
| `appid`             | INTEGER PK | ID do jogo na Steam |
| `steam_name`        | TEXT       | Nome do jogo |
| `playtime_forever`  | INTEGER    | Tempo jogado (minutos) |
| `rtime_last_played` | TEXT       | Última data jogada (YYYY-MM-DD) |

**Observação:**  
`rtime_last_played` é convertido de **epoch** (segundos desde 1970) para data legível antes de ser inserido no banco.

---

## 🔁 Fluxo de Atualização

1. Cria/valida o banco SQLite (`setup_db()`).
2. Consulta a API da Steam (`requests.get(...)`).
3. Atualiza ou insere jogos no banco (`INSERT ... ON CONFLICT DO UPDATE`).
4. Exporta tudo para `data.json`.
5. Gera `index.html` com busca e ordenação de jogos.

---

## 🌐 Interface Web

A interface usa **JavaScript puro** para carregar `data.json`, exibir os jogos e permitir filtros:

- Filtro de busca por nome  
- Ordenação por mais jogados, mais recentes ou alfabética  
- Exibição de tempo com “h” (ex: `200h`)  
- Datas no formato brasileiro (`31/04/2025`)

---

## 🚀 Execução

1. Adicione sua Steam API Key e ID no código Python.  
2. Rode:
   ```bash
   python main.py
   ```
3. Abra `index.html` ou use:
   ```bash
   python -m http.server
   ```
   e acesse **http://localhost:8000**

---

## 🧩 Tecnologias

| Camada | Tecnologia |
|--------|-------------|
| Banco  | SQLite |
| API    | Steam Web API |
| Backend | Python 3 |
| Frontend | HTML, CSS e JavaScript |
```
