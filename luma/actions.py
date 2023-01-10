from luma.project import LumaProject

def do_init(
    project: LumaProject,
    name: str = "",
    version: str = "",
    description: str = "",
    license: str = "MIT",
    author: str = "",
    email: str = "",
    python_requires: str = ""
) -> None:
    """Bootstrap the project and create a pyproject.toml"""
    data = {
        "project": {
            "name": name,
            "version": version,
            "description": description,
            "authors": array_of_inline_tables([{"name": author, "email": email}]),
            "license": make_inline_table({"text": license}),
            "dependencies": make_array([], True),
        },
    }
    if build_backend is not None:
        data["build-system"] = build_backend.build_system()
    if python_requires and python_requires != "*":
        data["project"]["requires-python"] = python_requires  # type: ignore
    if name and version:
        readme = next(project.root.glob("README*"), None)
        if readme is None:
            readme = project.root.joinpath("README.md")
            readme.write_text(f"# {name}\n\n{description}\n")
        data["project"]["readme"] = readme.name  # type: ignore
    get_specifier(python_requires)
    project.pyproject._data.update(data)
    project.pyproject.write()
    hooks.try_emit("post_init")