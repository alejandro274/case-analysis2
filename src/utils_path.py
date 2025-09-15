import sys
import os

def add_project_root_to_path():
    """
    Añade el directorio raíz del proyecto al sys.path si no está presente.
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if root not in sys.path:
        sys.path.insert(0, root)
