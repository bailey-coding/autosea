from pathlib import Path
import os

CONFIG_PATH = Path("data/user_agent.conf")

UA_MAP = {
    "PC": {
        "Chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.3124.95"
    },
    "Mac": {
        "Safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
        "Chrome": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Firefox": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.7; rv:136.0) Gecko/20100101 Firefox/136.0",
    },
    "iOS": {
        "Safari": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Mobile/15E148 Safari/604.1",
        "Chrome": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/135.0.7049.35 Mobile/15E148 Safari/604.1",
        "Firefox": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/136.0 Mobile/15E148 Safari/605.1.15"
    },
    "Android": {
        "Chrome": "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.135 Mobile Safari/537.36",
        "Firefox": "Mozilla/5.0 (Android 15; Mobile; rv:68.0) Gecko/68.0 Firefox/136.0",
    },
}

def get_user_agent() -> str:
    try:
        return CONFIG_PATH.read_text().strip()
    except FileNotFoundError:
        return ""

def set_user_agent(agent: str):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(agent.strip())

def generate_export_line(agent: str) -> str:
    return f'export user_agent="{agent}"'

def tui():
    from textual.app import App, ComposeResult
    from textual.widgets import Static, Select
    from textual.containers import Vertical

    class UserAgentApp(App):
        CSS = """
        Screen {
            align: center middle;
        }
        """

        def compose(self) -> ComposeResult:
            yield Vertical(
                Static("Choose your platform:"),
                Select([(k, k) for k in UA_MAP.keys()], id="platform"),
                Static("Choose your browser:"),
                Select([], id="browser"),
            )

        def on_mount(self) -> None:
            self.query_one("#platform", Select).focus()

        def on_select_changed(self, event: Select.Changed) -> None:
            if event.select.id == "platform":
                browser_select = self.query_one("#browser", Select)
                browser_select.options = [(b, b) for b in UA_MAP[event.value].keys()]
                browser_select.value = None

            elif event.select.id == "browser":
                platform = self.query_one("#platform", Select).value
                browser = event.value
                if platform and browser:
                    agent = UA_MAP[platform][browser]
                    set_user_agent(agent)
                    print(generate_export_line(agent))
                    self.exit()

    UserAgentApp().run()

if __name__ == "__main__":
    tui()