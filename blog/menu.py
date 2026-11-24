# blog/menu.py
# Interacción con el usuario: menú y lectura de datos con input().

from blog.validaciones import estados_post


def mostrar_menu():
    """Muestra el menú y retorna la opción elegida (o None si es texto)."""
    print("\n--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Crear nuevo post")
    print("5. Validar posts")
    print("6. Guardar posts en JSON")
    print("7. Salir")
    try:
        # int() falla si el usuario escribe texto: lo captura el except
        return int(input("Elegí una opción: "))
    except ValueError:
        print("Error: tenés que ingresar un número del 1 al 7.")
        return None


def pedir_texto(mensaje):
    """Pide un texto y retorna None si el usuario lo deja vacío."""
    texto = input(mensaje).strip()
    if texto == "":
        print("Error: no ingresaste ningún texto.")
        return None
    return texto


def pedir_datos_post():
    """Pide los datos de un post nuevo. Retorna un diccionario o None."""
    print("\n--- NUEVO POST ---")
    titulo = pedir_texto("Título: ")
    if titulo is None:
        return None
    contenido = pedir_texto("Contenido: ")
    if contenido is None:
        return None

    # Los tags se escriben separados por coma y se guardan en una lista
    texto_tags = input("Tags separados por coma (ej: Python, Web): ")
    tags = [tag.strip() for tag in texto_tags.split(",") if tag.strip()]

    print("Estados: 1. borrador  2. publicado  3. archivado")
    opcion = input("Elegí el estado (Enter = borrador): ").strip()
    if opcion == "":
        estado = estados_post[0]
    elif opcion in ("1", "2", "3"):
        estado = estados_post[int(opcion) - 1]
    else:
        print("Error: el estado tiene que ser 1, 2 o 3.")
        return None

    return {"titulo": titulo, "contenido": contenido,
            "tags": tags, "estado": estado}


def confirmar(mensaje):
    """Pregunta s/n y retorna True si el usuario responde que sí."""
    return input(mensaje).strip().lower() in ("s", "si", "sí")
