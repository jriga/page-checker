import asyncio
import signal
import logging
import functools as ft


class AsyncRunner:
    def __init__(self, coro, frequency=None):
        self.coro = coro
        self.task = None
        self.callbacks = []
        self.frequency = frequency
        self.loop = asyncio.get_event_loop()
        self.stop_signals = (
            signal.SIGHUP,
            signal.SIGTERM,
            signal.SIGINT)

    async def stop(self, s):
        logging.debug(f'Stopping with signal {s.name}')
        if self.task:
            self.task.cancel()

        self.loop.stop()

    def exception_handler(self, loop, context):
        logging.debug(f'Loop handling exception: {context}')

    def before_run(self, *callbacks):
        self.callbacks = callbacks

    async def periodic_task(self):
        while True:
            logging.debug('In periodic_task awaiting self.coro')
            res = await self.coro
            logging.debug('- '*30)
            await asyncio.sleep(self.frequency)

    def run(self):
        logging.debug('add exception handler')
        self.loop.set_exception_handler(self.exception_handler)

        if self.frequency
        logging.debug(f'frequency == {self.frequency}')
        self.task = self.loop.create_task(self.periodic_task())
        else:
            logging.debug('add coroutine')
            self.task = self.loop.create_task(self.coro)

        logging.debug(f'add stop signals for {self.stop_signals}')
        for s in self.stop_signals:
            self.loop.add_signal_handler(
                s,
                lambda x: asyncio.create_task(self.stop(x)),
                s)

        logging.debug('Executing *before_run* callbacks')
        for fn in self.callbacks:
            fn()

        logging.debug('start the loop')
        self.loop.run_forever()
