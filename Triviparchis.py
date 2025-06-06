import random
import firebase_admin
from firebase_admin import credentials, db

# --- BASE DE DATOS Y FIREBASE ---
def iniciar_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("clave_firebase.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://parchis-de-trivia-default-rtdb.firebaseio.com/'
        })

def crear_partida(partida_id, ubicaciones_tablero):
    ref = db.reference(f'partidas/{partida_id}/ubicacionesTablero')
    ref.set(ubicaciones_tablero)

def agregar_usuario_a_partida(partida_id, usuario_id, nombre, color_ficha, posicion_inicial=0):
    ref = db.reference(f'partidas/{partida_id}/usuarios/{usuario_id}')
    ref.set({
        'nombre': nombre,
        'colorFicha': color_ficha,
        'posicionFicha': posicion_inicial
    })

def actualizar_posicion_usuario(partida_id, usuario_id, nueva_posicion):
    ref = db.reference(f'partidas/{partida_id}/usuarios/{usuario_id}/posicionFicha')
    ref.set(nueva_posicion)

def obtener_posicion_usuario(partida_id, usuario_id):
    ref = db.reference(f'partidas/{partida_id}/usuarios/{usuario_id}/posicionFicha')
    return ref.get()

def obtener_posiciones_todas_las_fichas(partida_id):
    ref = db.reference(f'partidas/{partida_id}/usuarios')
    return ref.get()

