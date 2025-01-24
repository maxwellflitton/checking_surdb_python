from typing import Optional, List, Dict, Any, Union
from uuid import UUID
from data.types.record_id import RecordID
from data.types.table import Table


class AsyncTemplate:

    async def connect(self, url: str, options: Optional[Dict] = None) -> None:
        """Connects to a local or remote database endpoint.

        Args:
            url: The url of the database endpoint to connect to.
            options: An object with options to initiate the connection to SurrealDB.

        Example:
            # Connect to a remote endpoint
            await db.connect('https://cloud.surrealdb.com/rpc');

            # Specify a namespace and database pair to use
            await db.connect('https://cloud.surrealdb.com/rpc', {
                namespace: 'surrealdb',
                database: 'docs',
            });
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def close(self) -> None:
        """Closes the persistent connection to the database.

        Example:
            await db.close()
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def use(self, namespace: str, database: str) -> None:
        """Switch to a specific namespace and database.

        Args:
            namespace: Switches to a specific namespace.
            database: Switches to a specific database.

        Example:
            await db.use('test', 'test')
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def signup(self, vars: Dict[str, Any]) -> str:
        """Sign this connection up to a specific authentication scope.

        Args:
            vars: Variables used in a signup query.

        Example:
            await db.signup...
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def signin(self, vars: Dict[str, Any]) -> str:
        """Sign this connection in to a specific authentication scope.

        Args:
            vars: Variables used in a signin query.

        Example:
            await db.signin...
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def invalidate(self) -> None:
        """Invalidate the authentication for the current connection.
        
        Example:
            await db.invalidate()
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def authenticate(self, token: str) -> None:
        """Authenticate the current connection with a JWT token.

        Args:
            token: The JWT authentication token.

        Example:
            await db.authenticate('insert token here')
        """
        raise NotImplementedError(f"authenticate not implemented for: {self}")

    async def let(self, key: str, value: Any) -> None:
        """Assign a value as a parameter for this connection.

        Args:
            key: Specifies the name of the variable.
            value: Assigns the value to the variable name.

        Example:
            await db.let...
        """
        raise NotImplementedError(f"let not implemented for: {self}")

    async def query(
        self, sql: str, vars: Optional[Dict[str, Any]] = None
    ) -> Union[List[dict], dict]:
        """Run a set of SurrealQL statements against the database.

        Args:
            sql: Specifies the SurrealQL statements.
            vars: Assigns variables which can be used in the query.

        Example:
            await db.query...
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def select(self, thing: str) -> Union[List[dict], dict]:
        """Select all records in a table (or other entity),
        or a specific record, in the database.

        This function will run the following query in the database:
        `select * from $thing`

        Args:
            thing: The table or record ID to select.

        Example:
            db.select...
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def create(
        self,
        thing: Union[str, RecordID, Table],
        data: Optional[Union[Union[List[dict], dict], dict]] = None,
    ) -> Union[List[dict], dict]:
        """Create a record in the database.

        This function will run the following query in the database:
        `create $thing content $data`

        Args:
            thing: The table or record ID.
            data (optional): The document / record data to insert.

        Example:
            db.create
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def update(
        self, thing: str, data: Optional[Dict[str, Any]]
    ) -> Union[List[dict], dict]:
        """Update all records in a table, or a specific record, in the database.

        This function replaces the current document / record data with the
        specified data.

        This function will run the following query in the database:
        `update $thing content $data`

        Args:
            thing: The table or record ID.
            data: The document / record data to insert.

        Example:
            Update all records in a table
                person = await db.update('person')

            Update a record with a specific ID
                record = await db.update('person:tobie', {
                    'name': 'Tobie',
                    'settings': {
                        'active': true,
                        'marketing': true,
                        },
                })
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def merge(
        self, thing: str, data: Optional[Dict[str, Any]]
    ) -> Union[List[dict], dict]:
        """Modify by deep merging all records in a table, or a specific record, in the database.

        This function merges the current document / record data with the
        specified data.

        This function will run the following query in the database:
        `update $thing merge $data`

        Args:
            thing: The table name or the specific record ID to change.
            data: The document / record data to insert.

        Example:
            Update all records in a table
                people = await db.merge('person', {
                    'updated_at':  str(datetime.datetime.utcnow())
                    })

            Update a record with a specific ID
                person = await db.merge('person:tobie', {
                    'updated_at': str(datetime.datetime.utcnow()),
                    'settings': {
                        'active': True,
                        },
                    })

        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def patch(
        self, thing: str, data: Optional[Dict[str, Any]]
    ) -> Union[List[dict], dict]:
        """Apply JSON Patch changes to all records, or a specific record, in the database.

        This function patches the current document / record data with
        the specified JSON Patch data.

        This function will run the following query in the database:
        `update $thing patch $data`

        Args:
            thing: The table or record ID.
            data: The data to modify the record with.

        Example:
            Update all records in a table
                people = await db.patch('person', [
                    { 'op': "replace", 'path': "/created_at", 'value': str(datetime.datetime.utcnow()) }])

            Update a record with a specific ID
            person = await db.patch('person:tobie', [
                { 'op': "replace", 'path': "/settings/active", 'value': False },
                { 'op': "add", "path": "/tags", "value": ["developer", "engineer"] },
                { 'op': "remove", "path": "/temp" },
            ])
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def delete(self, thing: Union[str, RecordID, Table]) -> Union[List[dict], dict]:
        """Delete all records in a table, or a specific record, from the database.

        This function will run the following query in the database:
        `delete $thing`

        Args:
            thing: The table name or a RecordID to delete.

        Example:
            Delete a specific record from a table
                await db.delete(RecordID('person', 'h5wxrf2ewk8xjxosxtyc'))
            
            Delete all records from a table
                await db.delete('person')
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    def info(self) -> dict:
        """This returns the record of an authenticated record user.

        Example:
            await db.info()
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    def insert(self, table: Union[str, Table], data: Union[List[dict], dict]) -> Union[List[dict], dict]:
        """
        Inserts one or multiple records in the database.

        This function will run the following query in the database:
        `INSERT INTO $thing $data`

        Args:
            table: The table name to insert records in to
            data: Either a single document/record or an array of documents/records to insert

        Example:
            await db.insert('person', [{ name: 'Tobie'}, { name: 'Jaime'}])

        """
        raise NotImplementedError(f"query not implemented for: {self}")
    
    def insert_relation(self, table: Union[str, Table], data: Union[List[dict], dict]) -> Union[List[dict], dict]:
        """
        Inserts one or multiple relations in the database.

        This function will run the following query in the database:
        `INSERT RELATION INTO $table $data`

        Args:
            table: The table name to insert records in to
            data: Either a single document/record or an array of documents/records to insert

        Example:
            await db.insert_relation('likes', { in: person:1, id: 'object', out: person:2})

        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def live(self, table: str, diff: bool = False) -> str:
        """Initiates a live query.

        Args:
            table: The table name to listen for changes for.
            diff: If set to true, live notifications will include
                an array of JSON Patch objects,
                rather than the entire record for each notification.

        Returns:
            UUID string.
        """
        raise NotImplementedError(f"query not implemented for: {self}")

    async def kill(self, query_uuid: Union[str, UUID]) -> None:
        """Kills a running live query by it's UUID.

        Args:
            query_uuid: The UUID of the live query you wish to kill.

        Example:
            await db.kill(UUID)

        """
        raise NotImplementedError(f"query not implemented for: {self}")
