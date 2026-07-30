from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/clientes", tags=["Clientes"])

class ClienteEntrada(BaseModel):
    nombre: str
    correo: str
    telefono: str
    
clientes =[
    {"id": 1, "nombre": "Ana Rivera", "correo": "asriv0@gmail.com", "telefono": "3001236985"},
    
    {"id": 2, "nombre": "Pepe", "correo": "pepesas@gmail.com", "telefono": "3154287311"}, 
      
    {"id": 3, "nombre": "Sofia", "correo": "sofiaa@gmail.com", "telefono": "3116329291"}    
]

@router.get("")
def listar_clientes():
    return clientes

@router.get("/{cliente_id}")
def obtener_cliente(cliente_id: int):
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encotrado")

@router.post("", status_code=201)
def crear_cliente(datos: ClienteEntrada):
    nuevo_id = max((c["id"] for c in clientes), default=0)+1
    nuevo = {"id": nuevo_id, "nombre": datos.nombre, "correo": datos.correo, "telefono": datos.telefono}
    clientes.append(nuevo)
    return{"mensaje": "Cliente creado", "cliente": nuevo}

@router.put("/{cliente_id}")
def actualizar_cliente(cliente_id: int, datos: ClienteEntrada):
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            cliente["nombre"] = datos.nombre
            cliente["correo"] = datos.correo
            cliente["telefono"] = datos.telefono
            return {"mensaje": "Cliente actualizado", "cliente": cliente}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            clientes.remove(cliente)
            return {"mensaje": "Cliente eliminado", "cliente": cliente}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")