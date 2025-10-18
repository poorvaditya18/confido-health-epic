from .epic_auth import EpicAuthService

def get_auth_service(source_type: str):
    source = source_type.lower()
    if source == "epic":
        return EpicAuthService()
    raise ValueError(f"unknown source type: {source_type}")