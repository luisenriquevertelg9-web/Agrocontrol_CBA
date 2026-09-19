import os
import json
from datetime import datetime

DATA = "data"
RUTA_PRODUCTOS = os.path.join(DATA, "productos.json")
RUTA_LOTES = os.path.join(DATA, "lotes.json")
RUTA_MOVIMIENTOS = os.path.join(DATA, "movimientos.json")
RUTA_VENTAS = os.path.join(DATA, "ventas.json")

productos = []
lotes = []
movimientos = []
ventas = []

def cargar_archivo(ruta):
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def guardar_archivo(ruta, datos):
    os.makedirs(DATA, exist_ok=True)
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Error al guardar {ruta}: {e}")

def cargar_todo():
    global productos, lotes, movimientos, ventas
    productos = cargar_archivo(RUTA_PRODUCTOS)
    lotes = cargar_archivo(RUTA_LOTES)
    movimientos = cargar_archivo(RUTA_MOVIMIENTOS)
    ventas = cargar_archivo(RUTA_VENTAS)

def guardar_todo():
    guardar_archivo(RUTA_PRODUCTOS, productos)
    guardar_archivo(RUTA_LOTES, lotes)
    guardar_archivo(RUTA_MOVIMIENTOS, movimientos)
    guardar_archivo(RUTA_VENTAS, ventas)

def dinero(valor):
    return f"${float(valor):,.2f}"

def fecha_actual():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def leer_entero(mensaje, minimo=None):
    while True:
        try:
            val = int(input(mensaje).strip())
            if minimo is not None and val < minimo:
                print(f"Debe ser un numero entero mayor o igual a {minimo}.")
                continue
            return val
        except ValueError:
            print("Entrada invalida. Ingrese un numero entero.")

def leer_float(mensaje, minimo=None):
    while True:
        try:
            val = float(input(mensaje).strip())
            if minimo is not None and val < minimo:
                print(f"Debe ser un numero mayor o igual a {minimo}.")
                continue
            return val
        except ValueError:
            print("Entrada invalida. Ingrese un numero decimal.")

def producto_por_codigo(codigo):
    for p in productos:
        if p["codigo"] == codigo:
            return p
    return None

def lote_por_id(id_lote):
    for l in lotes:
        if l["id"] == id_lote:
            return l
    return None

def stock_producto(codigo):
    return sum(l["cantidad_actual"] for l in lotes if l["codigo_producto"] == codigo and l["estado"] == "activo")

def siguiente_id(lista):
    if not lista:
        return 1
    return max(x["id"] for x in lista) + 1
