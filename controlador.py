"""
controlador.py
=========
Aqui se encuentra la logica del programa y donde se llama y opera con los metodos de conexion.py y models.py
"""

from modelos import Libro, Usuario
from conexion import ConexionDB

# --- Clase Controlador ---
class Controlador:
    """
    Gestiona la logica del programa y actua como intermediario entre la interfaz de usuario y la base de datos.
    """
    def __init__(self, db: ConexionDB) -> None:
        self.db = db
        self.usuario_activo: Usuario | None = None

    def hay_sesion(self) -> bool:
        """Verifica si hay un usuario activo."""
        return self.usuario_activo is not None
    
    # --- Sesion ---
    def iniciar_sesion(self, username: str, password: str) -> bool:
        """Intenta iniciar sesion con las credenciales proporcionadas."""
        usuario = self.db.autenticar(username, password)
        if usuario:
            self.usuario_activo = usuario
            return True
        return False

    def cerrar_sesion(self) -> None:
        self.usuario_activo = None
 
    def verificar_empleado(self) -> None:
        if self.usuario_activo is None or not self.usuario_activo.es_empleado():
            raise PermissionError("Se requiere sesion de empleado.")
 
    # --- Operaciones de empleado ---
 
    def agregar_libro(self, titulo, autor, genero, isbn, cantidad):
        self.verificar_empleado()
        l = Libro(titulo=titulo, autor=autor, genero=genero,
                  isbn=isbn, cantidad=cantidad)
        return self.db.agregar_libro(l)
 
    def editar_libro(self, id_libro, titulo, autor, genero, isbn, cantidad):
        self.verificar_empleado()
        libro = self.db.obtener_por_id(id_libro)
        if libro is None:
            raise ValueError(f"No existe libro con ID={id_libro}.")
        libro.titulo   = titulo
        libro.autor    = autor
        libro.genero   = genero
        libro.isbn     = isbn
        libro.cantidad = cantidad
        self.db.editar_libro(libro)
        return libro
 
    def borrar_libro(self, id_libro):
        self.verificar_empleado()
        self.db.borrar_libro(id_libro)
 
    # --- Operaciones publicas (empleado y cliente) ---
 
    def buscar_libros(self, criterio, valor):
        return self.db.buscar_libros(criterio.lower().strip(), valor.strip())
 
    def listar_libros(self):
        return self.db.obtener_todos()
 
    def obtener_libro(self, id_libro):
        return self.db.obtener_por_id(id_libro)

