import re
from abc import abstractmethod
from typing import Union, List

import vbml

from tottle.polling.rules import ABCRule
from tottle.types.responses.update import Update
from tottle.utils.enums import ChatType

VBML_PATCHER = vbml.Patcher()


class ABCMessageRule(ABCRule):
    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass


class FromChatRule(ABCMessageRule):
    async def check(self, event: Update) -> bool:
        return event.message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)


class TextRule(ABCMessageRule):
    def __init__(
            self,
            pattern: Union[str, "vbml.Pattern", List[Union[str, "vbml.Pattern"]]],
            ignore_case: bool = False,
    ):
        if isinstance(pattern, str):
            pattern = [vbml.Pattern(pattern, flags=re.IGNORECASE if ignore_case else None)]
        elif isinstance(pattern, vbml.Pattern):
            pattern = [pattern]
        elif isinstance(pattern, list):
            pattern = [
                p if isinstance(p, vbml.Pattern)
                else vbml.Pattern(p, flags=re.IGNORECASE if ignore_case else None)
                for p in pattern
            ]
        self.patterns = pattern

    async def check(self, event: Update) -> Union[dict, bool]:
        for pattern in self.patterns:
            result = VBML_PATCHER.check(
                pattern, event.message.text
            )

            if isinstance(result, dict):
                return result
        return False
