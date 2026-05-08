"""
modelos.py
=========
Aqui se encuentran las clases que representan al libro y al usuario.
"""

# --- Clase de constantes ---
class Rol:
    EMPLEADO = "empleado"
    CLIENTE = "cliente"


# --- Clase Libro ---
class Libro:
    """Clase que modela el libro durante la ejecucion del programa."""

    def __init__(
            self, 
            titulo: str, 
            autor: str, 
            genero: str, 
            isbn: str,
            cantidad: int = 0,
            id: int | None = None
    ) -> None:
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.isbn = isbn
        self.cantidad = cantidad

    # Metodos auxiliares que usaremos para hablar con .db
    def to_dict(self) -> dict:
        """Convierte el libro a un diccionario."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "genero": self.genero,
            "isbn": self.isbn,
            "cantidad": self.cantidad
        }
    
    def mostrar_info(self) -> str:
        """Devuelve una cadena con la informacion del libro."""
        return f"{self.titulo} por {self.autor} (ISBN: {self.isbn}) - {self.cantidad} disponibles"
    
# Funcion auxiliares para convertir filas de la base de datos a objetos Libro

def libro_desde_fila(fila):
    # Crea un objeto Libro a partir de una fila de la base de datos
    return Libro(
        id       = fila["id"],
        titulo   = fila["titulo"],
        autor    = fila["autor"],
        genero   = fila["genero"],
        isbn     = fila["isbn"],
        cantidad = fila["cantidad"],
    )


def libro_desde_dict(data: dict) -> Libro:
    """Crea un libro usando la sintaxis de corchetes de los diccionarios."""
    return Libro(
        id=data["id"],
        titulo=data["titulo"],
        autor=data["autor"],
        genero=data["genero"],
        isbn=data["isbn"],
        cantidad=data["cantidad"]
    )


# --- Clase Usuario ---
class Usuario:
    """Clase que modela al usuario durante la ejecucion del programa."""

    def __init__(self, username: str, password: str, rol: str = Rol.EMPLEADO, id: int | None = None) -> None:
        self.id = id
        self.username = username
        self.password_hash = password
        self.rol = rol
    
    # Metodos auxiliares que usaremos para hablar con .db
    def to_dict(self) -> dict:
        """Convierte el usuario a un diccionario."""
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "rol": self.rol
        }
    
    def es_empleado(self) -> bool:
        """Devuelve True si el usuario es un empleado."""
        return self.rol == Rol.EMPLEADO
