import sqlite3
import requests
import datetime
import json
import webbrowser
import os
import senhas 

STEAM_API_KEY = senhas.STEAM_API_KEY
STEAM_ID = senhas.STEAM_ID
DB_PATH = "steam_games.db"

def setup_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game (
            appid INTEGER PRIMARY KEY,
            steam_name TEXT,
            playtime_forever INTEGER,
            rtime_last_played TEXT
        )
    """)
    conn.commit()
    conn.close()

def update_games():
    print("⏳ Baixando dados da Steam...")
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={STEAM_ID}&include_appinfo=1&include_played_free_games=1&format=json"
    data = requests.get(url).json()
    games = data["response"].get("games", [])

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for g in games:
        appid = g["appid"]
        name = g["name"]
        playtime = g.get("playtime_forever", 0)
        last_played_unix = g.get("rtime_last_played")
        last_played = datetime.datetime.utcfromtimestamp(last_played_unix).date().isoformat() if last_played_unix else None

        cursor.execute("""
            INSERT INTO game (appid, steam_name, playtime_forever, rtime_last_played)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(appid) DO UPDATE SET
                steam_name=excluded.steam_name,
                playtime_forever=excluded.playtime_forever,
                rtime_last_played=excluded.rtime_last_played
        """, (appid, name, playtime, last_played))

    conn.commit()
    conn.close()
    print(f"✅ {len(games)} jogos atualizados no banco.")
    export_to_json()
    print("📁 Dados exportados para data.json")

def export_to_json():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT steam_name, playtime_forever, rtime_last_played FROM game")
    games = cursor.fetchall()
    conn.close()

    data = [
        {
            "steam_name": g[0],
            "playtime": g[1] // 60,
            "last_played": g[2] or "-"
        }
        for g in games
    ]

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_html():
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE.strip())

    webbrowser.open("index.html")
    print("🌐 Página aberta no navegador.")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Biblioteca Steam</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #121212;
      color: #eee;
      margin: 0;
      padding: 20px;
    }
    h1 { text-align: center; color: #61dafb; }
    .controls {
      display: flex;
      gap: 10px;
      justify-content: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }
    input, select, button {
      padding: 8px;
      border-radius: 6px;
      border: none;
      font-size: 14px;
    }
    button { background: #61dafb; cursor: pointer; }
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th, td {
      padding: 8px 12px;
      border-bottom: 1px solid #333;
      text-align: left;
    }
    tr:hover { background: #1e1e1e; }
  </style>
</head>
<body>
  <h1>Biblioteca Steam</h1>

  <div class="controls">
    <input id="search" type="text" placeholder="Buscar jogo...">
    <select id="sort">
      <option value="name">Ordem alfabética</option>
      <option value="most_played">Mais jogados</option>
      <option value="recent">Mais recentes</option>
    </select>
    <button id="refresh">🔁 Atualizar Dados</button>
  </div>

  <table id="games-table">
    <thead>
      <tr>
        <th>Nome</th>
        <th>Tempo jogado (h)</th>
        <th>Última vez jogado</th>
      </tr>
    </thead>
    <tbody id="table-body"></tbody>
  </table>

  <script>
    let games = [];

    async function loadGames() {
      try {
        const response = await fetch('data.json');
        if (!response.ok) throw new Error('Falha ao carregar JSON');
        games = await response.json();
      } catch (err) {
        alert('⚠️ Erro ao carregar data.json. Use um servidor local ou execute o Python novamente.');
        return;
      }
      renderTable(games);
    }

    function renderTable(list) {
      const tbody = document.getElementById('table-body');
      tbody.innerHTML = '';
      list.forEach(g => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${g.steam_name}</td>
          <td>${g.playtime}</td>
          <td>${g.last_played}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    function filterGames() {
      const search = document.getElementById('search').value.toLowerCase();
      const sort = document.getElementById('sort').value;
      let filtered = games.filter(g => g.steam_name.toLowerCase().includes(search));
      
      if (sort === 'most_played') {
        filtered.sort((a,b) => b.playtime - a.playtime);
      } else if (sort === 'recent') {
        filtered.sort((a,b) => new Date(b.last_played) - new Date(a.last_played));
      } else {
        filtered.sort((a,b) => a.steam_name.localeCompare(b.steam_name));
      }

      renderTable(filtered);
    }

    document.getElementById('search').addEventListener('input', filterGames);
    document.getElementById('sort').addEventListener('change', filterGames);
    document.getElementById('refresh').addEventListener('click', () => {
      alert("🔁 Para atualizar os dados, execute novamente o main.py");
    });

    loadGames();
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    setup_db()
    update_games()
    generate_html()
