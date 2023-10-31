class ConfigLoader:
    def get_option_name(self, key: str) -> str:
        raise NotImplementedError

    def get_missing_key_error_message(self, key: str) -> str:
        raise NotImplementedError
