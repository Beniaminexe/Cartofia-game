import asyncio
import main as game_main


async def main() -> None:
    """Entry point for pygbag: just await the game's async main."""
    await game_main.main()


if __name__ == "__main__":
    asyncio.run(main())
