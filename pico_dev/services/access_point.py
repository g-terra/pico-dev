import shutil

import typer
from pathlib import Path
import importlib.resources as pkg_resources
import pico_dev.services.constants as constants


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

    ssid = typer.prompt("Enter SSID", default=constants.DEFAULT_SSID)
    password = typer.prompt(
        "Enter password (min 8 characters)",
        default=constants.DEFAULT_PASSWORD,
    )
    if len(password) < 8:
        typer.secho(
            "❌ Password must be at least 8 characters long.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    return ssid, password


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
        constants.AP_TEMPLATE_PACKAGE, "boot.py"
    ) as ap_boot:
        shutil.copy(ap_boot, root / "src" / "boot.py")
    typer.secho(
        "📄 boot.py for Access Point copied to src/",
        fg=typer.colors.BLUE,
    )
