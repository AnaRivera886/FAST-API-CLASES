from fastapi import FastAPI
from routers import productos

app = FastAPI(
    title = "API de la Tienda",
    description = "CRUD de productos y categorias organizacion en varios archivos",
    version = "2.0.0",
)

app.include_router(productos.router)

@app.get("/", tags={"Inicio"})
def inicio():
    return{"Mensaje:" "API Tienda"}