from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingTest(BaseSettings):
    MODE: str
    DB_TEST_HOST: str
    DB_TEST_PORT: int
    DB_TEST_NAME: str
    DB_TEST_USER: str
    DB_TEST_PASS: str

    @property
    def DB_TEST_URL(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}:"
                f"{self.DB_TEST_PORT}/{self.DB_TEST_NAME}")

    # .test.env хранится на одном уровне с .env 
    model_config = SettingsConfigDict(env_file=".test.env")



setting_test = SettingTest()
