from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListItem, ListView, Label, Input
from textual.containers import Container
import subprocess
import os

class YouTubeTV(App):
    TITLE = "X55 YouTube TV"
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("s", "focus_search", "Buscar"),
    ]

    CSS = """
    ListView {
        width: 100%;
        height: 1fr;
        border: solid $accent;
        background: $surface;
    }
    ListItem {
        padding: 1;
    }
    ListItem:focus {
        background: $accent;
        color: white;
        text-style: bold;
    }
    #search_box {
        dock: top;
        margin: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Digite sua busca...", id="search_box")
        yield ListView(id="video_list")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Quando você digita e aperta Enter na busca"""
        termo = event.value
        self.buscar_videos(termo)

    def buscar_videos(self, busca):
        lista = self.query_one("#video_list", ListView)
        lista.clear()
        
        # Busca os títulos e IDs usando yt-dlp (limite de 10 para ser rápido)
        cmd = f'yt-dlp "ytsearch10:{busca}" --get-title --get-id'
        try:
            output = subprocess.check_output(cmd, shell=True).decode("utf-8").splitlines()
            # O output vem em pares: Titulo \n ID
            for i in range(0, len(output), 2):
                titulo = output[i]
                video_id = output[i+1]
                item = ListItem(Label(f"▶ {titulo}"), id=f"vid_{video_id}")
                lista.append(item)
            lista.focus()
        except Exception as e:
            lista.append(ListItem(Label("Erro na busca!")))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Quando você seleciona um vídeo na lista com o botão A (Enter)"""
        video_id = event.item.id.replace("vid_", "")
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Suspende a interface para abrir o player nativo MPV
        self.suspend_video(url)

    def suspend_video(self, url):
        # O X55 usa MPV com aceleração de hardware
        subprocess.run(["mpv", "--fs", url])

    def action_focus_search(self):
        self.query_one("#search_box").focus()

if __name__ == "__main__":
    app = YouTubeTV()
    app.run()
