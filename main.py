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

def movimiento_inventario():
    print("\n--- MOVIMIENTO MANUAL DE INVENTARIO ---")
    codigo = input("Codigo del producto: ").strip().upper()
    p = producto_por_codigo(codigo)
    if not p:
        print("Producto no encontrado.")
        return

    lotes_prod = [l for l in lotes if l["codigo_producto"] == codigo and l["estado"] == "activo" and l["cantidad_actual"] > 0]
    if not lotes_prod:
        print("No hay lotes activos para este producto.")
        return

    for l in lotes_prod:
        print(f"ID #{l['id']} - Ubicacion: {l['ubicacion']} - Stock: {l['cantidad_actual']}")

    id_l = leer_entero("ID del lote a afectar: ", minimo=1)
    lote_sel = next((l for l in lotes_prod if l["id"] == id_l), None)
    if not lote_sel:
        print("Lote invalido.")
        return

    print("1. ENTRADA  2. SALIDA")
    t_op = input("Seleccione: ").strip()
    if t_op not in ["1", "2"]:
        print("Opcion invalida.")
        return

    tipo = "ENTRADA" if t_op == "1" else "SALIDA"
    cant = leer_entero("Cantidad: ", minimo=1)
    motivo = input("Motivo: ").strip()

    if tipo == "SALIDA":
        if cant > lote_sel["cantidad_actual"]:
            print("Cantidad supera el stock del lote.")
            return
        lote_sel["cantidad_actual"] -= cant
        if lote_sel["cantidad_actual"] == 0:
            lote_sel["estado"] = "agotado"
    else:
        lote_sel["cantidad_actual"] += cant

    movimientos.append({
        "id": siguiente_id(movimientos),
        "fecha": fecha_actual(),
        "codigo_producto": codigo,
        "id_lote": lote_sel["id"],
        "tipo": tipo,
        "cantidad": cant,
        "motivo": motivo if motivo else "Ajuste manual"
    })

    guardar_todo()
    print("Movimiento registrado exitosamente.")

def listar_movimientos():
    print("\n--- HISTORIAL DE MOVIMIENTOS ---")
    if not movimientos:
        print("No hay movimientos registrados.")
        return

    print(f"\n{'ID':<5} {'FECHA':<20} {'PRODUCTO':<10} {'LOTE':<6} {'TIPO':<8} {'CANT':<6} {'MOTIVO':<30}")
    print("-" * 90)
    for m in movimientos:
        print(f"{m['id']:<5} {m['fecha']:<20} {m['codigo_producto']:<10} {m['id_lote']:<6} {m['tipo']:<8} {m['cantidad']:<6} {m['motivo']:<30}")

def gestionar_inventario():
    while True:
        print("\n=== GESTION DE INVENTARIO ===")
        print("1. Consultar existencias generales")
        print("2. Registrar ajuste manual / merma")
        print("3. Ver historial de movimientos")
        print("4. Volver al menu principal")
        opc = input("Seleccione una opcion: ").strip()

        if opc == "1": listar_productos()
        elif opc == "2": movimiento_inventario()
        elif opc == "3": listar_movimientos()
        elif opc == "4": break
        else: print("Opcion invalida.")

def registrar_venta():
    print("\n--- REGISTRAR VENTA ---")
    if not productos:
        print("No hay productos registrados.")
        return

    cliente = input("Nombre del cliente: ").strip()
    if not cliente:
        cliente = "Cliente General"

    carrito = []
    total_venta = 0.0

    while True:
        mostrar_tabla_productos([p for p in productos if p.get("activo", True)])
        codigo = input("\nCodigo de producto (o 'FIN' para terminar): ").strip().upper()
        if codigo == "FIN":
            break

        p = producto_por_codigo(codigo)
        if not p or not p.get("activo", True):
            print("Producto invalido o inactivo.")
            continue

        st_disponible = stock_producto(codigo)
        if st_disponible <= 0:
            print("Sin stock disponible.")
            continue

        cant_pedida = leer_entero("Cantidad a vender: ", minimo=1)
        if cant_pedida > st_disponible:
            print("Stock insuficiente.")
            continue

        lotes_prod = [l for l in lotes if l["codigo_producto"] == codigo and l["estado"] == "activo" and l["cantidad_actual"] > 0]
        lotes_prod.sort(key=lambda x: x["fecha_ingreso"])

        pendiente = cant_pedida
        detalles_lotes = []

        for l in lotes_prod:
            if pendiente == 0:
                break
            a_tomar = min(l["cantidad_actual"], pendiente)
            l["cantidad_actual"] -= a_tomar
            if l["cantidad_actual"] == 0:
                l["estado"] = "agotado"
            pendiente -= a_tomar

            detalles_lotes.append({
                "id_lote": l["id"],
                "cantidad": a_tomar,
                "costo_unitario": l["costo_unitario"]
            })

            movimientos.append({
                "id": siguiente_id(movimientos),
                "fecha": fecha_actual(),
                "codigo_producto": codigo,
                "id_lote": l["id"],
                "tipo": "SALIDA",
                "cantidad": a_tomar,
                "motivo": "Venta realizada"
            })

        subtotal = cant_pedida * p["precio"]
        total_venta += subtotal

        carrito.append({
            "codigo_producto": codigo,
            "nombre": p["nombre"],
            "cantidad": cant_pedida,
            "precio_unitario": p["precio"],
            "subtotal": subtotal,
            "desglose_lotes": detalles_lotes
        })

        otra = input("¿Agregar otro producto? (s/n): ").strip().lower()
        if otra != "s":
            break

    if not carrito:
        print("Venta cancelada.")
        return

    id_v = siguiente_id(ventas)
    nueva_venta = {
        "id": id_v,
        "fecha": fecha_actual(),
        "cliente": cliente,
        "items": carrito,
        "total": total_venta,
        "estado": "completada"
    }
    ventas.append(nueva_venta)
    guardar_todo()

    print("\n" + "="*45)
    print(f"      COMPROBANTE DE VENTA #{id_v}")
    print("="*45)
    print(f"Cliente: {cliente}")
    for item in carrito:
        print(f"{item['nombre']} x {item['cantidad']} = {dinero(item['subtotal'])}")
    print(f"TOTAL: {dinero(total_venta)}")
    print("="*45 + "\n")

