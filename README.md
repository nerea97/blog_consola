# Blog de consola en Python

Sistema de blog por consola desarrollado para la Diplomatura en Inteligencia
Artificial - Python (Coderhouse).

El programa permite ver, buscar, filtrar, crear y validar publicaciones desde
un menú interactivo. Desde la **Preentrega 6** el sistema está modelado con
**Programación Orientada a Objetos** y los posts se guardan en un archivo
**`posts.json`**, así que se conservan entre una ejecución y otra.

**Autora:** Nerea Onieva

## Cómo ejecutarlo

Requisito: tener Python 3 instalado. No usa librerías externas (solo el módulo
`json`, que viene con Python).

1. Abrí una terminal en la carpeta raíz del proyecto (donde está `main.py`).
2. Ejecutá:

```bash
python main.py
```

Al iniciar, el programa lee `posts.json` y muestra cuántos posts cargó.

## Funcionalidades del menú

```
--- MENU DEL BLOG ---
1. Ver todos los posts
2. Buscar por titulo
3. Filtrar por tag
4. Crear nuevo post
5. Validar posts
6. Guardar posts en JSON
7. Salir
```

| Opción | Qué hace |
|---|---|
| 1. Ver todos los posts | Muestra título, autor y estado de cada post. |
| 2. Buscar por titulo | Muestra los posts cuyo título contiene el término. No distingue mayúsculas de minúsculas. |
| 3. Filtrar por tag | Muestra los tags disponibles y los posts que tienen el tag elegido. No distingue mayúsculas de minúsculas. |
| 4. Crear nuevo post | Pide título, contenido, tags y estado, y crea un nuevo objeto `Post` dentro del blog. |
| 5. Validar posts | Revisa cada post e indica si es válido o qué errores tiene. |
| 6. Guardar posts en JSON | Guarda todos los posts en `posts.json`. |
| 7. Salir | Si hay cambios sin guardar, pregunta si querés guardarlos. Después se despide. |

## Estructura del proyecto

```
blog_consola/
│
├── main.py
├── README.md
├── posts.json
│
└── blog/
    ├── __init__.py
    ├── datos.py
    ├── menu.py
    ├── modelos.py
    ├── operaciones.py
    └── validaciones.py
```

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Punto de entrada. Carga los posts, crea la instancia de `Blog` y coordina el menú dentro de `if __name__ == "__main__":`. |
| `posts.json` | Archivo donde se guardan los posts. |
| `blog/modelos.py` | Clases `Autor`, `Post` y `Blog`. |
| `blog/datos.py` | Datos iniciales y persistencia: `cargar_posts()` y `guardar_posts()`. |
| `blog/menu.py` | Interacción con el usuario: menú (con `try-except`), pedido de textos y de los datos de un post nuevo. |
| `blog/operaciones.py` | Acciones de cada opción del menú: llaman a los métodos de `Blog` y muestran los resultados. |
| `blog/validaciones.py` | Reglas del sistema: estados válidos (`estados_post`), validación de diccionarios del JSON y de objetos `Post`. |

## Clases principales (`blog/modelos.py`)

### `Autor`
Representa a la persona que escribe los posts.

- Atributos: `nombre`, `bio`, `especialidad`, `redes_sociales`.
- `to_dict()`: convierte el autor en diccionario.
- `Autor.from_dict(datos)`: crea un autor desde un diccionario. Si falta
  `nombre`, lanza un `ValueError` con un mensaje claro.

### `Post`
Representa una publicación.

- Atributos: `id`, `titulo`, `contenido`, `autor`, `tags`, `estado`.
- **Composición:** el atributo `autor` es un objeto `Autor`. Si se le pasa un
  texto, el constructor lanza un `TypeError`.
- `tiene_tag(tag)`: indica si el post tiene un tag, sin importar mayúsculas.
- `validar()`: valida el post con las reglas de `validaciones.py`.
- `to_dict()`: convierte el post en diccionario (incluido su autor).
- `Post.from_dict(datos)`: crea un post desde un diccionario. Si está
  incompleto, lanza un `ValueError` que explica qué falta.

