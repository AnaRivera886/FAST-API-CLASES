from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import seguridad
from database import obtener_conexion

router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria: str



# GET - Listar productos

@router.get("")
def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            c.nombre AS categoria
        FROM productos p
        INNER JOIN categorias c ON p.categoria_id = c.id
        ORDER BY p.id
    """)

    productos = [dict(fila) for fila in cursor.fetchall()]

    conexion.close()

    return productos



# GET - Obtener producto por ID

@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            c.nombre AS categoria
        FROM productos p
        INNER JOIN categorias c ON p.categoria_id = c.id
        WHERE p.id = ?
    """, (producto_id,))

    producto = cursor.fetchone()

    conexion.close()

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return dict(producto)



# POST - Crear producto
# Requiere usuario autenticado

@router.post("", status_code=201)
def crear_producto(
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Buscar la categoría por su nombre
    cursor.execute(
        "SELECT id FROM categorias WHERE nombre = ?",
        (datos.categoria,)
    )

    categoria = cursor.fetchone()

    if categoria is None:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="La categoría no existe"
        )

    cursor.execute("""
        INSERT INTO productos (nombre, precio, categoria_id)
        VALUES (?, ?, ?)
    """, (
        datos.nombre,
        datos.precio,
        categoria["id"]
    ))

    conexion.commit()

    nuevo_id = cursor.lastrowid

    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            c.nombre AS categoria
        FROM productos p
        INNER JOIN categorias c ON p.categoria_id = c.id
        WHERE p.id = ?
    """, (nuevo_id,))

    nuevo = dict(cursor.fetchone())

    conexion.close()

    return {
        "mensaje": "Producto creado",
        "producto": nuevo,
        "creado_por": usuario["username"]
    }



# PUT - Actualizar producto
# Requiere usuario autenticado

@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Verificar que el producto exista
    cursor.execute(
        "SELECT id FROM productos WHERE id = ?",
        (producto_id,)
    )

    producto = cursor.fetchone()

    if producto is None:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    # Buscar la categoría
    cursor.execute(
        "SELECT id FROM categorias WHERE nombre = ?",
        (datos.categoria,)
    )

    categoria = cursor.fetchone()

    if categoria is None:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="La categoría no existe"
        )

    cursor.execute("""
        UPDATE productos
        SET nombre = ?, precio = ?, categoria_id = ?
        WHERE id = ?
    """, (
        datos.nombre,
        datos.precio,
        categoria["id"],
        producto_id
    ))

    conexion.commit()

    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            c.nombre AS categoria
        FROM productos p
        INNER JOIN categorias c ON p.categoria_id = c.id
        WHERE p.id = ?
    """, (producto_id,))

    actualizado = dict(cursor.fetchone())

    conexion.close()

    return {
        "mensaje": "Producto actualizado",
        "producto": actualizado
    }



# DELETE - Eliminar producto
# Solo administrador

@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    admin: dict = Depends(seguridad.requerir_admin)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.precio,
            c.nombre AS categoria
        FROM productos p
        INNER JOIN categorias c ON p.categoria_id = c.id
        WHERE p.id = ?
    """, (producto_id,))

    producto = cursor.fetchone()

    if producto is None:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto = dict(producto)

    cursor.execute(
        "DELETE FROM productos WHERE id = ?",
        (producto_id,)
    )

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Producto eliminado",
        "producto": producto
    }