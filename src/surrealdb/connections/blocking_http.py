from surrealdb.connections.sync_template import SyncTemplate
from surrealdb.connections.utils_mixin import UtilsMixin


class BlockingHttpSurrealConnection(SyncTemplate, UtilsMixin):

    def __init__(self, url: str) -> None:
        pass
