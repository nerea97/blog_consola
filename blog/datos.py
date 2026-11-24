# blog/datos.py
# Datos base del blog y persistencia: carga y guardado en posts.json.

import json
import os

from blog.modelos import Autor, Post
from blog.validaciones import estados_post

# posts.json se guarda en la carpeta raíz del proyecto (junto a main.py),
# así funciona aunque el programa se ejecute desde otra carpeta
CARPETA_BLOG = os.path.dirname(os.path.abspath(__file__))
CARPETA_PROYECTO = os.path.dirname(CARPETA_BLOG)
RUTA_JSON = os.path.join(CARPETA_PROYECTO, "posts.json")

# ---------- DATOS INICIALES (si todavía no existe posts.json) ----------

# Perfil del autor: diccionario con una lista anidada de redes sociales
perfil_autor = {
    "nombre": "Nerea Onieva",
    "bio": "Estudiante de IA y entusiasta de la automatización.",
    "especialidad": "Python e IA aplicada a procesos",
    "redes_sociales": ["@nerea_dev", "@nerea_python"]
}

# Etiquetas del blog: set ("Python" se repite, el set lo guarda una vez)
etiquetas_blog = {"Python", "IA", "Automatización", "Web", "Backend", "Python"}

# Posts iniciales: el 4 está incompleto y el 5 tiene datos incorrectos,
# a propósito, para probar la carga y las validaciones
posts_iniciales = [
    {
        "id": 1,
        "titulo": "Primeros pasos con Python",
        "contenido": "Cómo empezar a programar con Python desde cero.",
        "autor": perfil_autor,
        "tags": ["Python", "Principiantes"],
        "estado": estados_post[1]  # "publicado"
    },
    {
        "id": 2,
        "titulo": "Cómo la IA puede optimizar procesos logísticos",
        "contenido": "Ideas para aplicar IA en el picking y el despacho.",
        "autor": perfil_autor,
        "tags": ["IA", "Automatización", "Logística"],
        "estado": estados_post[0]  # "borrador"
    },
    {
        "id": 3,
        "titulo": "Organizando datos con diccionarios",
        "contenido": "Los diccionarios guardan datos con pares clave-valor.",
        "autor": perfil_autor,
        "tags": ["Python", "Diccionarios"],
        "estado": estados_post[2]  # "archivado"
    },
    {
        # Post incompleto: falta la clave "contenido"
        "id": 4,
        "titulo": "",
        "autor": perfil_autor,
        "tags": ["Python"],
        "estado": "publicado"
    },
    {
        # Post incorrecto: tags es texto y el estado no existe en la tupla
        "id": 5,
        "titulo": "Módulos y paquetes en Python",
        "contenido": "Cómo dividir un proyecto en varios archivos.",
        "autor": perfil_autor,
        "tags": "Python",
        "estado": "pendiente"
    }
]


# ---------- CONVERSIÓN DE DICCIONARIOS A OBJETOS ----------

def obtener_autor_principal():
    """Crea el objeto Autor que firma los posts nuevos."""
    return Autor.from_dict(perfil_autor)


def convertir_a_posts(lista_datos):
    """Convierte una lista de diccionarios en objetos Post.

    Los diccionarios incompletos se informan y se saltean.
    """
    posts = []
    for numero, datos in enumerate(lista_datos, start=1):
        try:
            posts.append(Post.from_dict(datos))
        except (ValueError, TypeError) as error:
            print(f"Aviso: el post {numero} del archivo no se cargó: {error}")
    return posts


# ---------- PERSISTENCIA EN JSON ----------

def cargar_posts(ruta=RUTA_JSON):
    """Lee posts.json y retorna una lista de objetos Post.

    Nunca cierra el programa: ante cualquier problema avisa y sigue.
    """
    if not os.path.exists(ruta):
        print("No se encontró posts.json: se cargan los posts iniciales.")
        return convertir_a_posts(posts_iniciales)

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
    except OSError as error:
        print(f"Error: no se pudo leer posts.json ({error}).")
        return []

    if contenido.strip() == "":
        print("Aviso: posts.json está vacío. El blog empieza sin posts.")
        return []

    try:
        datos = json.loads(contenido)
    except json.JSONDecodeError:
        print("Error: posts.json tiene contenido inválido (no es JSON).")
        print("El blog empieza sin posts. "
              "Si guardás, se reemplaza el archivo.")
        return []

    if not isinstance(datos, list):
        print("Error: posts.json debe contener una lista de posts.")
        return []

    posts = convertir_a_posts(datos)
    print(f"Se cargaron {len(posts)} posts desde posts.json.")
    return posts


def guardar_posts(blog, ruta=RUTA_JSON):
    """Convierte los posts del blog a diccionarios y los guarda en JSON.

    Retorna True si se guardó correctamente.
    """
    try:
        # Primero se convierte todo a texto: si algún dato no es compatible
        # con JSON, falla acá y el archivo anterior no se pierde
        texto = json.dumps(blog.to_list(), ensure_ascii=False, indent=2)
    except TypeError as error:
        print("Error: hay datos que no se pueden guardar en JSON.")
        print("Revisá que los objetos estén convertidos a diccionario.")
        print(f"Detalle: {error}")
        return False

    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(texto)
    except OSError as error:
        print(f"Error: no se pudo escribir posts.json ({error}).")
        return False

    blog.hay_cambios = False
    return True
