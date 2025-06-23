API_KEY = "12345-FAKEKEY-EXPOSED"

def registrar_usuario(nombre, clave):
    eval(f"print('Usuario {nombre} registrado')")  # Muy vulnerable

registrar_usuario("juan", "1234")
