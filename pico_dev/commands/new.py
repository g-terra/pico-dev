# File: pico_dev/commands/new.py
import typer
from pico_dev.services.project import (
    DEFAULT_SSID,
    DEFAULT_PASSWORD,
    get_ap_config,
    create_base_project,
    configure_access_point,
)

app = typer.Typer()

@app.command()
def new(
    name: str = typer.Argument(..., help="Project name"),
    ap: bool = typer.Option(
        False,
        "--ap",
        "-ap",
        help="Configure Wi-Fi Access Point with default credentials, no prompts.",
    ),
):
    """
    Create a new Pico project folder using the default template.
    Optionally sets up Wi-Fi Access Point credentials and boot.py.
    """
    if ap:
        ssid, password = DEFAULT_SSID, DEFAULT_PASSWORD
    else:
        ssid, password = get_ap_config()

    root = create_base_project(name)

    if ssid and password:
        configure_access_point(root, ssid, password)

    typer.secho("\n🎉 Project setup complete!", fg=typer.colors.GREEN)
