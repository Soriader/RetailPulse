import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class DBConfig:
    server: str = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
    database: str = os.getenv("DB_NAME", "RetailPulse")
    username: str = os.getenv("DB_USER", "sa")
    password: str = os.getenv("DB_PASSWORD", "TwojeHaslo")
    driver: str = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

    @property
    def sqlalchemy_url(self) -> str:
        return (
            f"mssql+pyodbc://{self.username}:{self.password}"
            f"@{self.server}/{self.database}"
            f"?driver={self.driver.replace(' ', '+')}"
        )