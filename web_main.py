import asyncio
import runpy


async def main() -> None:
    """
    Entry point for pygbag.

    It just runs cartofia.py as if you had done:
        python cartofia.py

    All your existing game code stays in cartofia.py.
    """
    # This will execute cartofia.py with __name__ == "__main__"
    runpy.run_module("main", run_name="__main__")


if __name__ == "__main__":
    asyncio.run(main())
