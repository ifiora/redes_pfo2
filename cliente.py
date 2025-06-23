import requests
from getpass import getpass

API_URL = "http://localhost:5000"

# Función para registrar usuarios
def registrar_usuario():
    print("\n--- Registro ---")
    # Pedimos que ingrese el usuario
    usuario = input("Usuario: ")
    # Pedimos que ingrese la contraseña
    contrasena = getpass("Contraseña: ")
    # Creamos el objeto que vamos a enviar al servidor
    data = {"usuario": usuario, "contraseña": contrasena}
    # Hacemos una consulta POST al endpoint de registro enviando la data cargada
    r = requests.post(f"{API_URL}/registro", json=data)
    # Imprimimos en pantalla el mensaje recibido
    print(f"{r.status_code}: {r.json().get('mensaje')}")

# Función para hacer login y ver las tareas
def login_y_ver_tareas():
    print("\n--- Login y acceso a tareas ---")
    # Pedimos usuario y contraseña
    usuario = input("Usuario: ")
    contrasena = getpass("Contraseña: ")
    
    # Hacemos una llamada al endpoint de tareas agregando el campo de autenticacion con el usuario y contraseña ingresados
    r = requests.get(f"{API_URL}/tareas", auth=(usuario, contrasena))
    
    # Imprimimos el resultado obtenido por pantalla
    if r.status_code == 200:
        print("Acceso concedido:")
        print(r.text)
    else:
        print(f"Acceso denegado ({r.status_code})")

def menu():
    while True:
        print("\n=== MENÚ ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesión y ver tareas")
        print("3. Salir")
        opcion = input("Elegí una opción: ")
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            login_y_ver_tareas()
        elif opcion == "3":
            print("Chau!")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()
