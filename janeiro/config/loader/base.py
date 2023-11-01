from typing import Any, Union

from janeiro.constants import UNDEFINED


class ConfigLoader:
    def get_option_name(self, key: str) -> str:
        raise NotImplementedError

    def get_missing_key_error_message(self, key: str) -> str:
        raise NotImplementedError

    def get(self, key: str) -> Union[str, Any, UNDEFINED]:
        raise NotImplementedError
