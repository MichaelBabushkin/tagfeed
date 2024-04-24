import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, auth, item, tag

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(item.router)
app.include_router(tag.router)


# Example path / route
@app.get("/")
async def root():
    return {"message": "Hello world!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
