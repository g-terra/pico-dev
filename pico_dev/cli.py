import shutil
import sys
from pathlib import Path
import typer
import importlib.resources as pkg_resources
from pico_dev import templates  # this makes templates a valid importable package

app = typer.Typer()

@app.command()
def new(name: str = typer.Option(..., prompt="Project name")):
    """
    Create a new Pico project folder using the default template.
    """
    root = Path(name)
    if root.exists():
        typer.secho(f"❌ Directory '{name}' already exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Extract the package path to the template
    with pkg_resources.path("pico_dev.templates", "default") as template_dir:
        shutil.copytree(
            template_dir,
            root,
            ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store')
        )


    typer.secho(f"✅ Created Pico project: {name}", fg=typer.colors.GREEN)
