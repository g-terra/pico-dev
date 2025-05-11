# File: pico_dev/commands/new.py
import typer
from pico_dev.services import  web_server , constants , access_point, project

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
    web: bool = typer.Option(
        False,
        "--web",
        "-web",
        help="Configure a simple web server with necessary libs, no prompts.",
    ),
):

    if ap:
        ssid, password = constants.DEFAULT_SSID, constants.DEFAULT_PASSWORD
    else:
        ssid, password = access_point.get_ap_config()

    root, project_name = project.create_base_project(name)

    if ssid and password:
        access_point.configure_access_point(root, ssid, password)

    if web or web_server.get_web_server_config():
        web_server.configure_web_server(root, project_name)

    typer.secho("\n🎉 Project setup complete!", fg=typer.colors.GREEN)
