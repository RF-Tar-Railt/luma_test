from __future__ import annotations
from clilte import CommandLine
from contextvars import ContextVar
from contextlib import contextmanager
import importlib
import pkgutil
from luma import termui, __version__

COMMANDS_MODULE_PATH: str = importlib.import_module("luma.cli").__path__  # type: ignore


def rich_helper(cli: CommandLine):
    cmds = []
    cmds_description = []
    max_len = 1
    for name, plg in cli.plugins.items():
        if plg.command.headers and plg.command.command:
            cmds.append(
                f"[{''.join(map(str, plg.command.headers))}]{plg.command.command}"
            )
        elif plg.command.headers:
            cmds.append(
                f"{', '.join(sorted(map(str, plg.command.headers), key=len, reverse=True))}"
            )
        else:
            cmds.append(f"{name}")
        cmds_description.append(plg.command.meta.description)
    if cmds:
        max_len = max(max(map(len, cmds)), max_len)
    opts = []
    opts_description = []
    for name, opt in cli.options.items():
        if opt.command.headers and opt.command.command:
            opts.append(
                f"[{''.join(map(str, opt.command.headers))}]{opt.command.command}"
            )
        elif opt.command.headers:
            opts.append(
                f"{', '.join(sorted(map(str, opt.command.headers), key=len))}"
            )
        else:
            opts.append(f"{name}")
        opts_description.append(opt.command.meta.description)
    if opts:
        max_len = max(max(map(len, opts)), max_len)
    cmd_string = "\n".join(
        f"    {termui.style(i.ljust(max_len), style='cyan3')}\t{j}" for i, j in zip(cmds, cmds_description)
    )
    opt_string = "\n".join(
        f"    {termui.style(i.ljust(max_len), style='cyan')}\t{j}" for i, j in zip(opts, opts_description)
    )
    cmd_help = termui.style("Commands:\n", style="bold yellow") if cmd_string else ""
    opt_help = termui.style("Options:\n", style="bold dark_orange") if opt_string else ""
    footer = 'Use "luma <command> --help" for more information about a command.'
    return (
        f"{termui.style(cli.name, style='bold green')}\n\n"
        f"{cmd_help}{cmd_string}\n{opt_help}{opt_string}\n\n"
        f"{termui.style(footer, style='bold blue')}"
    )


CoreInstance: ContextVar['LumaCore'] = ContextVar("luma_instance")


class LumaCore:
    def __init__(self):
        self.cli = CommandLine("luma", "Luma-CLI", __version__, helper=rich_helper, argparser_formatter=True)
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
