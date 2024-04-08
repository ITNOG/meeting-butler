"""
Methods to read user related settings
"""

# pylint: disable=too-few-public-methods, no-name-in-module

import pathlib
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Defines application wide settings inherited from ENV.
    """

    sync_every: Optional[str] = 3600
    debug: Optional[bool] = True

    meetingtool_hostname: str
    meetingtool_token: str
    cache_filename: pathlib.Path
    data_source: Optional[Literal["eventbrite", "formbuilder"]] = "formbuilder"
    eventbrite_event: Optional[str] = ""
    eventbrite_token: Optional[str] = ""
    formbuilder_url: Optional[str] = ""

    model_config = SettingsConfigDict(
        env_prefix="meeting-butler_",
        env_file="meeting-butler.conf",
        env_file_encoding="utf-8",
    )
