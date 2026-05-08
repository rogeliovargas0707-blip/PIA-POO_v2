# gui.py
# Vista de TERMINAL para la Libreria ACME.
#
# COMO MIGRAR A TKINTER:
#   1. Crea gui_tkinter.py con una clase GUITkinter
#   2. La clase debe tener el metodo publico: iniciar()
#   3. En main.py cambia las dos lineas marcadas con (CAMBIAR AQUI)


# --- Helpers de consola ---

def pedir(prompt, obligatorio=True):
    while True:
        valor = input(f"  {prompt}: ").strip()
        if valor or not obligatorio:
            return valor
        print("  Advertencia: campo obligatorio.")

def pedir_int(prompt, minimo=0):
    while True:
        try:
            valor = int(pedir(prompt))
            if valor < minimo:
                print(f"  Advertencia: el valor minimo es {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Advertencia: ingresa un numero entero valido.")

def mostrar_libros(libros):
    if not libros:
        print("\n  (Sin resultados)\n")
        return
    print(f"\n  {'ID':<5} {'Titulo':<28} {'Autor':<20} {'Genero':<12} {'ISBN':<15} Stock")
    print("  " + "-" * 85)
    for l in libros:
        print(f"  {str(l.id):<5} {l.titulo[:27]:<28} {l.autor[:19]:<20} "
              f"{l.genero[:11]:<12} {l.isbn[:14]:<15} {l.cantidad}")
    print()

def pausa():
    input("  Presiona ENTER para continuar...")


# --- Vista principal ---

class GUITerminal:

    def __init__(self, controlador):
        self.ctrl = controlador

    def iniciar(self):
        print("\n" + "=" * 50)
        print("  Libreria ACME - Control de Stock")
        print("=" * 50)
        self.menu_inicio()

    def menu_inicio(self):
        while True:
            print("\n  Como deseas acceder?\n")
            print("  1 - Empleado (requiere contrasena)")
            print("  2 - Cliente  (solo busqueda)")
            print("  0 - Salir")
            opcion = pedir("Opcion")

            if opcion == "1":
                if self.login():
                    self.menu_empleado()
            elif opcion == "2":
                self.menu_cliente()
            elif opcion == "0":
                print("\n  Hasta luego.\n")
                break
            else:
                print("  Opcion no valida.")

    def login(self):
        print("\n  -- Inicio de sesion --")
        try:
            user = pedir("Usuario")
            pw   = pedir("Contrasena")
            if self.ctrl.iniciar_sesion(user, pw):
                print(f"\n  Bienvenido, {self.ctrl.usuario_activo.username}.")
                pausa()
                return True
            else:
                print("\n  Usuario o contrasena incorrectos.")
                pausa()
                return False
        except Exception as e:
            print(f"\n  Error inesperado: {e}")
            pausa()
            return False

    def menu_empleado(self):
        while True:
            usuario = self.ctrl.usuario_activo
            print(f"\n  -- Menu Empleado: {usuario.username} --\n")
            print("  1 - Agregar libro")
            print("  2 - Editar libro")
            print("  3 - Borrar libro")
            print("  4 - Buscar libros")
            print("  5 - Ver todos los libros")
            print("  0 - Cerrar sesion")
            opcion = pedir("Opcion")

            try:
                if   opcion == "1": self.vista_agregar()
                elif opcion == "2": self.vista_editar()
                elif opcion == "3": self.vista_borrar()
                elif opcion == "4": self.vista_buscar()
                elif opcion == "5": self.vista_listar()
                elif opcion == "0":
                    self.ctrl.cerrar_sesion()
                    print("\n  Sesion cerrada.")
                    pausa()
                    break
                else:
                    print("  Opcion no valida.")
            except PermissionError as e:
                print(f"\n  Acceso denegado: {e}")
                pausa()
                break
            except Exception as e:
                print(f"\n  Error: {e}")
                pausa()

    def menu_cliente(self):
        while True:
            print("\n  -- Menu Cliente --\n")
            print("  4 - Buscar libros")
            print("  5 - Ver catalogo completo")
            print("  0 - Volver")
            opcion = pedir("Opcion")

            try:
                if   opcion == "4": self.vista_buscar()
                elif opcion == "5": self.vista_listar()
                elif opcion == "0": break
                else: print("  Opcion no valida.")
            except Exception as e:
                print(f"\n  Error: {e}")
                pausa()

    # --- Acciones ---

    def vista_agregar(self):
        print("\n  -- Agregar libro --")
        titulo   = pedir("Titulo")
        autor    = pedir("Autor")
        genero   = pedir("Genero", obligatorio=False)
        isbn     = pedir("ISBN")
        cantidad = pedir_int("Cantidad en stock", minimo=0)
        id_nuevo = self.ctrl.agregar_libro(titulo, autor, genero, isbn, cantidad)
        if id_nuevo:
            print(f"\n  Libro agregado con ID={id_nuevo}.")
        pausa()

    def vista_editar(self):
        print("\n  -- Editar libro --")
        self.vista_listar(con_pausa=False)
        id_libro = pedir_int("ID del libro a editar", minimo=1)
        libro = self.ctrl.obtener_libro(id_libro)
        if libro is None:
            print(f"  No existe libro con ID={id_libro}.")
            pausa()
            return

        print(f"\n  Editando: [{libro.id}] {libro.titulo}")
        print("  (Deja en blanco para conservar el valor actual)\n")

        titulo   = input(f"  Titulo   [{libro.titulo}]: ").strip()   or libro.titulo
        autor    = input(f"  Autor    [{libro.autor}]: ").strip()    or libro.autor
        genero   = input(f"  Genero   [{libro.genero}]: ").strip()   or libro.genero
        isbn     = input(f"  ISBN     [{libro.isbn}]: ").strip()     or libro.isbn
        cant_str = input(f"  Cantidad [{libro.cantidad}]: ").strip()
        cantidad = int(cant_str) if cant_str else libro.cantidad

        self.ctrl.editar_libro(id_libro, titulo, autor, genero, isbn, cantidad)
        print("\n  Libro actualizado.")
        pausa()

    def vista_borrar(self):
        print("\n  -- Borrar libro --")
        self.vista_listar(con_pausa=False)
        id_libro = pedir_int("ID del libro a eliminar", minimo=1)
        conf = pedir(f"Confirmas eliminar ID={id_libro}? (s/n)")
        if conf.lower() == "s":
            self.ctrl.borrar_libro(id_libro)
            print("\n  Libro eliminado.")
        else:
            print("\n  Operacion cancelada.")
        pausa()

    def vista_buscar(self):
        print("\n  -- Buscar libros --")
        print("  Criterios disponibles: titulo, autor, genero, isbn\n")
        criterio   = pedir("Criterio de busqueda")
        valor      = pedir("Valor a buscar")
        resultados = self.ctrl.buscar_libros(criterio, valor)
        print(f"\n  Se encontraron {len(resultados)} resultado(s):")
        mostrar_libros(resultados)
        pausa()

    def vista_listar(self, con_pausa=True):
        print("\n  -- Catalogo completo --")
        libros = self.ctrl.listar_libros()
        print(f"  Total: {len(libros)} libro(s)")
        mostrar_libros(libros)
        if con_pausa:
            pausa()