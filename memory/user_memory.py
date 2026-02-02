USER_MEMORY: dict[str, dict] = {}


def get_user_memory(user_id: str) -> dict:
    return USER_MEMORY.setdefault(user_id, {})


def set_memory(user_id: str, key: str, value):
    USER_MEMORY.setdefault(user_id, {})[key] = value
