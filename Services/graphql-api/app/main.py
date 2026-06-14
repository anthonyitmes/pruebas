from fastapi import FastAPI
from app.routers import graphql_router
import logging
from fastapi import Request

# Import schema from router for direct execution
from app.routers.graphql_router import schema
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de GraphQL",
    root_path="/",
    docs_url="/docs",          
    openapi_url="/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/graphql", graphql_router.router)

# Log registered routes for debugging
logger = logging.getLogger("uvicorn")
for r in app.routes:
    logger.info(f"Registered route: {getattr(r, 'methods', None)} {r.path}")


@app.get("/graphql")
async def graphql_get():
    return {"status": "GraphQL endpoint (GET)"}


@app.post("/graphql")
async def graphql_post(request: Request):
    try:
        payload = await request.json()
    except Exception:
        return {"errors": ["Invalid JSON"]}
    query = payload.get("query")
    if not query:
        return {"errors": ["No query provided"]}
    result = schema.execute_sync(query)
    response = {}
    if result.errors:
        response["errors"] = [str(e) for e in result.errors]
    if result.data is not None:
        response["data"] = result.data
    return response

@app.get("/", tags=["Raíz"])
def leer_raiz():
    return {
        "status": "Online",
        "servicio": "GraphQL (graphql-api)",
        "mensaje": "Servidor listo. Navega a /graphql para abrir el entorno de pruebas interactivo"
    }