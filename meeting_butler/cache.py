"""
Local persistent caches
"""

import datetime
import json
import logging
import os
import sqlite3
from tempfile import gettempdir
from typing import Any, Optional, Tuple

LOGGER = logging.getLogger(__name__)


class Cache:
    """
    SQLite backed dict like object. Connects to the databse specified at filename.

     Arguments:
    ---------
    filename: Optional[os.PathLike]
        Filename. If False, a file named meeting_butle.db is created in the temp directory
        Default: False
    reset: Optional[bool]
        If true, deletes the database before starting. Default: False
    """
    def __init__(
        self, filename: Optional[os.PathLike] = False, reset: Optional[bool] = False
    ) -> None:
        self.filename = filename or os.path.join(gettempdir(), "meeting_butler.db")

        if reset:
            try:
                os.unlink(self.filename)
            except FileNotFoundError:
                pass

        self._connection = sqlite3.connect(self.filename)
        self._cursor = self._connection.cursor()

        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS data (key TEXT PRIMARY KEY, value JSON, datetime TEXT);"
        )

        self._connection.set_trace_callback(LOGGER.debug)

        LOGGER.debug("Connected to database: %s", self.filename)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.save()
        self.close()

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Sets key to value into the SQLite database

        Arguments:
        ----------
        key: str
           Cache key
        value: Any
           Any pickable value
        """
        if not isinstance(key, str):
            raise TypeError(f"Key must be str, not {type(key)}")

        value = json.dumps(value)
        now = datetime.datetime.now(datetime.timezone.utc)
        self._cursor.execute("INSERT OR REPLACE INTO data VALUES(?,?,?);", (key, value, now))

    def close(self) -> None:
        """
        Disconnects from the SQLite database
        """
        self._connection.close()
        LOGGER.debug("Disconnected from database: %s", self.filename)

    def __contains__(self, key: str) -> bool:
        """
        Returns True if key is in the SQLite database, False otherwise

        Arguments:
        ----------
        key: str
            The key to look for

        Returns:
        -------
        bool: True if the key is in the databse, False othwerise
        """
        result = self._cursor.execute("SELECT key FROM data WHERE key = ?", (key,))
        return bool(result.fetchone())

    def __delitem__(self, key: str) -> None:
        """
        Deletees key fromthe SQLite database

        Arguments:
        ----------
        key: str
           Cache key
        """
        result = self._cursor.execute("DELETE FROM data WHERE key = ?", (key,))
        if not result.rowcount:
            raise KeyError(key)

    def __getitem__(self, key) -> Any:
        """
        Gets the value for key as stored in the SQLite database

        Arguments:
        ----------
        key: str
           Cache key

        Returns:
        -------
        Any: value as saved into the SQLite database
        """
        result = self._cursor.execute("SELECT value FROM data WHERE key = ?", (key,))
        try:
            serialized = next(iter(result.fetchone()))
        except TypeError as error:
            raise KeyError(key) from error

        return json.loads(serialized)

    def keys(self) -> list[str]:
        """
        Returns the list of the keys as saved in the SQLite database

        Returns:
        -------
        list[str]: Keys
        """
        result = self._cursor.execute("SELECT key FROM data")
        return [next(iter(cols)) for cols in result.fetchall()]

    def values(self) -> list[Any]:
        """
        Returns the list of the values as saved in the SQLite database

        Returns:
        -------
        list[Any]: Values
        """
        result = self._cursor.execute("SELECT value FROM data")
        return [json.loads(next(iter(cols))) for cols in result.fetchall()]

    def items(self) -> list[Tuple]:
        """
        Returns a list of (key, value) tuples

        Returns:
        -------
        list[Tuple]: (key, value)
        """
        result = self._cursor.execute("SELECT key, value FROM data")
        return [(key, json.loads(value)) for key, value in result.fetchall()]

    def save(self) -> None:
        """
        Write data do disk
        """
        self._connection.commit()
