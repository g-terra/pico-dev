# File: pico_dev/services/project.py
import typer
import shutil
from pathlib import Path
import importlib.resources as pkg_resources

# Template locations
TEMPLATE_PACKAGE = "pico_dev.templates"
DEFAULT_TEMPLATE_DIR = "default"
AP_TEMPLATE_PACKAGE = "pico_dev.templates.access_point"

# Default Access Point credentials
DEFAULT_SSID = "PicoW-AP"
DEFAULT_PASSWORD = "12345678"

def get_ap_config():
    """
    Prompt user for optional Wi-Fi Access Point configuration.

    Returns:
        tuple[str | None, str | None]: SSID and password, or (None, None) if skipped.
    """
    typer.secho("\n📡 Optional: Wi-Fi Access Point Setup", fg=typer.colors.MAGENTA)
    setup_ap = typer.confirm(
        "Would you like to configure the Pico as a Wi-Fi Access Point?",
        default=True,
    )
    if not setup_ap:
        return None, None

    ssid = typer.prompt("Enter SSID", default=DEFAULT_SSID)
    password = typer.prompt(
        "Enter password (min 8 characters)",
        default=DEFAULT_PASSWORD,
    )
    if len(password) < 8:
        typer.secho(
            "❌ Password must be at least 8 characters long.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    return ssid, password

def create_base_project(name: str) -> Path:
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
    with pkg_resources.path(TEMPLATE_PACKAGE, DEFAULT_TEMPLATE_DIR) as template_dir:
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
    return root

def configure_access_point(root: Path, ssid: str, password: str):
    """
    Write Wi-Fi credentials and copy AP-specific boot.py.

    Args:
        root: Project root path.
        ssid: Wi-Fi SSID.
        password: Wi-Fi password.
    """
    secrets_path = root / "src" / "secrets.py"
    secrets_path.write_text(
        f'SSID = "{ssid}"\nPASSWORD = "{password}"\n'
    )
    typer.secho(
        f"🔐 Wi-Fi credentials saved to: {secrets_path}",
        fg=typer.colors.BLUE,
    )

    with pkg_resources.path(
        AP_TEMPLATE_PACKAGE, "boot.py"
    ) as ap_boot:
        shutil.copy(ap_boot, root / "src" / "boot.py")
    typer.secho(
        "📄 boot.py for Access Point copied to src/",
        fg=typer.colors.BLUE,
    )
