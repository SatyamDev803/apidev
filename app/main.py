from fastapi import FastAPI
from app.routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# Create database tables 
# models.Base.metadata.create_all(bind=engine) # Now we longer need this command as we're working with alembic now for migration

# Initialize FastAPI app
app = FastAPI()

origins = [
    # "http://www.google.com",
    # "http://localhost",
    # "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World! This is CI CD pipeline development && Testing the Github action"}







