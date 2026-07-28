from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/productos", tags=["Productos"])

class ProductosEntrada(BaseModel):
    nombre: str
    precio: float
    categoria: str

productos = [
	{"id": 1, "nombre": "Teclado mecanico", "precio": 120000, "categoria": "Perifericos"},
	{"id": 2, "nombre": "Mouse gamer",      "precio": 85000,  "categoria": "Perifericos"},
	{"id": 3, "nombre": "Monitor 24",       "precio": 650000, "categoria": "Pantallas"},
]

@router.get("/productos")
def ListarProductos():
    return productos

@router.post("", status_code=201)
def IngresarProductos(datos:ProductosEntrada):
    id=len(productos)+1
    nuevoProducto={
        "id" : id,
        "nombre" : datos.nombre,
        "precio" : datos.precio,
         "categorias" : datos.categoria
    }
    productos.append(nuevoProducto)
    return {"Producto Creado":nuevoProducto}

@router.put("/{id_producto}")
def ActualizarProductos(id_producto :int , datos:ProductosEntrada):
    for producto in productos:
        if producto["id"]==id_producto:
            producto["nombre"]==datos.nombre
            producto["precio"]==datos.precio
            producto["categoria"]==datos.categoria
            return{"Producto Actualizado ":producto}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.delete("/productos")
def EliminarProductos():
    return {"ELIMINAR"}