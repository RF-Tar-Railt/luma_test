from clilte.main import BaseCommand, CommandMetadata, register
from arclet.alconna import Alconna, Args, CommandMeta, Arparma, Option
from pathlib import Path
from ..compat import tomllib

def init_luma(path: Path, interactive: bool = True):
    if not path.exists():
        path.mkdir(parents=True)
    if not (path / "luma.toml").exists():
        with open(path / "luma.toml", "w") as f:
            f.write(tomllib.dumps({"name": "luma"}))
    if not (path / "luma").exists():
        (path / "luma").mkdir()
    if not (path / "luma" / "__init__.py").exists():
        with open(path / "luma" / "__init__.py", "w") as f:
            f.write("")



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
        path = Path.cwd() if result.project == "." else Path(result.project)
        path.mkdir(parents=True, exist_ok=True)
        return init_luma(path, not result.non_interactive)