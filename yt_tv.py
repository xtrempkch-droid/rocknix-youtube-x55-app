import asyncio
import subprocess
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListItem, ListView, Label, Input, Static
from textual.containers import Vertical, Horizontal

class YouTubeTV(App):
    TITLE = "X55 Ultra-Light YouTube"
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("s", "focus_search", "Buscar"),
        ("backspace", "back_to_list", "Voltar")
    ]

    CSS = """
    #main_container { layout: grid; grid-size: 1; }
    ListView { width: 100%; height: 1fr; border: double $accent; }
    ListItem { padding: 1; margin: 0 1; background: $surface; }
    ListItem:focus { background: $accent 50%; border: tall $accent; }
    #search_box { margin: 1; border: round $primary; }
    .loading { content-align: center middle; color: $warning; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="🔍 Pesquisar vídeo...", id="search_box")
        yield Vertical(
            ListView(id="video_list"),
            id="main_container"
        )
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        termo = event.value.strip()
        if termo:
            await self.buscar_videos_otimizado(termo)

    async def buscar_videos_otimizado(self, busca):
        lista = self.query_one("#video_list", ListView)
        lista.clear()
        self.notify(f"Buscando: {busca}...", timeout=2)

        # Otimização: --flat-playlist extrai dados sem entrar em cada vídeo (MUITO mais rápido)
        # --print limpa o output para vir apenas Titulo + ID
        cmd = [
            "yt-dlp", 
            f"ytsearch10:{busca}", 
            "--flat-playlist", 
            "--print", "%(title)s|%(id)s"
        ]

        try:
            # Roda o comando em background para não congelar a TUI
            proc = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            
            for line in stdout.decode().splitlines():
                if "|" in line:
                    titulo, video_id = line.split("|")
                    item = ListItem(Label(f"📺 {titulo[:60]}..."), id=f"vid_{video_id}")
                    lista.append(item)
            
            lista.focus()
        except Exception as e:
            self.notify("Erro na busca!", severity="error")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        video_id = event.item.id.replace("vid_", "")
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Otimização X55: Chama o MPV configurado para Rockchip (DRM/GBM)
        # --ytdl-format="bestvideo[height<=720]+bestaudio" evita 4K que trava o chip
        subprocess.run([
            "mpv", 
            "--fs", 
            "--vo=gpu",      # Usa aceleração de GPU
            "--hwdec=auto",   # Tenta decodificação de hardware (RK3566)
            "--ytdl-format=best[height<=720]", # Limita a 720p para fluidez total
            url
        ])

if __name__ == "__main__":
    YouTubeTV().run()
