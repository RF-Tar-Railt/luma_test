from __future__ import annotations

from clilte.main import BaseCommand, CommandMetadata, register
from arclet.alconna import Alconna, Args, CommandMeta, Arparma, Field, Option
from luma.compat import importlib_metadata
from luma.main import LumaCore
from luma import termui


def _entry(group: str | None = None, is_list: bool = False):
    entry_points = importlib_metadata.entry_points()
    is_list = is_list or (not group)
    if is_list:
        groups = sorted(entry_points.groups)
        LumaCore.current().ui.display_columns(
            [
                [
                    f'[yellow3]{group}[/]',
                    f'[cyan3]{" | ".join(sorted(entry_points.select(group=group).names))}[/]'
                ]
                for group in groups
            ],
            ["Group", "Names"]
        )
    elif entry_map := {entry.name: entry.value for entry in entry_points.select(group=group)}:
        LumaCore.current().ui.display_columns(
            [
                [f'[req]{k}[/]', f'[magenta]{v.split(":")[0]}[/]', f'[red]{v.split(":")[-1]}[/]']
                for k, v in entry_map.items()
            ],
            ["Name", "Path", "Entry"]
        )
    else:
        return print(f"{termui.style(group, style='bold cyan')} doesn't match any package in your python env.")


@register("luma")
class EntryPoint(BaseCommand):
    def init(self) -> Alconna:
        return Alconna(
            "entry", Args["group;?", str, Field(completion=lambda: ["luma-thirdparty", "creart.creators"])],
            Option("--list", help_text="展示当前环境所有的 entry_point"),
            meta=CommandMeta(
                "查看声明了某个入口点的所有内容"
            )
        )

    def meta(self) -> CommandMetadata:
        return CommandMetadata("entry", "0.1.0", "query entry point", ["query"], ["RF-Tar-Railt"])

    def dispatch(self, result: Arparma):
        return _entry(result.group, bool(result.components.get('list')))
