import asyncio
from unittest import TestCase

from refit.workers import WorkerManager


async def hello():
    print('hello')


class TestWorkerManager(TestCase):
    """
    Testing ... async stuff ...
    """

    def test_adding_task(self):
        loop = asyncio.get_event_loop()
        manager = WorkerManager()

        loop.create_task(
            manager.start()
        )

        async def run():
            manager.add_coroutine(
                hello()
            )

        loop.create_task(
            run()
        )

        loop.create_task(
            manager.close()
        )

        loop.run_forever()
