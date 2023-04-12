import pathlib
from typing import Optional

from pydantic import BaseSettings, conint

# pylint: disable=too-few-public-methods, no-name-in-module


class Settings(BaseSettings):
    """
    Defines application wide settings inherited from ENV.
    """

    sync_every: Optional[conint(gt=0, le=86400)] = 3600
    debug: Optional[bool] = False

    eventbrite_event: str
    eventbrite_token: str
    meetingtool_hostname: str
    meetingtool_token: str
    cache_filename: pathlib.Path
    debug: Optional[bool] = False

    class Config:
        env_prefix = "meeting_butler_"
