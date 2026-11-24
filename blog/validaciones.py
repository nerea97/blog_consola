# blog/validaciones.py
# Reglas lógicas del sistema: estados válidos y validación de posts.
# Este módulo no importa nada del paquete para evitar imports circulares.

# Estados posibles de un post: tupla con valores fijos del sistema
estados_post = ("borrador", "publicado", "archivado")

# Claves que debe tener un post guardado en JSON
CLAVES_POST = ("id", "titulo", "contenido", "autor", "tags", "estado")


def validar_datos_post(datos):
    """Revisa un diccionario leído del JSON antes de convertirlo en objeto.

    Retorna una lista de errores (vacía si el diccionario está completo).
    """
    if not isinstance(datos, dict):
        return ["no es un diccionario"]

    errores = []
    # Se verifica con "in" que existan las claves antes de usarlas
    for clave in CLAVES_POST:
        if clave not in datos:
            errores.append(f'falta la clave "{clave}"')

    autor = datos.get("autor")
    if "autor" in datos:
        if not isinstance(autor, dict):
            errores.append('"autor" no es un diccionario')
        elif "nombre" not in autor:
            errores.append('el autor no tiene la clave "nombre"')
    return errores


def validar_post(post):
    """Valida un objeto Post. Retorna (True, "válido") o (False, errores)."""
    errores = []

    # getattr() evita un AttributeError si al objeto le falta un atributo
    titulo = getattr(post, "titulo", None)
    contenido = getattr(post, "contenido", None)
    autor = getattr(post, "autor", None)
    tags = getattr(post, "tags", None)
    estado = getattr(post, "estado", None)

    if not isinstance(titulo, str) or titulo.strip() == "":
        errores.append("el título está vacío")
    if not isinstance(contenido, str) or contenido.strip() == "":
        errores.append("el contenido está vacío")
    if not getattr(autor, "nombre", ""):
        errores.append("el autor no tiene nombre")
    if not isinstance(tags, list):
        errores.append('"tags" no es una lista')
    if estado not in estados_post:
        errores.append(f'el estado "{estado}" no es válido')

    if errores:
        return False, "; ".join(errores)
    return True, "válido"
