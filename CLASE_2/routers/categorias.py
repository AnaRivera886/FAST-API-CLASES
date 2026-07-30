from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
 
router = APIRouter(prefix="/categorias", tags=["Categorias"])
 
class CategoriaEntrada(BaseModel):
	nombre: str
 
categorias = [
	{"id": 1, "nombre": "Perifericos"},
	{"id": 2, "nombre": "Pantallas"},
	{"id": 3, "nombre": "Audio"},
]
 
# LISTAR (resuelto como ejemplo)
@router.get("")
def listar_categorias():
	return categorias
 

@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            return categoria
    raise HTTPException(status_code=404, detail="categoria no encontrado")


@router.post("", status_code=201)
def crear_categoria(datos: CategoriaEntrada):
    nuevo_id = max((p["id"] for p in categorias), default=0) + 1
    nuevo = {"id": nuevo_id, "nombre": datos.nombre,
             }
    categorias.append(nuevo)
    return {"mensaje": "Categoria creada", "categoria": nuevo}



@router.put("/{categoria_id}")
def actualizar_categoria(categoria_id: int, datos: CategoriaEntrada):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            categoria["nombre"] = datos.nombre
            return {"mensaje": "categoria actualizada", "categoria": categoria}
    raise HTTPException(status_code=404, detail="categoria no encontrado")


@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            categorias.remove(categoria)
            return {"mensaje": "categoria eliminada", "categoria": categoria}
    raise HTTPException(status_code=404, detail="categoria no encontrado")
 