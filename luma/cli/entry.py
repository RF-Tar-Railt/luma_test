from clilte.main import BaseCommand, CommandMetadata, register
from arclet.alconna import Alconna, Args, CommandMeta, Arparma
from ..compat import importlib_metadata


def _entry(group: str):
    entry_points = importlib_metadata.entry_points()
    entry_map: dict[str, str] = {entry.name: entry.value for entry in entry_points.select(group=group)}
    if not entry_map:
        return print(f"!!! '{group}' doesn't match any package in your python.")
    m_len = max(len(i) for i in entry_map)
    print("-" * (m_len + max(len(i) for i in entry_map.values())))
    print("Name".ljust(m_len + 4), "Path")
    print("-" * (m_len + max(len(i) for i in entry_map.values())))
    for k, v in entry_map.items():
        print(f"{k}".ljust(m_len + 4), v)


@register("luma")
class EntryPoint(BaseCommand):
    def init_plugin(self) -> Alconna:
        return Alconna(
            "entry", Args["group", ["luma-thirdparty", "creart.creators"], "creart.creators"],
            meta=CommandMeta(
                "查看声明了某个入口点的所有内容"
            )
        )

    def meta(self) -> CommandMetadata:
        return CommandMetadata("entry", "0.1.0", "query entry point", ["query"], ["RF-Tar-Railt"])

    def dispatch(self, result: Arparma):
        return _entry(result.group)
