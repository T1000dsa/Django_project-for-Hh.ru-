from pydantic import BaseModel


class SecretKey(BaseModel):
    key: str


class RunConfig(BaseModel):
    host:str = "127.0.0.1"
    port:int = 8000


class AppMode(BaseModel):
    DEV:str = 'DEV'
    TEST:str = 'TEST'
    PROD:str = 'PROD'


class Mode(BaseModel):
    mode:str = AppMode().DEV


class DatabaseConfig(BaseModel): 
    url: None|str = None
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    engine: str = 'django.db.backends.postgresql'
    name: str
    user: str
    password: str
    host: str = 'localhost'
    port: int = 5432

    def give_url(self):
        if self.url is None:
            self.url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
            return self.url
        else:
            return self.url

    @property
    def connection_params(self):
        return {
            'ENGINE': self.engine,
            'NAME': self.name,
            'USER': self.user,
            'PASSWORD': self.password,
            'HOST': self.host,
            'PORT': self.port,
            }
    
    def __str__(self):
        return ', '.join(f'{key}={value}' for key, value in self.connection_params.items() if key != 'PASSWORD')
    
    
class Email_Settings(BaseModel):
    email:str
    email_host:str
    email_port:int
    email_host_user:str=''
    email_password:str
    email_use_ssl:bool = True
