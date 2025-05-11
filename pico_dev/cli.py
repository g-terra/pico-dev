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
        web: bool = typer.Option(
            False,
            "--web",
            "-web",
            help="Configure a simple web server with necessary libs",
        ),
):
    """
    Shortcut invocation: `pico-dev --new <name> [--ap] [--web]`
    """
    if new:
        # Inline logic for shortcut
        from pico_dev.services.project import (
            create_base_project,
        )

        from pico_dev.services.constants import (
            DEFAULT_SSID,
            DEFAULT_PASSWORD
        )

        from pico_dev.services.access_point import (
            get_ap_config,
            configure_access_point,
        )

        from pico_dev.services.web_server import (
            configure_web_server,
        )

        if ap:
            ssid, password = DEFAULT_SSID, DEFAULT_PASSWORD
        else:
            ssid, password = get_ap_config()

        root, project_name = create_base_project(new)
        if ssid and password:
            configure_access_point(root, ssid, password)

        if web:
            configure_web_server(root, project_name)

        typer.secho("\n🎉 Project setup complete!", fg=typer.colors.GREEN)
        raise typer.Exit()


# Register regular subcommand
app.command()(new_command)

if __name__ == "__main__":
    app()
