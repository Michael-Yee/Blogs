import uvicorn
from functools import lru_cache
from fastapi import Depends, FastAPI
import config


app = FastAPI()


@lru_cache()
def get_settings_development():
    return config.DevelopmentConfig()


@app.get("/")
def home(settings: config.DevelopmentConfig = Depends(get_settings_development)):
    return {"Hello": settings.MESSAGE}

if __name__ == "__main__":
    uvicorn.run("hello_world:app")
