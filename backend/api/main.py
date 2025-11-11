from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import extract_routes, health_routes

app = FastAPI(title="Tile Catalog AI Backend", version="1.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health_routes.router, prefix="/api")
app.include_router(extract_routes.router, prefix="/api/extract")

@app.get("/")
def root():
    return {"message": "Welcome to Tile Catalog AI Backend"}
