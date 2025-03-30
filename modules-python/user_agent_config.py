from pathlib import Path
import json
from pydantic import BaseModel
from typing import Optional
from textual.app import App, ComposeResult
from textual.widgets import Static, Select, Button
from textual.containers import Vertical, Horizontal
from textual import on

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
USERAGENT_OPTIONS_PATH = DATA_DIR / "useragent_options.json"
CONFIG_PATH = DATA_DIR / "user-agent.conf"

class OperatingSystemUserAgentsModel(BaseModel):
    Chrome: Optional[str] = None
    Firefox: Optional[str] = None
    Edge: Optional[str] = None
    Safari: Optional[str] = None

class OperatingSystemsModel(BaseModel):
    PC: Optional[OperatingSystemUserAgentsModel] = None
    Mac: Optional[OperatingSystemUserAgentsModel] = None
    iOS: Optional[OperatingSystemUserAgentsModel] = None
    Android: Optional[OperatingSystemUserAgentsModel] = None

# Load user agent data safely
try:
    with USERAGENT_OPTIONS_PATH.open("r") as f:
        useragent_data = json.load(f)
except FileNotFoundError:
    print(f"[ERROR] File not found: {USERAGENT_OPTIONS_PATH}")
    exit(1)

OS_UserAgent_Model = OperatingSystemsModel(**useragent_data)
OS_DICT = OS_UserAgent_Model.model_dump()

def set_user_agent(agent: str):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(agent.strip())

def generate_export_line(agent: str) -> str:
    return f'export user_agent="{agent}"'

def tui():
    class UserAgentApp(App):

        def compose(self) -> ComposeResult:
            self.platform = None
            self.browser = None

            platforms = [(os, os) for os in OS_DICT.keys()]
            self.platform_select = Select(options=platforms, id="platform")
            self.browser_static = Static("Choose your browser:")
            self.browser_select = Select(options=[])

            self.button_row = Horizontal(
                Button("Cancel", id="cancel", variant="error"),
                Button("Okay", id="confirm", disabled=True, variant="success"),
            )

            self.input_container = Vertical(
                Static("Choose your platform:"),
                self.platform_select,
                self.browser_static,
                self.browser_select,
            )

            self.layout = Vertical(
                self.input_container,
                self.button_row,
                id="dialog",
            )

            yield self.layout

        def on_mount(self) -> None:
            self.platform_select.focus()

        def validate_ready(self):
            confirm_button = self.query_one("#confirm", Button)
            confirm_button.disabled = not (self.platform and self.browser)

        @on(Select.Changed, "#platform")
        def platform_selected(self, event: Select.Changed) -> None:
            self.platform = event.value
            self.browser = None
            self.validate_ready()

            platform_data = OS_DICT.get(self.platform)
            if not platform_data:
                print(f"[ERROR] No platform data for {self.platform}")
                return

            browser_options = [
                (browser, browser)
                for browser, agent in platform_data.items()
                if agent
            ]

            if self.browser_select.parent:
                self.browser_select.remove()

            self.browser_select = Select(options=browser_options)
            self.input_container.mount(self.browser_select, after=self.browser_static)
            self.browser_select.focus()

        @on(Select.Changed)
        def browser_selected(self, event: Select.Changed) -> None:
            if event.select is self.browser_select:
                self.browser = event.value
                self.validate_ready()

        @on(Button.Pressed, "#cancel")
        def cancel_pressed(self) -> None:
            print("[ACTION] Cancelled by user. Exiting.")
            self.exit()

        @on(Button.Pressed, "#confirm")
        def confirm_pressed(self) -> None:
            if not (self.platform and self.browser):
                print("[ERROR] Incomplete selection.")
                return

            platform_data = OS_DICT.get(self.platform)
            agent = platform_data.get(self.browser) if platform_data else None

            if agent:
                print(f"[SUCCESS] Selected: {self.platform}/{self.browser}")
                print(f"[WRITING] {agent}")
                set_user_agent(agent)
                print(generate_export_line(agent))
                self.exit()
            else:
                print(f"[ERROR] No agent for {self.platform}/{self.browser}")
                self.exit(1)

    UserAgentApp().run()

if __name__ == "__main__":
    tui()
