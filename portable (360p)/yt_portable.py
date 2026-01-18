import asyncio
import subprocess
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListItem, ListView, Label, Input
from textual.containers import Vertical

class YoutubePortable(App):
    """Um cliente YouTube leve para R36S e X55."""
    
    TITLE = "YT Portable"
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("s", "focus_search", "Busca"),
        ("enter", "select_cursor", "Selecionar"),
    ]

    # CSS Otimizado para telas pequenas (4:3 do R36S e 16:9 do X55)
    CSS = """
    Screen {
        background: #121212;
    }
    Input {
        dock: top;
        margin: 0;
        border: tall $accent;
        height: 3;
    }
    ListView {
        width: 100%;
        height: 1fr;
        background: #1a1a1a;
    }
    ListItem {
        padding: 0 1;
        height: 2; /* Altura fixa para caber mais itens em telas de 3.5" */
        border-bottom: thin #333;
    }
    ListItem:focus {
        background: $accent 40%;
        text-style: bold;
        color: white;
    }
    Label {
        font-size: 1; /* Fonte compacta para o R36S */
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Input(placeholder="🔍 Buscar...", id="search_box")
        yield Vertical(
            ListView(id="video_list"),
            id="main_container"
        )
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        termo = event.value.strip()
        if termo:
            await self.buscar_videos(termo)

    async def buscar_videos(self, busca):
        lista = self.query_one("#video_list", ListView)
        lista.clear()
        
        # Otimização extrema de busca para o processador do R36S
        cmd = [
            "yt-dlp", 
            f"ytsearch8:{busca}", # Reduzido para 8 resultados para carregar mais rápido
            "--flat-playlist", 
            "--print", "%(title)s|%(id)s"
        ]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            
            for line in stdout.decode().splitlines():
                if "|" in line:
                    titulo, video_id = line.split("|")
                    # Truncar título para não vazar da tela do R36S
                    display_title = (titulo[:35] + '..') if len(titulo) > 35 else titulo
                    item = ListItem(Label(f"• {display_title}"), id=f"vid_{video_id}")
                    lista.append(item)
            
            lista.focus()
        except Exception:
            self.notify("Erro na conexão", severity="error")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        video_id = event.item.id.replace("vid_", "")
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Comando MPV Otimizado para telas de 480p/720p
        # No R36S (ArkOS), o player precisa ser muito eficiente
        subprocess.run([
            "mpv", 
            "--fs", 
            "--vo=gpu", 
            "--hwdec=auto",
            "--ytdl-format=best[height<=480]", # 480p é o ideal para o R36S (economiza bateria e CPU)
            url
        ])

    def action_focus_search(self):
        self.query_one("#search_box").focus()

if __name__ == "__main__":
    YoutubePortable().run()
