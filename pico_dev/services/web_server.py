import shutil

import typer
from pathlib import Path
import importlib.resources as pkg_resources
import pico_dev.services.constants as constants

def get_web_server_config():
    """
       Prompt user for optional Wi-Fi Access Point configuration.

       Returns:
           tuple[str | None, str | None]: SSID and password, or (None, None) if skipped.
       """
    typer.secho("\n📡 Optional: Web server setup", fg=typer.colors.MAGENTA)
    return typer.confirm(
        "Would you like to configure a web server? this requires an access point to be running.",
        default=True,
    )

def configure_web_server(root: Path, project_name: str):
    """
    Copy in the web‐server boilerplate and inject project name.

    Args:
        root: Project root path (the folder that contains `src/`).
        project_name: The name to substitute into package.json.
    """
    # 1️⃣ Copy `web/` → src/web
    target_web = root / "src" / "web"
    target_web.parent.mkdir(parents=True, exist_ok=True)
    with pkg_resources.path(constants.WEB_SERVER_TEMPLATE_PACKAGE, "web") as tmpl_web:
        if target_web.exists():
            shutil.rmtree(target_web)
        shutil.copytree(tmpl_web, target_web)
    typer.secho(f"🌐 Web directory copied to: {target_web}", fg=typer.colors.BLUE)

    # 2️⃣ Copy Makefile & tailwind.config.js → project root
    for fname in ("Makefile", "tailwind.config.js"):
        with pkg_resources.path(constants.WEB_SERVER_TEMPLATE_PACKAGE, fname) as src_file:
            dst = root / fname
            shutil.copy(src_file, dst)
            typer.secho(f"📄 {fname} copied to: {dst}", fg=typer.colors.BLUE)


    # 3️⃣ Templated package.json
    with pkg_resources.path(constants.WEB_SERVER_TEMPLATE_PACKAGE, "package.json") as src_pkg:
        pkg_txt = src_pkg.read_text()
    pkg_txt = pkg_txt.replace("##PROJECT_NAME##", project_name)
    dst_pkg = root / "package.json"
    dst_pkg.write_text(pkg_txt)
    typer.secho(f"🛠 package.json written with project name “{project_name}”", fg=typer.colors.BLUE)

    # 4️⃣ Copy `lib/` → project root
    with pkg_resources.path(constants.WEB_SERVER_TEMPLATE_PACKAGE, "lib") as tmpl_lib:
        target_lib = root / "lib"
        if target_lib.exists():
            shutil.rmtree(target_lib)
        shutil.copytree(tmpl_lib, target_lib)
    typer.secho(f"📂 lib directory copied to: {target_lib}", fg=typer.colors.BLUE)

    # 5️⃣ Overwrite `main.py` in project root with template version
    with pkg_resources.path(constants.WEB_SERVER_TEMPLATE_PACKAGE, "main.py") as tmpl_main:
        dst_main = root / "src" / "main.py"
        shutil.copy(tmpl_main, dst_main)
    typer.secho(f"⚙️ main.py replaced from template at: {dst_main}", fg=typer.colors.BLUE)
