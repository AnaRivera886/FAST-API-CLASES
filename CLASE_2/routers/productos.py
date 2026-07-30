from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
 
router = APIRouter(prefix="/productos", tags=["Productos"])
 
class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria: str
 

productos = [
    {"id": 1, "nombre": "Teclado mecanico", "precio": 120000, "categoria": "Perifericos"},
    {"id": 2, "nombre": "Mouse gamer",      "precio": 85000,  "categoria": "Perifericos"},
    {"id": 3, "nombre": "Monitor 24",       "precio": 650000, "categoria": "Pantallas"},
]


@router.get("")
def listar_productos():
    return productos
 
@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")
 
@router.post("", status_code=201)
def crear_producto(datos: ProductoEntrada):
    nuevo_id = max((p["id"] for p in productos), default=0) + 1
    nuevo = {"id": nuevo_id, "nombre": datos.nombre,
             "precio": datos.precio, "categoria": datos.categoria}
    productos.append(nuevo)
    return {"mensaje": "Producto creado", "producto": nuevo}
 
@router.put("/{producto_id}")
def actualizar_producto(producto_id: int, datos: ProductoEntrada):
    for producto in productos:
        if producto["id"] == producto_id:
            producto["nombre"] = datos.nombre
            producto["precio"] = datos.precio
            producto["categoria"] = datos.categoria
            return {"mensaje": "Producto actualizado", "producto": producto}
    raise HTTPException(status_code=404, detail="Producto no encontrado")
 
@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            productos.remove(producto)
            return {"mensaje": "Producto eliminado", "producto": producto}
    raise HTTPException(status_code=404, detail="Producto no encontrado")


