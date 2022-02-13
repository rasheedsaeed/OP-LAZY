from typing import TypedDict


class LoginCredentials(TypedDict):
    """Login credentials schema for the Findajob.gov website"""
    email: str
    password: str
