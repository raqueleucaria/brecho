from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../.env', env_file_encoding='utf-8', extra='allow'
    )

    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_LOCAL_PORT: str
    MYSQL_DATABASE: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f'mysql+pymysql://{self.MYSQL_USERNAME}:{self.MYSQL_PASSWORD}'
            f'@{self.MYSQL_HOST}:{self.MYSQL_LOCAL_PORT}/{self.MYSQL_DATABASE}'
        )
