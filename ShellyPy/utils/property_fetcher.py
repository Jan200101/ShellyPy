from functools import wraps
from typing import Optional

def property_fetcher(attr_name: Optional[str] = None, update_method: str = "update"):
    def decorator(func):
        nonlocal attr_name
        if attr_name is None:
            attr_name = f"_{func.__name__}"
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if getattr(self, attr_name) is None:
                update = getattr(self, update_method)
                if update: update()
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
