import uasyncio as asyncio
from microdot import Microdot
import web.controller.ContentController as ContentController

async def init_app() -> None:
    app = Microdot()
    await ContentController.register(app)
    app.run(debug=True, port=80)

async def main():
    await init_app()

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    # Run the asynchronous main function
    asyncio.run(main())