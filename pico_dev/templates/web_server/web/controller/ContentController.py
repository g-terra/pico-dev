from microdot import Microdot ,send_file

class ContentController:
    """
    Controller that automatically registers routes for all files in a static folder.

    - `/` serves `<static_folder>/index.html`
    - `/<filename>` serves other files in the folder (e.g., CSS, JS)
    """

    def __init__(self, app: Microdot):
        self.app = app

    async def register_routes(self) -> None:
        """
        Register routes for serving static files.

        Args:
            app (Microdot): The Microdot application instance.
        """

        @self.app.route('/')
        async def main(request):
            return send_file('web/static/index.html')

        # a route for saving files in the static folder. it should be path aware for example /styles/style.css maps to src/static/styles/style.css
        @self.app.route('/<path:path>')
        async def send_static_file(request, path):
            # Check if the file exists in the static folder
            try:
                return send_file(f'web/static/{path}')
            except FileNotFoundError:
                return 'File not found', 404


async def register(app: Microdot) -> None:
    """
    Register the ApiController with the given Microdot application.

    Args:
        app (Microdot): The Microdot application instance.
    """
    await ContentController(app).register_routes()

