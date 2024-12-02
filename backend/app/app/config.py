from pathlib import Path

from pydantic import computed_field, MySQLDsn, EmailStr, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = Path(__file__).parent / ".env"
# print(DOTENV)


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    SERVER_HOST: AnyHttpUrl

    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    SECRET_KEY: str # = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 1
    EMAIL_ACTIVATION_TOKEN_EXPIRE_HOURS: int = 1
    PASSWORD_RECOVERY_MAX_ATTEMPTS: int = 3

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_USERNAME: str
    FIRST_SUPERUSER_PASSWORD: str

    EMAILS_FROM_DISPLAY_NAME: str = "Cyclity"
    EMAILS_FROM_USERNAME: str = "contact"
    EMAILS_FROM_DOMAIN: str = "cycliti.com"

    @computed_field(return_type=str)
    @property
    def DB_URI(self):
        return MySQLDsn.build(
            scheme="mysql+mysqldb",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            path=self.MYSQL_DB,
        )

    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8')


settings = Settings()
