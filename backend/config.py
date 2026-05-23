import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    postgres_dsn: str = os.getenv(
        "OLAP_DSN", "postgresql://airflow:airflow@localhost:5434/olap"
    )
    keycloak_server_url: str = os.getenv("KEYCLOAK_SERVER_URL", "http://localhost:8080")
    keycloak_realm: str = os.getenv("KEYCLOAK_REALM", "reports-realm")
    keycloak_client_id: str = os.getenv("KEYCLOAK_CLIENT_ID", "reports-api")
    cors_allow_origins: tuple[str, ...] = ("http://localhost:3000",)

    @property
    def keycloak_jwks_url(self) -> str:
        base_url = self.keycloak_server_url.rstrip("/")
        return f"{base_url}/realms/{self.keycloak_realm}/protocol/openid-connect/certs"


settings = Settings()
