from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import crear_tablas, sembrar_datos
from routers import productos, categorias, clientes, ventas, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear las tablas y cargar los datos iniciales
    crear_tablas()
    sembrar_datos()

    yield


app = FastAPI(
    title="API de la Tienda",
    lifespan=lifespan
)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API de la Tienda funcionando. Visita /docs"}


app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(clientes.router)
app.include_router(ventas.router)
app.include_router(auth.router)