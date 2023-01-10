from clilte.main import BaseCommand, CommandMetadata, register
from arclet.alconna import Alconna, Args, CommandMeta, Arparma, Option
from pathlib import Path
from luma.main import LumaCore
from luma.project import LumaProject
from luma import termui


@register("luma")
class Init(BaseCommand):
    def init_plugin(self) -> Alconna:
        return Alconna(
            "init", Args["project", str, "."],
            Option("-n|--non-interactive", help_text="Don't ask questions but use default values"),
            meta=CommandMeta(
                "为 Luma 初始化一个 luma.toml"
            )
        )

    def meta(self) -> CommandMetadata:
        return CommandMetadata("init", "0.1.0", "initialize a project", ["init"], ["RF-Tar-Railt"])

    def dispatch(self, result: Arparma):
        def ask(question: str, default: str) -> str:
            if result.query("non-interactive", False):
                return default
            return termui.ask(question, default=default)

        path = Path.cwd() if result.project == "." else Path(result.project)
        core = LumaCore.current()
        if path.parts[-1] == "luma.toml":
            path = path.parent
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        if (file := path / "luma.toml").exists():
            core.ui.echo("luma.toml already exists, update it now.", style="primary")
        else:
            core.ui.echo("Creating a luma.toml...", style="primary")
        project = LumaProject(file, ui=core.ui)
        if not result.query("non-interactive", False):
            endpoint = ask("Kayaku Config Endpoints", "{**}:./config.jsonc")


