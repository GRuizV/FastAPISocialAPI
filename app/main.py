
# 3RD PARTY IMPORTS
from fastapi import FastAPI

# LOCAL IMPORTS
from . import models, database
from .routers import post, user, auth, vote

# BUILT-IN IMPORTS
...





# Sentence to Create all tables in the database
models.Base.metadata.create_all(bind=database.engine)


# Set up the server app
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



# PATH OPERATIONS / ENDPOINTS DEFINITION

# ROOT DIRECTORY
@app.get("/")
def root():
    return {"message": "World"}
















