import typer
from rich import print
from rich.table import Table
from enum import StrEnum
import subprocess
import shutil
import pathlib
import os


class Library(StrEnum):
    FASTAPI = "fastapi"
    NEXTJS = "nextjs"
    NESTJS = "nestjs" # ! To be implemented


def get_path():
    return pathlib.Path(__file__).resolve()


def get_this_dir():
    return get_path().parent


def get_library_init_command(library: Library, project_name: str):
    if library == Library.FASTAPI:
        return ["poetry", "new", "--src", f"{project_name}"]

    return []


def get_install_deps_commands(library: Library):
    dependencies = []
    if library == Library.FASTAPI:
        dependencies = [
            "fastapi",
            "gunicorn",
            'uvicorn', 
            "sqlalchemy", 
            "pydantic-settings", 
            "psycopg2", 
            "psycopg2-binary",
            "bcrypt",
            "cryptography"]
        return [(dep, ["poetry", "add", f"{dep}"]) for dep in dependencies]

    return []


def get_dockerfile(library: Library):
    dockerfile = get_this_dir() / library / "Dockerfile"
    dockerignore = get_this_dir() / library / ".dockerignore"
    return [dockerfile, dockerignore]


app = typer.Typer()


@app.command()
def create(
    library: Library,
    project_name: str,
    dockerfile: bool = True, # ! To be implemented
    src: bool = True,
    poetry: bool = True, # ! To be implemented
    latest: bool = True, # ! To be implemented
):
    cmd = get_library_init_command(library=library, project_name=project_name)
    if len(cmd) == 0:
        print(f"[bold red]Error! Library {library} not implemented yet![/bold red] :boom:")
        raise typer.Exit(code=1)
    
    print(f"[bold green]Creating new project[bold green]")
    table = Table("Project Name", "Library")
    table.add_row(project_name, library)
    print(table)
    subprocess.run(cmd)

    for dockerfile in get_dockerfile(library=library):
        shutil.copy2(dockerfile, f"./{project_name}")
    
    if library == Library.FASTAPI:
        shutil.copytree(get_this_dir() / library / "src", f"./{project_name}/src", dirs_exist_ok=True)
        shutil.copy2(get_this_dir() / library / "server.py", f"./{project_name}")
    
    os.chdir(get_this_dir() / project_name)
    for install_dep in get_install_deps_commands(library=library):
        dep, install_cmd = install_dep
        print(f"[bold green]Installing {dep}[bold green]")
        subprocess.run(install_cmd) 
    print(f"[bold green]Success! Project created[bold green] :boom:")
    print(f"  cd {project_name}")
    print(f"  python src/main.py")


@app.command()
def delete(name: str, formal: bool = False):
    pass



if __name__ == "__main__":
    app()
