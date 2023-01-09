from __future__ import annotations
from clilte import CommandLine
import importlib
import pkgutil
from luma import termui

COMMANDS_MODULE_PATH: str = importlib.import_module("luma.cli").__path__  # type: ignore


class LumaCLI(CommandLine):
    def __init__(self):
        super().__init__("luma", "Luma-CLI", "0.1.0")
        for _, modname, _ in pkgutil.iter_modules(COMMANDS_MODULE_PATH):
            __ = importlib.import_module(f"luma.cli.{modname}", __name__)

    @property
    def help(self):
        cmds = []
        cmds_description = []
        max_len = 1
        for name, plg in self.plugins.items():
            if plg._command.headers and plg._command.command:
                cmds.append(
                    f"[{''.join(map(str, plg._command.headers))}]{plg._command.command}"
                )
            elif plg._command.headers:
                cmds.append(
                    f"{', '.join(sorted(map(str, plg._command.headers), key=len, reverse=True))}"
                )
            else:
                cmds.append(f"{name}")
            cmds_description.append(plg._command.meta.description)
        if cmds:
            max_len = max(max(map(len, cmds)), max_len)
        opts = []
        opts_description = []
        for name, opt in self.options.items():
            if opt._command.headers and opt._command.command:
                opts.append(
                    f"[{''.join(map(str, opt._command.headers))}]{opt._command.command}"
                )
            elif opt._command.headers:
                opts.append(
                    f"{', '.join(sorted(map(str, opt._command.headers), key=len, reverse=True))}"
                )
            else:
                opts.append(f"{name}")
            opts_description.append(opt._command.meta.description)
        if opts:
            max_len = max(max(map(len, opts)), max_len)
        cmd_string = "\n".join(
            f"    {termui.style(i.ljust(max_len), style='primary')}\t{j}" for i, j in zip(cmds, cmds_description)
        )
        opt_string = "\n".join(
            f"    {termui.style(i.ljust(max_len), style='primary')}\t{j}" for i, j in zip(opts, opts_description)
        )
        cmd_help = termui.style("Commands:\n", style="warning") if cmd_string else ""
        opt_help = termui.style("Options:\n", style="warning") if opt_string else ""
        footer = 'Use "luma <command> --help" for more information about a command.'
        return (
            f"{termui.style(self.name, style='success')}\n\n"
            f"{cmd_help}{cmd_string}\n{opt_help}{opt_string}\n\n"
            f"{termui.style(footer, style='success')}"
        )


def main(args: list[str] | None = None) -> None:
    return LumaCLI().main(args)
