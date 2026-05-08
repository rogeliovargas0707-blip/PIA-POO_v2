"""
Conexion.py
=========
Aqui se realiza la conexion con la base de datos
Solo aqui se puede acceder a la base de datos y solo se importa sqlite3 aqui
"""
import sqlite3

from modelos import Libro, Rol, libro_desde_dict, libro_desde_fila, Usuario

# --- Path del archivo de la base de datos ---
db_path = "libreria_acme.db"

# --- Clase ConexionDB ---
class ConexionDB:
    """Gestiona la conexion a SQLite3 y expone metodos CRUD para los libros y usuarios."""
    
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.conn: sqlite3.Connection | None = None
    
    # --- Metodos de gestion de conexion ---
    def conectar(self) -> None:
        """Abre la conexion a a la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            
            self.crear_tablas()
            self.seed_admin()
            
        except sqlite3.Error as e:
            raise e
    
    def cerrar(self) -> None:
        """Cierra la conexion a la base de datos."""
        if self.conn:
            self.conn.close()
            self.conn = None

    # --- Metodos auxiliares para inicializacion de la base de datos ---
    def crear_tablas(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS libros (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo   TEXT    NOT NULL,
            autor    TEXT    NOT NULL,
            genero   TEXT    NOT NULL DEFAULT '',
            isbn     TEXT    NOT NULL UNIQUE,
            cantidad INTEGER NOT NULL DEFAULT 0
        );
 
        CREATE TABLE IF NOT EXISTS usuarios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL,
            rol      TEXT    NOT NULL DEFAULT 'empleado'
        );
        """
        self.conn.executescript(sql)
        self.conn.commit()

    def seed_admin(self) -> None:
        """Agrega a un usuario admin por defecto si no existe.
        Lo que sera verdadero durante la primera ejecucion del programa."""
        cur = self.conn.execute("SELECT COUNT(*) FROM usuarios")
        if cur.fetchone()[0] == 0:
            self.conn.execute(
                "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                ("admin", "admin123", Rol.EMPLEADO)
            )
            self.conn.commit()
            print("Usuario 'admin' creado con password 'admin123'.")        

    # --- Operaciones CRUD para libros ---
    def agregar_libro(self, libro: Libro) -> int | None:
        """Agrega un nuevo libro a la base de datos."""
        sql = """
        INSERT INTO libros (titulo, autor, genero, isbn, cantidad)
        VALUES (:titulo, :autor, :genero, :isbn, :cantidad);
        """
        try:
            cur = self.conn.execute(sql, libro.to_dict())
            self.conn.commit()

            # Asignamos el ID generado al libro
            libro.id = cur.lastrowid
            return libro.id
        
        except sqlite3.IntegrityError as e:
            print(f"Error: ya existe un libro con ISBN '{libro.isbn}'.")
            return None
        
        except sqlite3.Error as e:
            print(f"Error al agregar libro: {e}")
            return None        

    def editar_libro(self, libro: Libro) -> None:
        sql = """
        UPDATE libros
           SET titulo=:titulo, autor=:autor, genero=:genero,
               isbn=:isbn, cantidad=:cantidad
         WHERE id=:id
        """
        try:
            cur = self.conn.execute(sql, libro.to_dict())
            self.conn.commit()
            if cur.rowcount == 0:
                print(f"No existe libro con ID={libro.id}.")
        except sqlite3.IntegrityError:
            print("Error: ISBN duplicado.")
        except sqlite3.Error as e:
            print(f"Error al editar libro: {e}")
    
    
    def borrar_libro(self, libro_id: int) -> None:
        """Elimina un libro de la base de datos por su ID."""
        try:
            cur = self.conn.execute("DELETE FROM libros WHERE id = ?;", (libro_id,))
            self.conn.commit()
            if cur.rowcount == 0:
                print(f"No se encontró un libro con ID {libro_id} para eliminar.")
        
        except sqlite3.Error as e:
            print(f"Error al eliminar libro: {e}")
            raise e
        
    def buscar_libros(self, criterio: str, valor: str) -> list[Libro]:
        """Obtiene una lista de todos los libros en la base de datos."""
        columnas_validas = ["titulo", "autor", "genero", "isbn"]
        if criterio not in columnas_validas:
            print(f"Criterio de búsqueda inválido: '{criterio}'.")
            return []
        sql = f"SELECT * FROM libros WHERE {criterio} LIKE ? COLLATE NOCASE;"
        try:
            cur = self.conn.execute(sql, (f"%{valor}%",))
            return [libro_desde_fila(fila) for fila in cur.fetchall()]
        
        except sqlite3.Error as e:
            print(f"Error al buscar libros: {e}")
            return []

    def obtener_todos(self) -> list[Libro]:
        """Obtiene una lista de todos los libros en la base de datos."""
        try:
            cur = self.conn.execute("SELECT * FROM libros ORDER BY titulo COLLATE NOCASE")
            return [libro_desde_fila(f) for f in cur.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al obtener libros: {e}")
            return []
    
    def obtener_por_id(self, id_libro):
        """Obtiene un libro por su ID.""" #Tal vez me lo borre
        try:
            cur = self.conn.execute("SELECT * FROM libros WHERE id=?", (id_libro,))
            fila = cur.fetchone()
            if fila:
                return libro_desde_fila(fila)
            return None
        except sqlite3.Error as e:
            print(f"Error al obtener libro: {e}")
            return None

    # --- Autenticacion de usuarios ---
    def autenticar(self, username: str, password: str) -> Usuario | None:
        try:
            cur = self.conn.execute(
                "SELECT * FROM usuarios WHERE username=? AND password=?",
                (username, password)
            )
            fila = cur.fetchone()
            if fila:
                return Usuario(
                    id       = fila["id"],
                    username = fila["username"],
                    password = fila["password"],
                    rol      = fila["rol"],
                )
            return None
        except sqlite3.Error as e:
            print(f"Error al autenticar: {e}")
            return None



    


    