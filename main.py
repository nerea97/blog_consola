# main.py
# Punto de entrada: carga los datos, crea el Blog y coordina el menú.

from blog.datos import cargar_posts, guardar_posts, obtener_autor_principal
from blog.menu import mostrar_menu, confirmar
from blog.modelos import Blog
from blog.operaciones import (
    ver_posts,
    buscar_posts,
    filtrar_posts,
    crear_post,
    validar_posts,
    guardar,
)


def salir(blog):
    """Opción 7: ofrece guardar si hay cambios y se despide."""
    if blog.hay_cambios:
        pregunta = "Hay cambios sin guardar. ¿Guardar antes de salir? (s/n): "
        if confirmar(pregunta):
            if guardar_posts(blog):
                print("Cambios guardados en posts.json.")
    print("Gracias por usar el sistema del blog. ¡Hasta luego!")


def ejecutar():
    """Crea la instancia de Blog y mantiene el menú activo hasta salir."""
    # Al iniciar se leen los posts de posts.json y se convierten en objetos
    blog = Blog("Blog de Nerea", obtener_autor_principal(), cargar_posts())

    # Cada opción del menú llama a una función que usa los métodos del Blog
    acciones = {
        1: ver_posts,
        2: buscar_posts,
        3: filtrar_posts,
        4: crear_post,
        5: validar_posts,
        6: guardar,
    }

    while True:
        opcion = mostrar_menu()

        # Si el usuario escribió texto, se vuelve a mostrar el menú
        if opcion is None:
            continue

        if opcion in acciones:
            acciones[opcion](blog)
        elif opcion == 7:
            salir(blog)
            break
        else:
            # Número fuera del rango 1 a 7
            print("Opción inválida, intenta de nuevo")


if __name__ == "__main__":
    ejecutar()
