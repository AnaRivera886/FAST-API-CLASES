from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import seguridad
from database import obtener_conexion


router = APIRouter(prefix="/categorias", tags=["Categorias"])


class CategoriaEntrada(BaseModel):
    nombre: str



# GET - Listar categorías
# Público

@router.get("")
def listar_categorias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre
        FROM categorias
        ORDER BY id
    """)

    categorias = [dict(fila) for fila in cursor.fetchall()]

    conexion.close()

    return categorias



# GET - Obtener categoría por ID
# Público

@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre
        FROM categorias
        WHERE id = ?
    """, (categoria_id,))

    categoria = cursor.fetchone()

    conexion.close()

    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    return dict(categoria)



# POST - Crear categoría
# Requiere usuario autenticado

@router.post("", status_code=201)
def crear_categoria(
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Verificar si ya existe una categoría con ese nombre
    cursor.execute(
        "SELECT id FROM categorias WHERE nombre = ?",
        (datos.nombre,)
    )

    existente = cursor.fetchone()

    if existente is not None:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="La categoria ya existe"
        )

    cursor.execute("""
        INSERT INTO categorias (nombre)
        VALUES (?)
    """, (datos.nombre,))

    conexion.commit()

    nuevo_id = cursor.lastrowid

    cursor.execute("""
        SELECT id, nombre
        FROM categorias
        WHERE id = ?
    """, (nuevo_id,))

    nueva = dict(cursor.fetchone())

    conexion.close()

    return {
        "mensaje": "Categoria creada",
        "categoria": nueva
    }



# PUT - Actualizar categoría
# Requiere usuario autenticado

@router.put("/{categoria_id}")
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Verificar que exista
    cursor.execute(
        "SELECT id FROM categorias WHERE id = ?",
        (categoria_id,)
    )

    categoria = cursor.fetchone()

    if categoria is None:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    # Actualizar
    cursor.execute("""
        UPDATE categorias
        SET nombre = ?
        WHERE id = ?
    """, (
        datos.nombre,
        categoria_id
    ))

    conexion.commit()

    cursor.execute("""
        SELECT id, nombre
        FROM categorias
        WHERE id = ?
    """, (categoria_id,))

    actualizada = dict(cursor.fetchone())

    conexion.close()

    return {
        "mensaje": "Categoria actualizada",
        "categoria": actualizada
    }



# DELETE - Eliminar categoría
# Solo administrador

@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int,
    admin: dict = Depends(seguridad.requerir_admin)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Buscar la categoría
    cursor.execute("""
        SELECT id, nombre
        FROM categorias
        WHERE id = ?
    """, (categoria_id,))

    categoria = cursor.fetchone()

    if categoria is None:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    categoria = dict(categoria)

    try:
        cursor.execute(
            "DELETE FROM categorias WHERE id = ?",
            (categoria_id,)
        )

        conexion.commit()

    except Exception:
        conexion.rollback()
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la categoria porque tiene productos asociados"
        )

    conexion.close()

    return {
        "mensaje": "Categoria eliminada",
        "categoria": categoria
    }