# 🎮 Projeto Steam Game Tracker

## Descrição

Este projeto faz com que um banco de MySQLServer consuma a API da steam.

- Armazena dados básicos de cada jogo (nome, tempo de jogo, nota).  
- Atualiza automaticamente os jogos existentes e adiciona novos jogos com base na API da Steam.  
- Mantém um **log de atualizações**, registrando quantas linhas foram alteradas e se a execução foi bem-sucedida.  

---

## Estrutura do Banco de Dados

### Tabela `game`

Armazena os jogos e seus dados.

| Coluna             | Tipo           | Descrição |
|-------------------|---------------|-----------|
| `appid`           | INT (PK)      | Identificador único do jogo na Steam |
| `Steam_name`      | NVARCHAR(255) | Nome do jogo |
| `rating`          | TINYINT       | Nota pessoal de 0 a 10 |
| `playtime_forever`| INT           | Tempo total jogado (em minutos) |
| `rtime_last_played` | DATETIME     | Última vez que o jogo foi jogado |
| `img_url`         | NVARCHAR(255) | Hash da imagem do jogo (Steam) |

**Observações**:

- `rtime_last_played` da API vem em **epoch** (segundos desde 1970). Antes de inserir no SQL Server, deve ser convertido usando:

### Tabela `UpdatesLog`

Registra as execuções do script de atualização.

| Coluna        | Tipo                  | Descrição |
|--------------|-----------------------|-----------|
| `id`         | INT (PK, auto-increment) | Identificador único do log |
| `rows_updated` | INT                  | Quantidade de linhas atualizadas/inseridas |
| `date_run`   | DATETIME              | Data e hora da execução do script |
| `success`    | BIT                   | Status da execução (1 = sucesso, 0 = falha) |
