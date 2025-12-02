import sys
import asyncio

import main as main_mod


class Game:
    """A minimal Game wrapper that runs the main entry in the repo.
    This wrapper is intentionally light so we don't duplicate the many globals.
    It will call an existing `main()` coroutine if found, or fallback to a synchronous `run()` function.
    """

    def __init__(self):
        self.main_module = main_mod

    async def run_async(self):
        # If the main module exports an async main coroutine -> call it
        main_obj = getattr(self.main_module, 'main', None)
        if main_obj and asyncio.iscoroutinefunction(main_obj):
            await main_obj()
            return
        # Fallback: find a sync function named 'run' or 'main' and call it in a thread
        run_fn = getattr(self.main_module, 'run', None) or main_obj
        if run_fn and callable(run_fn):
            # call synchronously in thread
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, run_fn)
            return
        raise RuntimeError('No suitable main/run function found in main module')

    def run(self):
        # Synchronous run: call the async variant or directly call sync run
        try:
            main_obj = getattr(self.main_module, 'main', None)
            if main_obj and asyncio.iscoroutinefunction(main_obj):
                asyncio.run(main_obj())
                return
            run_fn = getattr(self.main_module, 'run', None) or main_obj
            if run_fn and callable(run_fn):
                run_fn()
                return
        except Exception as e:
            print('Error running main module via wrapper:', e)
        raise RuntimeError('Could not find runnable entrypoint in main module')


if __name__ == '__main__':
    Game().run()
