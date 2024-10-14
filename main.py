from fastapi import FastAPI
from database import Base, engine
from routes import auth, tasks

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth.router)
app.include_router(tasks.router)
