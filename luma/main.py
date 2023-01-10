from __future__ import annotations
from clilte import CommandLine, Helper
from contextvars import ContextVar
from contextlib import contextmanager
import importlib
import pkgutil
from luma import termui, __version__

COMMANDS_MODULE_PATH: str = importlib.import_module("luma.cli").__path__  # type: ignore


class RichHelper(Helper):
    def cmd_line(self, name, desc, max_len: int = 0):
        return f"  [cyan3]{name.ljust(max_len)}[/]    {desc}"

    def opt_line(self, name, desc, max_len: int = 0):
        return f"  [cyan]{name.ljust(max_len)}[/]    {desc}"

    def help(self):
        footer = 'Use "luma <command> --help" for more information about a command.'
        return (
            f"[bold green]{self.cli.name}[/]\n\n"
            f"{self.lines('[bold yellow]Commands[/]', '[bold dark_orange]Options[/]')}\n\n"
            f"[bold blue]{footer}[/]"
        )


CoreInstance: ContextVar['LumaCore'] = ContextVar("luma_instance")


class LumaCore:
    def __init__(self):
        self.cli = CommandLine(
            "luma",
            "Luma-CLI",
            __version__,
            termui.rprint,
            argparser_formatter=True,
            _helper=RichHelper
        )
        self.ui = termui.UI()

    @classmethod
    def current(cls):
        return CoreInstance.get()

    @contextmanager
    def use(self):
        token = CoreInstance.set(self)
        yield
        CoreInstance.reset(token)


def main(args: list[str] | None = None) -> None:
    for _, modname, _ in pkgutil.iter_modules(COMMANDS_MODULE_PATH):
        __ = importlib.import_module(f"luma.cli.{modname}", __name__)
    core = LumaCore()
    with core.use():
        return core.cli.main(args)
