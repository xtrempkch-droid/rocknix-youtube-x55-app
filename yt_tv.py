#!/usr/bin/env python3
import asyncio
import subprocess
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListItem, ListView, Label, Input
from textual.containers import Vertical

class YouTubeTV(App):
    TITLE = "X55 Ultra-Light YouTube"
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("s", "focus_search", "Buscar"),
        ("backspace", "back_to_list", "Voltar"),
    ]

    CSS = """
    ListView { width: 100%; height: 1fr; border: double $accent; background: $surface; }
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

    async def on_mount(self) -> None:
        # Foca a busca por padrão
        self.query_one("#search_box").focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        termo = event.value.strip()
        if termo:
            await self.buscar_videos_otimizado(termo)

    async def buscar_videos_otimizado(self, busca: str) -> None:
        """
        Busca usando yt-dlp de forma assíncrona e rápida (--flat-playlist + --print).
        Evita travar a TUI ao rodar o processo em background.
        """
        lista = self.query_one("#video_list", ListView)
        lista.clear()
        lista.append(ListItem(Label("⏳ Buscando...", classes="loading"), id="loading"))
        search_input = self.query_one("#search_box", Input)
        search_input.disabled = True
        cmd = [
            "yt-dlp",
            f"ytsearch10:{busca}",
            "--flat-playlist",
            "--print", "%(title)s|%(id)s"
        ]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            lista.clear()

            if proc.returncode != 0:
                err_text = stderr.decode(errors="ignore").strip()
                lista.append(ListItem(Label("Erro na busca. Veja logs.")))
                self.log(f"yt-dlp stderr: {err_text}")
                return

            for line in stdout.decode(errors="ignore").splitlines():
                if "|" in line:
                    titulo, video_id = line.split("|", 1)
                    display = titulo.strip()
                    if len(display) > 80:
                        display = display[:77] + "..."
                    item = ListItem(Label(f"📺 {display}"), id=f"vid_{video_id.strip()}")
                    lista.append(item)

            if len(lista.children) == 0:
                lista.append(ListItem(Label("Nenhum resultado encontrado.")))
            else:
                lista.focus()

        except FileNotFoundError:
            lista.clear()
            lista.append(ListItem(Label("yt-dlp não encontrado. Instale yt-dlp.")))
        except Exception as e:
            lista.clear()
            lista.append(ListItem(Label("Erro ao executar a busca.")))
            self.log(f"Exception in buscar_videos_otimizado: {e}")
        finally:
            search_input.disabled = False

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        # event.item é o ListItem selecionado
        if not getattr(event.item, "id", None):
            return
        video_id = event.item.id.replace("vid_", "")
        url = f"https://www.youtube.com/watch?v={video_id}"
        self.suspend_video(url)

    def suspend_video(self, url: str) -> None:
        """
        Suspende a TUI e executa o mpv de forma que o player ocupe o terminal.
        Usa self.suspend() como contexto (Textual provê essa interface para pausar a UI).
        """
        mpv_cmd = [
            "mpv",
            "--fs",
            "--vo=gpu",
            "--hwdec=auto",
            "--ytdl-format=best[height<=720]",
            url
        ]
        try:
            # self.suspend() pausa a UI e restaura no retorno
            with self.suspend():
                subprocess.run(mpv_cmd)
        except FileNotFoundError:
            self.notify("mpv não encontrado. Instale mpv.", severity="error")
        except Exception as e:
            self.notify("Erro ao abrir o player.", severity="error")
            self.log(f"Exception in suspend_video: {e}")

    def action_focus_search(self) -> None:
        self.query_one("#search_box", Input).focus()

    def action_back_to_list(self) -> None:
        self.query_one("#video_list", ListView).focus()

if __name__ == "__main__":
    YouTubeTV().run()
