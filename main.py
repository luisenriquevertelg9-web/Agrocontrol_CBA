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


def mostrar_tabla_productos(lista):
    if not lista:
        print("No hay productos para mostrar.")
        return
    print(f"\n{'CODIGO':<10} {'NOMBRE':<25} {'CATEGORIA':<15} {'UNIDAD':<8} {'PRECIO':<12} {'ST.MIN':<8} {'STOCK':<8} {'ESTADO':<8}")
    print("-" * 100)
    for p in lista:
        st = stock_producto(p["codigo"])
        est = "Activo" if p.get("activo", True) else "Inactivo"
        print(f"{p['codigo']:<10} {p['nombre']:<25} {p['categoria']:<15} {p['unidad']:<8} {dinero(p['precio']):<12} {p['stock_minimo']:<8} {st:<8} {est:<8}")

def registrar_producto():
    print("\n--- REGISTRAR PRODUCTO ---")
    codigo = input("Codigo del producto: ").strip().upper()
    if not codigo:
        print("El codigo no puede estar vacio.")
        return
    if producto_por_codigo(codigo):
        print("Ya existe un producto con ese codigo.")
        return

    nombre = input("Nombre del producto: ").strip()
    categoria = input("Categoria: ").strip()
    unidad = input("Unidad de medida: ").strip()
    precio = leer_float("Precio de venta unitario: ", minimo=0)
    stock_minimo = leer_entero("Stock minimo de alerta: ", minimo=0)

    nuevo = {
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "unidad": unidad,
        "precio": precio,
        "stock_minimo": stock_minimo,
        "activo": True
    }
    productos.append(nuevo)
    guardar_todo()
    print(f"Producto '{nombre}' registrado exitosamente.")

def listar_productos():
    print("\n--- LISTADO DE PRODUCTOS ---")
    mostrar_tabla_productos(productos)

def buscar_producto():
    print("\n--- BUSCAR PRODUCTO ---")
    q = input("Ingrese texto a buscar: ").strip().lower()
    hallados = [p for p in productos if q in p["codigo"].lower() or q in p["nombre"].lower() or q in p["categoria"].lower()]
    mostrar_tabla_productos(hallados)

def actualizar_producto():
    print("\n--- ACTUALIZAR PRODUCTO ---")
    codigo = input("Ingrese el codigo del producto a modificar: ").strip().upper()
    p = producto_por_codigo(codigo)
    if not p:
        print("Producto no encontrado.")
        return

    n_nombre = input(f"Nombre [{p['nombre']}]: ").strip()
    n_cat = input(f"Categoria [{p['categoria']}]: ").strip()
    n_uni = input(f"Unidad [{p['unidad']}]: ").strip()

    str_precio = input(f"Precio [{p['precio']}]: ").strip()
    str_min = input(f"Stock minimo [{p['stock_minimo']}]: ").strip()

    if n_nombre: p["nombre"] = n_nombre
    if n_cat: p["categoria"] = n_cat
    if n_uni: p["unidad"] = n_uni
    if str_precio:
        try:
            p["precio"] = float(str_precio)
        except ValueError:
            pass
    if str_min:
        try:
            p["stock_minimo"] = int(str_min)
        except ValueError:
            pass

    guardar_todo()
    print("Producto actualizado exitosamente.")

def desactivar_producto():
    print("\n--- CAMBIAR ESTADO DE PRODUCTO ---")
    codigo = input("Codigo del producto: ").strip().upper()
    p = producto_por_codigo(codigo)
    if not p:
        print("Producto no encontrado.")
        return

    p["activo"] = not p.get("activo", True)
    guardar_todo()
    print("Estado del producto actualizado.")

def gestionar_productos():
    while True:
        print("\n=== GESTION DE PRODUCTOS ===")
        print("1. Registrar producto")
        print("2. Listar productos")
        print("3. Buscar producto")
        print("4. Actualizar producto")
        print("5. Activar/Desactivar producto")
        print("6. Volver al menu principal")
        opc = input("Seleccione una opcion: ").strip()

        if opc == "1": registrar_producto()
        elif opc == "2": listar_productos()
        elif opc == "3": buscar_producto()
        elif opc == "4": actualizar_producto()
        elif opc == "5": desactivar_producto()
        elif opc == "6": break
        else: print("Opcion invalida.")