# --- TRIVIA - PREGUNTAS ---
PREGUNTAS = {
    "Matemáticas": [
        {"pregunta": "¿Cuál es el resultado de 8 × 7?", "opciones": ["A) 54", "B) 56", "C) 58", "D) 64"], "respuesta": "B"},
        {"pregunta": "¿Qué nombre recibe un polígono de ocho lados?", "opciones": ["A) Hexágono", "B) Octágono", "C) Decágono", "D) Heptágono"], "respuesta": "B"},
        {"pregunta": "¿Cuál es el valor de π (pi) aproximado?", "opciones": ["A) 2.14", "B) 3.14", "C) 3.41", "D) 4.13"], "respuesta": "B"},
        {"pregunta": "Si un triángulo tiene dos lados iguales, ¿cómo se llama?", "opciones": ["A) Equilátero", "B) Isósceles", "C) Escaleno", "D) Rectángulo"], "respuesta": "B"},
        {"pregunta": "¿Qué es el mínimo común múltiplo de 6 y 8?", "opciones": ["A) 24", "B) 12", "C) 16", "D) 48"], "respuesta": "A"}
    ],
    "Ciencias Naturales": [
        {"pregunta": "¿Cuál es el planeta más grande del sistema solar?", "opciones": ["A) Marte", "B) Saturno", "C) Júpiter", "D) Urano"], "respuesta": "C"},
        {"pregunta": "¿Qué gas es esencial para la respiración humana?", "opciones": ["A) Nitrógeno", "B) Oxígeno", "C) Hidrógeno", "D) Dióxido de carbono"], "respuesta": "B"},
        {"pregunta": "¿Qué órgano del cuerpo humano bombea la sangre?", "opciones": ["A) Pulmón", "B) Estómago", "C) Hígado", "D) Corazón"], "respuesta": "D"},
        {"pregunta": "¿Cómo se llama el cambio de estado de sólido a líquido?", "opciones": ["A) Evaporación", "B) Condensación", "C) Fusión", "D) Sublimación"], "respuesta": "C"},
        {"pregunta": "¿Cuál es la unidad principal de la célula?", "opciones": ["A) Núcleo", "B) Citoplasma", "C) Membrana", "D) Mitocondria"], "respuesta": "A"}
    ],
    "Ciencias Sociales": [
        {"pregunta": "¿Quién fue el primer presidente de Estados Unidos?", "opciones": ["A) Abraham Lincoln", "B) George Washington", "C) Thomas Jefferson", "D) John Adams"], "respuesta": "B"},
        {"pregunta": "¿Cuál es la capital de Francia?", "opciones": ["A) Roma", "B) Berlín", "C) París", "D) Madrid"], "respuesta": "C"},
        {"pregunta": "¿Qué civilización construyó las pirámides de Egipto?", "opciones": ["A) Griega", "B) Romana", "C) Egipcia", "D) Mesopotámica"], "respuesta": "C"},
        {"pregunta": "¿Qué día se celebra la independencia de México?", "opciones": ["A) 5 de mayo", "B) 16 de septiembre", "C) 20 de noviembre", "D) 1 de octubre"], "respuesta": "B"},
        {"pregunta": "¿Cómo se llama el documento que establece las leyes de un país?", "opciones": ["A) Tratado", "B) Constitución", "C) Código Penal", "D) Juramento"], "respuesta": "B"}
    ],
    "Literatura": [
        {"pregunta": "¿Quién escribió Don Quijote de la Mancha?", "opciones": ["A) Gabriel García Márquez", "B) Miguel de Cervantes", "C) Pablo Neruda", "D) Mario Vargas Llosa"], "respuesta": "B"},
        {"pregunta": "¿Qué es una fábula?", "opciones": ["A) Un poema épico", "B) Una narración de animales con moraleja", "C) Una leyenda histórica", "D) Una historia sin personajes"], "respuesta": "B"},
        {"pregunta": "¿Quién escribió Cien años de soledad?", "opciones": ["A) Gabriel García Márquez", "B) Julio Cortázar", "C) Isabel Allende", "D) Jorge Luis Borges"], "respuesta": "A"},
        {"pregunta": "¿Qué tipo de texto es una obra de teatro?", "opciones": ["A) Lírico", "B) Narrativo", "C) Dramático", "D) Científico"], "respuesta": "C"},
        {"pregunta": "¿Qué figura literaria compara dos cosas usando 'como'?", "opciones": ["A) Metáfora", "B) Hipérbole", "C) Personificación", "D) Símil"], "respuesta": "D"}
    ],
    "Deportes": [
        {"pregunta": "¿Cuántos jugadores hay en un equipo de fútbol (en cancha)?", "opciones": ["A) 9", "B) 10", "C) 11", "D) 12"], "respuesta": "C"},
        {"pregunta": "¿Qué país organiza los Juegos Olímpicos cada 4 años?", "opciones": ["A) Rusia", "B) No es un país fijo", "C) Estados Unidos", "D) China"], "respuesta": "B"},
        {"pregunta": "¿Qué deporte utiliza raquetas y una red?", "opciones": ["A) Golf", "B) Tenis", "C) Natación", "D) Rugby"], "respuesta": "B"},
        {"pregunta": "¿En qué deporte se usa una canasta?", "opciones": ["A) Béisbol", "B) Fútbol", "C) Baloncesto", "D) Hockey"], "respuesta": "C"},
        {"pregunta": "¿Qué país ha ganado más Copas del Mundo de fútbol?", "opciones": ["A) Alemania", "B) Italia", "C) Argentina", "D) Brasil"], "respuesta": "D"}
    ]
}

# --- SELECCIÓN Y PREGUNTA ---
def seleccionar_materia():
    print("📚 Materias disponibles:")
    for i, materia in enumerate(PREGUNTAS.keys(), 1):
        print(f"{i}. {materia}")
    while True:
        try:
            opcion = int(input("Selecciona una materia para esta partida: "))
            materia = list(PREGUNTAS.keys())[opcion - 1]
            print(f"✅ Se jugará con preguntas de: {materia}\n")
            return materia
        except (ValueError, IndexError):
            print("❌ Selección no válida. Intenta nuevamente.")