def consultar_ventas():
    print("\n--- HISTORIAL DE VENTAS ---")
    if not ventas:
        print("No hay ventas registradas.")
        return

    print(f"\n{'ID':<5} {'FECHA':<20} {'CLIENTE':<20} {'TOTAL':<12} {'ESTADO':<10}")
    print("-" * 70)
    for v in ventas:
        print(f"{v['id']:<5} {v['fecha']:<20} {v['cliente']:<20} {dinero(v['total']):<12} {v['estado']:<10}")


def ranking_productos():
    print("\n--- RANKING DE PRODUCTOS ---")
    acumulado = {}

    for v in ventas:
        if v.get("estado") == "completada":
            for it in v["items"]:
                cod = it["codigo_producto"]
                if cod not in acumulado:
                    acumulado[cod] = {"nombre": it["nombre"], "unidades": 0, "ingresos": 0.0}
                acumulado[cod]["unidades"] += it["cantidad"]
                acumulado[cod]["ingresos"] += it["subtotal"]

    if not acumulado:
        print("No hay datos de ventas.")
        return

    lista_ranked = sorted(acumulado.values(), key=lambda x: x["unidades"], reverse=True)
    for idx, item in enumerate(lista_ranked, 1):
        print(f"{idx}. {item['nombre']} - Unidades: {item['unidades']} - Total: {dinero(item['ingresos'])}")

def reporte_rotacion():
    print("\n--- ROTACION POR CATEGORIA ---")
    categorias = {}

    for p in productos:
        cat = p["categoria"]
        if cat not in categorias:
            categorias[cat] = {"stock": 0, "vendidas": 0}
        categorias[cat]["stock"] += stock_producto(p["codigo"])

    for v in ventas:
        if v.get("estado") == "completada":
            for it in v["items"]:
                p = producto_por_codigo(it["codigo_producto"])
                cat = p["categoria"] if p else "Sin categoria"
                if cat not in categorias:
                    categorias[cat] = {"stock": 0, "vendidas": 0}
                categorias[cat]["vendidas"] += it["cantidad"]

    for cat, datos in categorias.items():
        print(f"Categoria: {cat} | Stock: {datos['stock']} | Vendidas: {datos['vendidas']}")

def ventas_rango_fechas():
    print("\n--- VENTAS POR RANGO DE FECHAS ---")
    f_inicio = input("Fecha inicio (YYYY-MM-DD): ").strip()
    f_fin = input("Fecha fin (YYYY-MM-DD): ").strip()

    filtradas = [v for v in ventas if v.get("estado") == "completada" and f_inicio <= v["fecha"].split()[0] <= f_fin]
    if not filtradas:
        print("No hay ventas en ese rango.")
        return

    total = sum(v["total"] for v in filtradas)
    print(f"Total ventas en rango: {dinero(total)}")

def leer_costo_guardado(item):
    costo_total_item = 0.0
    if "desglose_lotes" in item:
        for dl in item["desglose_lotes"]:
            costo_total_item += dl["cantidad"] * dl["costo_unitario"]
    else:
        lotes_p = [l for l in lotes if l["codigo_producto"] == item["codigo_producto"]]
        costo_u = lotes_p[0]["costo_unitario"] if lotes_p else 0
        costo_total_item = item["cantidad"] * costo_u
    return costo_total_item

def reporte_utilidad():
    print("\n--- REPORTE DE UTILIDAD ---")
    ventas_validas = [v for v in ventas if v.get("estado") == "completada"]
    if not ventas_validas:
        print("No hay ventas registradas.")
        return

    ingreso_total = sum(v["total"] for v in ventas_validas)
    costo_total = sum(sum(leer_costo_guardado(it) for it in v["items"]) for v in ventas_validas)
    utilidad = ingreso_total - costo_total

    print(f"Ingresos: {dinero(ingreso_total)}")
    print(f"Costos:   {dinero(costo_total)}")
    print(f"Utilidad: {dinero(utilidad)}")