def registrar_lote():
    print("\n--- REGISTRAR LOTE ---")
    if not productos:
        print("No hay productos registrados.")
        return

    codigo = input("Codigo del producto: ").strip().upper()
    p = producto_por_codigo(codigo)
    if not p:
        print("Producto no encontrado.")
        return

    cant = leer_entero("Cantidad ingresada: ", minimo=1)
    costo_u = leer_float("Costo unitario: ", minimo=0)
    ubicacion = input("Ubicacion: ").strip()
    fecha_venc = input("Fecha vencimiento (opcional): ").strip()

    nuevo_l = {
        "id": siguiente_id(lotes),
        "codigo_producto": codigo,
        "cantidad_inicial": cant,
        "cantidad_actual": cant,
        "costo_unitario": costo_u,
        "fecha_ingreso": fecha_actual(),
        "fecha_vencimiento": fecha_venc if fecha_venc else "N/A",
        "ubicacion": ubicacion if ubicacion else "General",
        "estado": "activo"
    }
    lotes.append(nuevo_l)

    movimientos.append({
        "id": siguiente_id(movimientos),
        "fecha": fecha_actual(),
        "codigo_producto": codigo,
        "id_lote": nuevo_l["id"],
        "tipo": "ENTRADA",
        "cantidad": cant,
        "motivo": "Registro de nuevo lote"
    })

    guardar_todo()
    print(f"Lote ID #{nuevo_l['id']} registrado correctamente.")

def listar_lotes():
    print("\n--- LISTADO DE LOTES ---")
    if not lotes:
        print("No hay lotes registrados.")
        return

    print(f"\n{'ID':<5} {'CODIGO':<10} {'PRODUCTO':<20} {'INICIAL':<8} {'ACTUAL':<8} {'COSTO U.':<12} {'UBICACION':<15} {'ESTADO':<8}")
    print("-" * 95)
    for l in lotes:
        p = producto_por_codigo(l["codigo_producto"])
        nom_p = p["nombre"] if p else "Desconocido"
        print(f"{l['id']:<5} {l['codigo_producto']:<10} {nom_p:<20} {l['cantidad_inicial']:<8} {l['cantidad_actual']:<8} {dinero(l['costo_unitario']):<12} {l['ubicacion']:<15} {l['estado']:<8}")

def cosechar_lote():
    print("\n--- ADICION A LOTE ---")
    id_l = leer_entero("ID del lote: ", minimo=1)
    l = lote_por_id(id_l)
    if not l or l["estado"] != "activo":
        print("Lote no encontrado o inactivo.")
        return

    cant = leer_entero("Cantidad adicional: ", minimo=1)
    l["cantidad_inicial"] += cant
    l["cantidad_actual"] += cant

    movimientos.append({
        "id": siguiente_id(movimientos),
        "fecha": fecha_actual(),
        "codigo_producto": l["codigo_producto"],
        "id_lote": l["id"],
        "tipo": "ENTRADA",
        "cantidad": cant,
        "motivo": "Adicion a lote"
    })

    guardar_todo()
    print(f"Se adicionaron {cant} unidades al Lote ID #{l['id']}.")

def cambiar_estado_lote():
    print("\n--- CAMBIAR ESTADO DE LOTE ---")
    id_l = leer_entero("ID del lote: ", minimo=1)
    l = lote_por_id(id_l)
    if not l:
        print("Lote no encontrado.")
        return

    print("1. activo  2. agotado  3. descartado")
    op = input("Nuevo estado: ").strip()
    mapa = {"1": "activo", "2": "agotado", "3": "descartado"}
    if op in mapa:
        l["estado"] = mapa[op]
        guardar_todo()
        print("Estado actualizado.")

def gestionar_lotes():
    while True:
        print("\n=== GESTION DE LOTES ===")
        print("1. Registrar nuevo lote")
        print("2. Listar lotes")
        print("3. Adicion a lote")
        print("4. Cambiar estado de lote")
        print("5. Volver al menu principal")
        opc = input("Seleccione una opcion: ").strip()

        if opc == "1": registrar_lote()
        elif opc == "2": listar_lotes()
        elif opc == "3": cosechar_lote()
        elif opc == "4": cambiar_estado_lote()
        elif opc == "5": break
        else: print("Opcion invalida.")

