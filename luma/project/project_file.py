from __future__ import annotations

from tomlkit import items

from .toml_file import TOMLBase


class LumaProject(TOMLBase):
    """The data object representing th pyproject.toml file"""

    def write(self, show_message: bool = True) -> None:
        """Write the TOMLDocument to the file."""
        super().write()
        if show_message:
            self.ui.echo("Changes are written to [success]luma.toml[/].")

    # @property
    # def is_valid(self) -> bool:
    #     return "project" in self._data

    @property
    def config_root(self) -> items.Table:
        return self._data.setdefault("config", {})

    @property
    def config_modules(self) -> items.Table:
        return self._data.setdefault("module", {})

    @property
    def settings(self) -> items.Table:
        return self._data.setdefault("tool", {}).setdefault("luma", {})

    # def content_hash(self, algo: str = "sha256") -> str:
    #     """Generate a hash of the sensible content of the pyproject.toml file.
    #     When the hash changes, it means the project needs to be relocked.
    #     """
    #     dump_data = {
    #         "sources": self.settings.get("source", []),
    #         "dependencies": self.metadata.get("dependencies", []),
    #         "dev-dependencies": self.settings.get("dev-dependencies", {}),
    #         "optional-dependencies": self.metadata.get("optional-dependencies", {}),
    #         "requires-python": self.metadata.get("requires-python", ""),
    #     }
    #     pyproject_content = json.dumps(dump_data, sort_keys=True)
    #     hasher = hashlib.new(algo)
    #     hasher.update(pyproject_content.encode("utf-8"))
    #     return hasher.hexdigest()
