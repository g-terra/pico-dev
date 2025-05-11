# File: pico_dev/services/project.py
import typer
import shutil
from pathlib import Path
import importlib.resources as pkg_resources
import pico_dev.services.constants as constants

def create_base_project(name: str) -> tuple[Path, str]:
    """
    Copy the default template into a new project directory.

    Args:
        name: Name of the project directory.

    Returns:
        Path: Path to the created project directory.
    """
    root = Path(name)
    if root.exists():
        typer.secho(
            f"❌ Directory '{name}' already exists.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    typer.secho("\n📦 Creating base project files...", fg=typer.colors.CYAN)
    with pkg_resources.path(constants.TEMPLATE_PACKAGE, constants.DEFAULT_TEMPLATE_DIR) as template_dir:
        shutil.copytree(
            template_dir,
            root,
            ignore=shutil.ignore_patterns(
                '__pycache__', '*.pyc', '.DS_Store'
            ),
        )
    typer.secho(
        f"✅ Project structure created at: {root}",
        fg=typer.colors.GREEN,
    )
    return root , name