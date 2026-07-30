from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/ventas", tags=["Ventas"])

class VentaEntrada(BaseModel):
    producto_id: int
    cliente_id: int
    cantidad: int


ventas = [
    {"id": 1, "producto_id": 1, "cliente_id": 1, "cantidad": 2},
    {"id": 2, "producto_id": 3, "cliente_id": 2, "cantidad": 1},
    {"id": 3, "producto_id": 2, "cliente_id": 3, "cantidad": 3},
]


@router.get("")
def listar_ventas():
    return ventas

@router.get("/{venta_id}")
def obtener_venta(venta_id: int):
    for venta in ventas:
        if venta["id"] == venta_id:
            return venta
    raise HTTPException(status_code=404, detail="Venta no encontrada")

@router.post("", status_code=201)
def crear_venta(datos: VentaEntrada):
    nuevo_id = max((v["id"] for v in ventas), default=0) + 1
    nueva = {"id": nuevo_id, "producto_id": datos.producto_id,
             "cliente_id": datos.cliente_id, "cantidad": datos.cantidad}
    ventas.append(nueva)
    return {"mensaje": "Venta creada", "venta": nueva}

@router.put("/{venta_id}")
def actualizar_venta(venta_id: int, datos: VentaEntrada):
    for venta in ventas:
        if venta["id"] == venta_id:
            venta["producto_id"] = datos.producto_id
            venta["cliente_id"] = datos.cliente_id
            venta["cantidad"] = datos.cantidad
            return {"mensaje": "Venta actualizada", "venta": venta}
    raise HTTPException(status_code=404, detail="Venta no encontrada")

@router.delete("/{venta_id}")
def eliminar_venta(venta_id: int):
    for venta in ventas:
        if venta["id"] == venta_id:
            ventas.remove(venta)
            return {"mensaje": "Venta eliminada", "venta": venta}
    raise HTTPException(status_code=404, detail="Venta no encontrada")