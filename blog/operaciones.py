# blog/operaciones.py
# Acciones del menú: conectan lo que pide el usuario con los métodos del Blog
# y muestran los resultados en consola.

from blog.datos import guardar_posts
from blog.menu import pedir_texto, pedir_datos_post


def mostrar_posts(posts):
    """Imprime título, autor y estado de cada post."""
    for post in posts:
        print("-", post)  # usa el método __str__ de Post


def ver_posts(blog):
    """Opción 1: muestra todos los posts del blog."""
    posts = blog.listar_posts()
    if not posts:
        print("No hay posts cargados.")
        return
    print(f"\nPosts disponibles ({len(posts)}):")
    mostrar_posts(posts)


def buscar_posts(blog):
    """Opción 2: busca posts por título."""
    termino = pedir_texto("Buscar por titulo: ")
    if termino is None:
        return
    encontrados = blog.buscar_por_titulo(termino)
    if encontrados:
        print(f'\nPosts que contienen "{termino}":')
        mostrar_posts(encontrados)
    else:
        print(f'No se encontraron posts con "{termino}".')


def filtrar_posts(blog):
    """Opción 3: filtra posts por tag."""
    etiquetas = sorted(blog.obtener_etiquetas())
    print("Tags disponibles:", ", ".join(etiquetas))
    tag = pedir_texto("Ingresá un tag: ")
    if tag is None:
        return
    encontrados = blog.filtrar_por_tag(tag)
    if encontrados:
        print(f"\nPosts con el tag {tag}:")
        mostrar_posts(encontrados)
    else:
        print(f'No hay posts con el tag "{tag}".')


def crear_post(blog):
    """Opción 4: pide los datos y crea un nuevo objeto Post en el blog."""
    datos = pedir_datos_post()
    if datos is None:
        print("No se creó el post.")
        return
    try:
        post = blog.crear_post(**datos)
    except ValueError as error:
        print(f"Error: {error}. No se creó el post.")
        return
    print(f'Post creado con id {post.id}: "{post.titulo}".')
    print("Recordá guardar (opción 6) para que quede en posts.json.")


def validar_posts(blog):
    """Opción 5: valida cada post y muestra el resultado."""
    print("\nValidación de posts:")
    for post, es_valido, mensaje in blog.validar_posts():
        if es_valido:
            print(f"Post id {post.id}: válido")
        else:
            print(f"Post id {post.id}: error - {mensaje}")


def guardar(blog):
    """Opción 6: guarda los posts en posts.json."""
    if guardar_posts(blog):
        print(f"Se guardaron {len(blog.posts)} posts en posts.json.")