def hacer_pregunta(materia):
    pregunta = random.choice(PREGUNTAS[materia])
    print(f"\n❓ Pregunta de {materia}:\n{pregunta['pregunta']}")
    for opcion in pregunta['opciones']:
        print(opcion)
    respuesta_usuario = input("Tu respuesta (A, B, C o D): ").strip().upper()
    return respuesta_usuario == pregunta['respuesta']

# --- JUEGO ---
def lanzar_dado():
    return random.randint(1, 6)

def registrar_jugadores(partida_id):
    jugadores = []
    while True:
        try:
            cantidad = int(input("👥 ¿Cuántos jugadores van a participar?: "))
            if cantidad > 0:
                break
            else:
                print("⚠️ Debe haber al menos un jugador.")
        except ValueError:
            print("❌ Ingresa un número válido.")

    for i in range(1, cantidad + 1):
        print(f"\n🔸 Registro del jugador {i}:")
        nombre = input("🎮 Nombre: ").strip()
        correo = input("📧 Correo: ").strip()
        color_ficha = input("🎨 Color de ficha: ").strip().lower()
        usuario_id = nombre.replace(" ", "_").lower()

        agregar_usuario_a_partida(partida_id, usuario_id, nombre, color_ficha)
        jugadores.append(usuario_id)
        print(f"✅ Jugador '{nombre}' registrado correctamente.\n")
    return jugadores

def mostrar_posiciones(partida_id):
    datos = obtener_posiciones_todas_las_fichas(partida_id)
    print("\n📍 Posiciones actuales:")
    for uid, info in datos.items():
        print(f"🔹 {info['nombre']} ({info['colorFicha']}): Posición {info['posicionFicha']}")

def main():
    iniciar_firebase()
    partida_id = "partida_demo"

    ubicaciones_tablero = {
        'celdas': {str(i): {'x': i*10, 'y': 0} for i in range(1, 11)},
        'carcel': {'x': 0, 'y': -10},
        'salida': {'x': 0, 'y': 0}
    }
    crear_partida(partida_id, ubicaciones_tablero)

    print("🎲 BIENVENIDO AL JUEGO DE PARCHÍS - CON TRIVIA")
    materia = seleccionar_materia()
    jugadores = registrar_jugadores(partida_id)
    turno_actual = 0

    while True:
        jugador_id = jugadores[turno_actual]
        print(f"\n🔁 TURNO DE: {jugador_id.replace('_', ' ').title()}")
        print("1. Lanzar dado 🎲")
        print("2. Ver posiciones de todas las fichas 🧩")
        print("3. Salir 🚪")

        opcion = input("Elige una opción: ").strip()

        if opcion == '1':
            dado = lanzar_dado()
            print(f"🎲 Sacaste un {dado}!")

            actual = obtener_posicion_usuario(partida_id, jugador_id)
            nueva = actual + dado
            if nueva > 10:
                nueva = 10

            posiciones = obtener_posiciones_todas_las_fichas(partida_id)
            ocupante = None
            for otro_id, info in posiciones.items():
                if otro_id != jugador_id and info['posicionFicha'] == nueva:
                    ocupante = otro_id
                    break

            if ocupante:
                print(f"⚠️ La casilla {nueva} ya está ocupada por {ocupante.replace('_', ' ').title()}")
                print("Se le hará una pregunta de trivia para defender su posición.")
                if hacer_pregunta(materia):
                    print("✅ ¡Respuesta correcta! El jugador atacante será devuelto a su casilla anterior.")
                    nueva = actual
                else:
                    print("❌ Respuesta incorrecta. El jugador avanzará como estaba previsto.")

            actualizar_posicion_usuario(partida_id, jugador_id, nueva)
            print(f"➡️ Nueva posición: {nueva}")

            turno_actual = (turno_actual + 1) % len(jugadores)

        elif opcion == '2':
            mostrar_posiciones(partida_id)

        elif opcion == '3':
            print("👋 Juego finalizado. ¡Hasta la próxima!")
            break

        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    main()