### `Blog`
Centraliza la lógica del sistema. Su atributo `posts` es una **lista de
objetos `Post`**.

- `listar_posts()` y `obtener_posts()`: retornan los posts.
- `buscar_por_titulo(termino)`: búsqueda parcial con `.lower()`.
- `filtrar_por_tag(tag)`: filtrado con `.lower()`.
- `obtener_etiquetas()`: retorna un `set` con los tags usados, sin repetidos.
- `crear_post(titulo, contenido, tags, estado)`: crea un `Post` firmado por el
  autor del blog, le asigna el siguiente `id` y lo agrega a la lista.
- `validar_posts()`: valida todos los posts.
- `to_list()`: convierte todos los posts en una lista de diccionarios.
- `hay_cambios`: indica si hay posts nuevos sin guardar.

## Cómo funciona la persistencia con JSON

JSON no puede guardar objetos de Python directamente, por eso los datos se
convierten en los dos sentidos:

```
Guardar:  Blog → to_list() → Post.to_dict() → Autor.to_dict() → posts.json
Cargar:   posts.json → lista de diccionarios → Post.from_dict() → objetos Post → Blog
```

**Al iniciar** (`cargar_posts()` en `datos.py`):

1. Se lee `posts.json` con el módulo `json`.
2. Cada diccionario se convierte en un objeto `Post` (con su objeto `Autor`).
3. Con esa lista de objetos, `main.py` crea la instancia de `Blog`.

**Al guardar** (opción 6, o al salir si hay cambios):

1. `Blog.to_list()` convierte cada `Post` y su `Autor` en diccionarios.
2. `guardar_posts()` los escribe en `posts.json` con `json.dumps(...)`.

`posts.json` se guarda siempre en la carpeta raíz del proyecto, junto a
`main.py`.

### Manejo de errores

El programa nunca se cierra por un problema con los datos:

| Situación | Qué hace el programa |
|---|---|
| `posts.json` no existe | Carga los posts iniciales de `datos.py`. Al guardar se crea el archivo. |
| `posts.json` está vacío | Avisa y empieza con el blog vacío. |
| `posts.json` tiene contenido inválido | Avisa y empieza con el blog vacío. |
| Un post del JSON está incompleto | Avisa qué le falta y no lo carga. El resto se carga normalmente. |
| Un dato no se puede convertir a JSON | Avisa el error y no toca el archivo anterior. |
| Opción del menú con texto o fuera de rango | Muestra un aviso y vuelve al menú. |
| Campos vacíos al crear un post | Avisa y no crea el post. |

## Datos de prueba

`posts.json` trae 5 posts. Dos tienen errores a propósito para probar la
carga y la validación:

- **Post 4:** le falta la clave `contenido`, así que no se carga y el
  programa lo avisa al iniciar. Si guardás, ese post no se vuelve a escribir.
- **Post 5:** se carga, pero `tags` es un texto en lugar de una lista y el
  estado `pendiente` no es válido. La opción **5. Validar posts** lo detecta.

## Cambios respecto a la Preentrega 5

- Se agregó `blog/modelos.py` con las clases `Autor`, `Post` y `Blog`.
- Los posts dejaron de ser diccionarios sueltos: ahora son objetos `Post` con
  un objeto `Autor`, y la lógica de listar, buscar y filtrar pasó a los
  métodos de la clase `Blog`.
- Se agregó persistencia: `datos.py` carga y guarda los posts en
  `posts.json`, con conversión entre objetos y diccionarios.
- El menú suma **Crear nuevo post** y **Guardar posts en JSON**, y al salir
  avisa si hay cambios sin guardar.
- `operaciones.py` ahora contiene las acciones del menú, que llaman a los
  métodos de `Blog`.
- `validaciones.py` valida tanto los diccionarios leídos del JSON como los
  objetos `Post`.
- `main.py` crea la instancia de `Blog` y conecta cada opción del menú con
  su acción.
