import typing

from tottle.api import API
from tottle.polling.routers import BotRouter
from tottle.types.responses.update import Update
from tottle.utils.logger import logger


class Polling:
    def __init__(self, api: "API"):
        self.api = api
        self.offset: int = 0
        self.stop: bool = False

        self.router: "BotRouter" = BotRouter()

    async def get_raw_updates(self) -> typing.Optional[typing.List[dict]]:
        raw_updates = await self.api.request(
            "getUpdates", {"offset": self.offset}
        )

        return raw_updates

    async def listen(self) -> typing.AsyncIterator[dict]:
        while not self.stop:
            updates = await self.get_raw_updates()

            for update in updates:
                self.offset = updates[-1]["update_id"] + 1
                yield update

    async def run(self) -> typing.NoReturn:
        async for update in self.listen():
            event = Update(**update)

            logger.debug("New event — {}", event)
            await self.router.route(event, self.api)
