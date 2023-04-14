"""
Defines user object
"""

from typing import Optional, TypedDict


class User(TypedDict):
    """User data structure"""

    name: str
    surename: str
    company: str
    email: str
    title: str
    # There might be users without an ASN
    asn: Optional[int]
    country: str
