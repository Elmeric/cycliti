from fastapi import FastAPI

from app.api.api_v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware

from config import settings

app = FastAPI()
#     title="Cycliti",
#     openapi_url="/openapi.json",
#     # title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )

# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

# Add CORS middleware to allow requests from the frontend
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    # os.environ.get("FRONTEND_PROTOCOL")
    # + "://"
    # + os.environ.get("FRONTEND_HOST"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(api_router)
app.include_router(api_router, prefix=settings.API_V1_STR)

# db_uri = settings.DB_URI
# print(f"Connecting to MySQL database using: {db_uri}")
