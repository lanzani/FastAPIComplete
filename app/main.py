from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine)


# app = FastAPI(
#     title="ChimichangApp",
#     description=description,
#     version="0.0.1",
#     terms_of_service="http://example.com/terms/",
#     contact={
#         "name": "Deadpoolio the Amazing",
#         "url": "http://x-force.example.com/contact/",
#         "email": "dp@x-force.example.com",
#     },
#     license_info={
#         "name": "Apache 2.0",
#         "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
#     },
# )


app = FastAPI()

# For public apis access (anyone can call this apis)
origins = ["*"]

# For private apis access (only listed can call this apis)
# origins = [""]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    print("ciao")
    return {"Hello": "world"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
