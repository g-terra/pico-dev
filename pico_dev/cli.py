import shutil
from pathlib import Path
import typer
import importlib.resources as pkg_resources
from pico_dev import templates

app = typer.Typer()

@app.command()
def new(name: str = typer.Option(..., prompt="📁 Project name")):
    """
    Create a new Pico project folder using the default template.
    Optionally sets up Wi-Fi Access Point credentials and boot.py.
    """
    # === Step 1: Collect user input ===

    # Prompt for Access Point setup
    typer.secho("\n📡 Optional: Wi-Fi Access Point Setup", fg=typer.colors.MAGENTA)
    setup_ap = typer.confirm("Would you like to configure the Pico as a Wi-Fi Access Point?", default=True)

    ssid = "PicoW-AP"
    password = "12345678"

    if setup_ap:
        ssid = typer.prompt("Enter SSID", default=ssid)
        password = typer.prompt("Enter password (min 8 characters)", default=password)

        if len(password) < 8:
            typer.secho("❌ Password must be at least 8 characters long.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    # === Step 2: Create project ===

    root = Path(name)
    if root.exists():
        typer.secho(f"❌ Directory '{name}' already exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Copy base template
    typer.secho("\n📦 Creating base project files...", fg=typer.colors.CYAN)
    with pkg_resources.path("pico_dev.templates", "default") as template_dir:
        shutil.copytree(
            template_dir,
            root,
            ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store')
        )
    typer.secho(f"✅ Project structure created at: {root}", fg=typer.colors.GREEN)

    # === Step 3: If AP is enabled, generate secrets.py and copy boot.py ===

    if setup_ap:
        # Write secrets.py
        secrets_path = root / "src" / "secrets.py"
        secrets_path.write_text(f'SSID = "{ssid}"\nPASSWORD = "{password}"\n')
        typer.secho(f"🔐 Wi-Fi credentials saved to: {secrets_path}", fg=typer.colors.BLUE)

        # Copy boot.py
        with pkg_resources.path("pico_dev.templates.access_point", "boot.py") as ap_boot:
            shutil.copy(ap_boot, root / "src" / "boot.py")
        typer.secho("📄 boot.py for Access Point copied to src/", fg=typer.colors.BLUE)

    # === Done ===
    typer.secho("\n🎉 Project setup complete!", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
