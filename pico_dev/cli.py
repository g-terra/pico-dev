# File: cli.py
import typer
from pico_dev.commands.new import new as new_command

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(
    new: str = typer.Option(
        None,
        "--new",
        "-new",
        help="Create a new Pico project",
    ),
    ap: bool = typer.Option(
        False,
        "--ap",
        "-ap",
        help="Configure Wi-Fi Access Point with default credentials",
    ),
):
    """
    Shortcut invocation: `pico-dev --new <name> [--ap]`
    """
    if new:
        # Inline logic for shortcut
        from pico_dev.services.project import (
            DEFAULT_SSID,
            DEFAULT_PASSWORD,
            get_ap_config,
            create_base_project,
            configure_access_point,
        )
        if ap:
            ssid, password = DEFAULT_SSID, DEFAULT_PASSWORD
        else:
            ssid, password = get_ap_config()

        root = create_base_project(new)
        if ssid and password:
            configure_access_point(root, ssid, password)

        typer.secho("\n🎉 Project setup complete!", fg=typer.colors.GREEN)
        raise typer.Exit()

# Register regular subcommand
app.command()(new_command)

if __name__ == "__main__":
    app()
