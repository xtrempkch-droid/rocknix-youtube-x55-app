import asyncio
import subprocess
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListItem, ListView, Label, Input
from textual.containers import Vertical

class YoutubeX55(App):
    TITLE = "YouTube TV - X55 Edition"
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("s", "focus_search", "Buscar"),
    ]

    # Interface otimizada para a tela 16:9 do X55
    CSS = """
    Screen { background: #0f0f0f; }
    Input { dock: top; margin: 1; border: tall $accent; height: 3; }
    ListView { width: 100%; height: 1fr; background: #121212; border: solid $primary; }
    ListItem { padding: 1 2; height: 3; border-bottom: thin #222; }
    ListItem:focus { background: $accent; color: white; text-style: bold; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Pesquise vídeos aqui...", id="search_box")
        yield Vertical(ListView(id="video_list"))
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        termo = event.value.strip()
        if termo:
            await self.buscar_videos(termo)

    async def buscar_videos(self, busca):
        lista = self.query_one("#video_list", ListView)
        lista.clear()
        
        # Busca otimizada (10 resultados para a tela maior do X55)
        cmd = ["yt-dlp", f"ytsearch10:{busca}", "--flat-playlist", "--print", "%(title)s|%(id)s"]

        try:
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE)
            stdout, _ = await proc.communicate()
            for line in stdout.decode().splitlines():
                if "|" in line:
                    titulo, video_id = line.split("|")
                    lista.append(ListItem(Label(f"▶ {titulo[:70]}"), id=f"vid_{video_id}"))
            lista.focus()
        except:
            self.notify("Erro na busca")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        video_id = event.item.id.replace("vid_", "")
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # OTIMIZAÇÃO X55: Resolução 720p com Aceleração de Hardware
        subprocess.run([
            "mpv", "--fs", "--vo=gpu", "--hwdec=auto",
            "--ytdl-format=best[height<=720]", 
            url
        ])

if __name__ == "__main__":
    YoutubeX55().run()
