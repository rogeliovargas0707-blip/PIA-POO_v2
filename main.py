"""
main.py
=======
Punto de entrada del programa.
"""
# Para cambiar a tkinter:
#   1. Crea gui_tkinter.py con la clase GUITkinter y el metodo iniciar()
#   2. Cambia las dos lineas marcadas con (CAMBIAR AQUI)

from conexion    import ConexionDB, db_path
from controlador import Controlador
from gui         import GUITerminal  


def main():
    db = ConexionDB(db_path)

    try:
        db.conectar()

        ctrl  = Controlador(db)
        vista = GUITerminal(ctrl)     # (CAMBIAR AQUI) -> GUITkinter(ctrl)
        vista.iniciar()

    except KeyboardInterrupt:
        print("\n  Programa interrumpido por el usuario.")

    except Exception as e:
        # Manejo de excepcion desde nivel superior (Modulo 9)
        print(f"\n  ERROR CRITICO: {e}")
        print("  El programa se cerrara.")

    finally:
        db.cerrar()
        print("  BD cerrada. Hasta luego.")


main()