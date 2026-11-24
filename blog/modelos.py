# blog/modelos.py
# Clases principales del sistema: Autor, Post y Blog.

from blog.validaciones import estados_post, validar_datos_post, validar_post


class Autor:
    """Persona autora de los posts del blog."""

    def __init__(self, nombre, bio="", especialidad="", redes_sociales=None):
        self.nombre = nombre
        self.bio = bio
        self.especialidad = especialidad
        # Se crea una lista nueva si no se recibe ninguna
        self.redes_sociales = redes_sociales if redes_sociales else []

    def to_dict(self):
        """Convierte el autor en un diccionario compatible con JSON."""
        return {
            "nombre": self.nombre,
            "bio": self.bio,
            "especialidad": self.especialidad,
            "redes_sociales": list(self.redes_sociales),
        }

    @classmethod
    def from_dict(cls, datos):
        """Crea un Autor a partir de un diccionario (por ejemplo, del JSON)."""
        if not isinstance(datos, dict) or "nombre" not in datos:
            raise ValueError('el autor no tiene la clave "nombre"')
        return cls(
            nombre=datos["nombre"],
            bio=datos.get("bio", ""),
            especialidad=datos.get("especialidad", ""),
            redes_sociales=datos.get("redes_sociales", []),
        )

    def __str__(self):
        return self.nombre


class Post:
    """Publicación del blog. Su autor es un objeto Autor (composición)."""

    def __init__(self, id, titulo, contenido, autor, tags, estado="borrador"):
        # El autor tiene que ser una instancia de Autor, no un texto
        if not isinstance(autor, Autor):
            raise TypeError("el autor debe ser una instancia de Autor")
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.autor = autor
        self.tags = tags
        self.estado = estado

    def tiene_tag(self, tag):
        """Indica si el post tiene el tag (sin importar mayúsculas)."""
        if not isinstance(self.tags, list):
            return False
        return tag.lower() in [str(t).lower() for t in self.tags]

    def validar(self):
        """Valida el post usando las reglas de validaciones.py."""
        return validar_post(self)

    def to_dict(self):
        """Convierte el post (y su autor) en un diccionario para el JSON."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": self.autor.to_dict(),
            "tags": self.tags,
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, datos):
        """Crea un Post desde un diccionario. Falla si está incompleto."""
        errores = validar_datos_post(datos)
        if errores:
            raise ValueError("; ".join(errores))
        return cls(
            id=datos["id"],
            titulo=datos["titulo"],
            contenido=datos["contenido"],
            autor=Autor.from_dict(datos["autor"]),
            tags=datos["tags"],
            estado=datos["estado"],
        )

    def __str__(self):
        titulo = self.titulo or "(sin título)"
        return f"{titulo} | Autor: {self.autor} | Estado: {self.estado}"


class Blog:
    """Centraliza la colección de posts y las operaciones sobre ella."""

    def __init__(self, nombre, autor, posts=None):
        self.nombre = nombre
        self.autor = autor  # autor que firma los posts nuevos
        self.posts = posts if posts else []  # lista de objetos Post
        self.hay_cambios = False  # True si hay cambios sin guardar

    def obtener_posts(self):
        """Retorna una copia de la lista de posts."""
        return list(self.posts)

    def listar_posts(self):
        """Retorna todos los posts del blog."""
        return self.obtener_posts()

    def buscar_por_titulo(self, termino):
        """Retorna los posts cuyo título contiene el término."""
        termino = termino.lower()
        return [
            post for post in self.posts
            if isinstance(post.titulo, str)
            and termino in post.titulo.lower()
        ]

    def filtrar_por_tag(self, tag):
        """Retorna los posts que tienen el tag indicado."""
        return [post for post in self.posts if post.tiene_tag(tag)]

    def obtener_etiquetas(self):
        """Retorna un set con todas las etiquetas usadas (sin repetidos)."""
        etiquetas = set()
        for post in self.posts:
            if isinstance(post.tags, list):
                etiquetas.update(post.tags)
        return etiquetas

    def siguiente_id(self):
        """Calcula el id del próximo post."""
        ids = [post.id for post in self.posts if isinstance(post.id, int)]
        return max(ids, default=0) + 1

    def crear_post(self, titulo, contenido, tags, estado="borrador"):
        """Crea un Post, lo agrega al blog y lo retorna."""
        if not titulo.strip() or not contenido.strip():
            raise ValueError("el título y el contenido son obligatorios")
        if estado not in estados_post:
            raise ValueError(f'el estado "{estado}" no es válido')
        post = Post(self.siguiente_id(), titulo.strip(), contenido.strip(),
                    self.autor, tags, estado)
        self.posts.append(post)
        self.hay_cambios = True
        return post

    def validar_posts(self):
        """Retorna (post, es_valido, mensaje) por cada post."""
        resultados = []
        for post in self.posts:
            es_valido, mensaje = post.validar()
            resultados.append((post, es_valido, mensaje))
        return resultados

    def to_list(self):
        """Convierte todos los posts en una lista de diccionarios."""
        return [post.to_dict() for post in self.posts]
