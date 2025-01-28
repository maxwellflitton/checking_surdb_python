from surrealdb.connections.blocking_ws import BlockingWsSurrealConnection
from surrealdb.connections.blocking_http import BlockingHttpSurrealConnection
from surrealdb.connections.url import Url, UrlScheme


class SurrealDBMeta(type):
    def __call__(cls, *args, **kwargs):
        # Ensure `url` is provided as either an arg or kwarg
        if len(args) > 0:
            url = args[0]  # Assume the first positional argument is `url`
        else:
            url = kwargs.get("url")

        if url is None:
            raise ValueError("The 'url' parameter is required to initialise SurrealDB.")

        constructed_url = Url(url)


        # Extract `max_size` with a default if not explicitly provided
        max_size = kwargs.get("max_size", 2 ** 20)

        if constructed_url.scheme == UrlScheme.HTTP or constructed_url.scheme == UrlScheme.HTTPS:
            return BlockingHttpSurrealConnection(url=url)
        elif constructed_url.scheme == UrlScheme.WS or constructed_url.scheme == UrlScheme.WSS:
            return BlockingWsSurrealConnection(url=url, max_size=max_size)
        else:
            raise ValueError(f"Unsupported protocol in URL: {url}. Use 'ws://' or 'http://'.")

class SurrealDB(metaclass=SurrealDBMeta):

    def __init__(self, url: str, max_size: int = 2 ** 20) -> None:
        pass

