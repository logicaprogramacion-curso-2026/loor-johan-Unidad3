"""
MiniTienda - Registro y análisis de ventas
============================================
Programa de consola que gestiona un catálogo de productos, registra ventas,
persiste datos en CSV, calcula métricas con NumPy, agrupa con Pandas y
grafica ingresos por producto con Matplotlib.

Estructuras de datos utilizadas:
- Tuplas       -> catálogo de productos (id, nombre, categoría)
- Diccionarios -> precios (id -> precio) y stock (id -> cantidad)
- Listas       -> buffer de ventas (lista de diccionarios) e IDs de venta
- Pandas       -> DataFrame de ventas, groupby por producto, lectura/escritura CSV
- NumPy        -> mean, std, sum sobre arreglos de montos
- Matplotlib   -> gráfico de barras de ingresos por producto
"""

import os
import csv
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sin ventana, apto para consola/servidor
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# 1. CATÁLOGO (TUPLAS) + PRECIOS / STOCK (DICCIONARIOS)
# ----------------------------------------------------------------------

# Catálogo: tupla de tuplas inmutables (producto_id, nombre, categoria)
CATALOGO = (
    (1, "Arroz 1kg", "Abarrotes"),
    (2, "Aceite 1L", "Abarrotes"),
    (3, "Leche 1L", "Lacteos"),
    (4, "Pan Molde", "Panaderia"),
    (5, "Detergente 1kg", "Limpieza"),
)

# Diccionarios: precio y stock inicial por producto_id
PRECIOS = {1: 1.25, 2: 3.10, 3: 0.95, 4: 2.20, 5: 4.50}
STOCK = {1: 50, 2: 40, 3: 60, 4: 35, 5: 25}

VENTAS_CSV = "ventas.csv"
LOG_TXT = "log.txt"


# ----------------------------------------------------------------------
# FUNCIONES DE APOYO / LOG
# ----------------------------------------------------------------------

def escribir_log(mensaje, log_path=LOG_TXT):
    """Escribe una línea con timestamp en el archivo de log (archivos)."""
    marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{marca}] {mensaje}\n")


def buscar_producto(producto_id, catalogo=CATALOGO):
    """Recorre el catálogo (tupla) con un for y devuelve la tupla del
    producto o None si no existe. Usa continue/break como control de flujo."""
    for item in catalogo:
        if item[0] != producto_id:
            continue          # control de flujo: continue
        return item
        break                  # (inalcanzable, ilustrativo de break)
    return None


def validar_producto(producto_id, catalogo=CATALOGO):
    """True/False según exista el producto en el catálogo."""
    return buscar_producto(producto_id, catalogo) is not None


# ----------------------------------------------------------------------
# 2. CATÁLOGO / MOSTRAR
# ----------------------------------------------------------------------

def mostrar_catalogo(catalogo=CATALOGO, precios=PRECIOS, stock=STOCK):
    print("\n" + "=" * 60)
    print(f"{'ID':<4}{'PRODUCTO':<18}{'CATEGORIA':<14}{'PRECIO':<10}{'STOCK':<6}")
    print("=" * 60)
    for producto_id, nombre, categoria in catalogo:      # desempaquetado de tupla
        precio = precios.get(producto_id, 0.0)
        cant = stock.get(producto_id, 0)
        print(f"{producto_id:<4}{nombre:<18}{categoria:<14}${precio:<9.2f}{cant:<6}")
    print("=" * 60)


# ----------------------------------------------------------------------
# RETO C: DESCUENTO POR VOLUMEN
# ----------------------------------------------------------------------

def calcular_descuento(cantidad, subtotal):
    """Reto C: si las unidades vendidas son >= 10, aplica 5% de descuento."""
    if cantidad >= 10:
        descuento = round(subtotal * 0.05, 2)
    else:
        descuento = 0.0
    return descuento


# ----------------------------------------------------------------------
# 3. REGISTRO DE VENTAS (LISTAS + DATAFRAME) / RETO D (log de fallidos)
# ----------------------------------------------------------------------

def registrar_venta(producto_id, cantidad, ventas, ids_venta,
                     catalogo=CATALOGO, precios=PRECIOS, stock=STOCK,
                     log_path=LOG_TXT):
    """
    Registra una venta si el producto existe y hay stock suficiente.
    - ventas: lista (buffer) de diccionarios que luego se vuelca a un DataFrame.
    - ids_venta: lista de IDs de venta (arreglo de identificadores).
    Devuelve el diccionario de la venta si tuvo éxito, o None si falló.
    Los intentos fallidos (producto inexistente) se registran en log.txt (Reto D).
    """
    # --- Validaciones con control de flujo if/elif/else ---
    if not validar_producto(producto_id, catalogo):
        mensaje = f"INTENTO FALLIDO: producto_id={producto_id} no existe en el catalogo."
        print(f"Error: {mensaje}")
        escribir_log(mensaje, log_path)          # Reto D
        return None
    elif cantidad <= 0:
        mensaje = f"INTENTO FALLIDO: cantidad invalida ({cantidad}) para producto_id={producto_id}."
        print(f"Error: {mensaje}")
        escribir_log(mensaje, log_path)
        return None
    elif stock.get(producto_id, 0) < cantidad:
        mensaje = (f"INTENTO FALLIDO: stock insuficiente para producto_id={producto_id} "
                   f"(solicitado={cantidad}, disponible={stock.get(producto_id, 0)}).")
        print(f"Error: {mensaje}")
        escribir_log(mensaje, log_path)
        return None
    else:
        producto = buscar_producto(producto_id, catalogo)
        nombre = producto[1]
        precio_unitario = precios[producto_id]
        subtotal_bruto = round(precio_unitario * cantidad, 2)
        descuento = calcular_descuento(cantidad, subtotal_bruto)     # Reto C
        subtotal_neto = round(subtotal_bruto - descuento, 2)

        stock[producto_id] -= cantidad   # actualizar stock (diccionario)

        nueva_id = (max(ids_venta) + 1) if ids_venta else 1
        ids_venta.append(nueva_id)       # lista de IDs

        venta = {
            "id_venta": nueva_id,
            "producto_id": producto_id,
            "producto_nombre": nombre,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "descuento": descuento,
            "subtotal": subtotal_neto,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        ventas.append(venta)             # buffer de ventas (lista de dicts)
        print(f"Venta registrada -> ID {nueva_id}: {cantidad} x {nombre} "
              f"= ${subtotal_neto:.2f} (descuento ${descuento:.2f})")
        return venta


# ----------------------------------------------------------------------
# RETO A: AGREGAR PRODUCTO NUEVO AL CATALOGO
# ----------------------------------------------------------------------

def agregar_producto(catalogo, precios, stock, producto_id, nombre,
                      categoria, precio, stock_inicial):
    """
    Reto A: agrega un producto nuevo. Como el catálogo es una TUPLA
    (inmutable), se reconstruye una tupla nueva a partir de la anterior.
    precios y stock, al ser diccionarios, se actualizan in-place.
    Devuelve el nuevo catálogo (tupla).
    """
    if validar_producto(producto_id, catalogo):
        print(f"Error: el producto_id {producto_id} ya existe en el catalogo.")
        return catalogo

    nuevo_item = (producto_id, nombre, categoria)
    nuevo_catalogo = catalogo + (nuevo_item,)   # concatenación de tuplas
    precios[producto_id] = precio
    stock[producto_id] = stock_inicial
    print(f"Producto agregado: {nuevo_item} | precio=${precio:.2f} stock={stock_inicial}")
    return nuevo_catalogo


def actualizar_precio_stock(precios, stock, producto_id, nuevo_precio=None, nuevo_stock=None):
    """Actualiza precio y/o stock de un producto existente (diccionarios)."""
    if producto_id not in precios:
        print(f"Error: producto_id {producto_id} no existe.")
        return False
    if nuevo_precio is not None:
        precios[producto_id] = nuevo_precio
    if nuevo_stock is not None:
        stock[producto_id] = nuevo_stock
    print(f"Producto {producto_id} actualizado -> precio={precios[producto_id]}, stock={stock[producto_id]}")
    return True


# ----------------------------------------------------------------------
# 4. GUARDAR / LEER DATOS DESDE CSV (ARCHIVOS)
# ----------------------------------------------------------------------

def guardar_ventas_csv(ventas, path=VENTAS_CSV):
    """Convierte el buffer de ventas (lista de dicts) a DataFrame y lo
    guarda en CSV con pandas."""
    if not ventas:
        print("No hay ventas para guardar.")
        return None
    df = pd.DataFrame(ventas)
    df.to_csv(path, index=False)
    print(f"{len(df)} ventas guardadas en '{path}'.")
    return df


def leer_ventas_csv(path=VENTAS_CSV):
    """Lee el CSV de ventas con pandas. Maneja el error de archivo
    inexistente con try/except/else/finally."""
    df = None
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        mensaje = f"No se encontro el archivo '{path}'."
        print(f"Error: {mensaje}")
        escribir_log(mensaje)
    except pd.errors.EmptyDataError:
        mensaje = f"El archivo '{path}' esta vacio."
        print(f"Error: {mensaje}")
        escribir_log(mensaje)
    else:
        print(f"Archivo '{path}' leido correctamente ({len(df)} filas).")
    finally:
        print("Fin del intento de lectura de ventas.csv.")
    return df


# ----------------------------------------------------------------------
# 5. METRICAS CON NUMPY + AGRUPACION CON PANDAS
# ----------------------------------------------------------------------

def calcular_metricas(df):
    """
    Calcula métricas con NumPy (mean, std, sum) sobre el arreglo de
    subtotales, y agrupa ingresos por producto con pandas groupby.
    Maneja división por cero de forma controlada (try/except).
    """
    if df is None or df.empty:
        print("No hay datos para calcular metricas.")
        return None, None

    montos = np.array(df["subtotal"], dtype=float)   # arreglo NumPy

    try:
        promedio = np.mean(montos)
        desviacion = np.std(montos)
        total = np.sum(montos)
        unidades_totales = np.sum(df["cantidad"].to_numpy())
        if unidades_totales == 0:
            raise ZeroDivisionError("no hay unidades vendidas (unidades_totales == 0)")
        ticket_promedio_por_unidad = total / unidades_totales
    except ZeroDivisionError:
        mensaje = "Division por cero al calcular ticket promedio por unidad."
        print(f"Error controlado: {mensaje}")
        escribir_log(mensaje)
        ticket_promedio_por_unidad = 0.0

    print("\n--- Metricas generales (NumPy) ---")
    print(f"Ingreso total:        ${total:.2f}")
    print(f"Promedio por venta:   ${promedio:.2f}")
    print(f"Desviacion estandar:  ${desviacion:.2f}")
    print(f"Ingreso por unidad:   ${ticket_promedio_por_unidad:.2f}")

    # Pandas: agrupación de ingresos por producto
    ingresos_por_producto = df.groupby("producto_nombre")["subtotal"].sum().sort_values(ascending=False)
    unidades_por_producto = df.groupby("producto_nombre")["cantidad"].sum()

    print("\n--- Ingresos por producto (Pandas groupby) ---")
    for nombre, ingreso in ingresos_por_producto.items():
        print(f"  {nombre:<18} ${ingreso:.2f}   ({unidades_por_producto[nombre]} unidades)")

    resumen = {
        "total": total,
        "promedio": promedio,
        "desviacion": desviacion,
        "ingreso_por_unidad": ticket_promedio_por_unidad,
    }
    return resumen, ingresos_por_producto


# ----------------------------------------------------------------------
# 6. GRAFICO DE INGRESOS POR PRODUCTO (MATPLOTLIB) + RETO B (exportar PNG)
# ----------------------------------------------------------------------

def graficar_ingresos(ingresos_por_producto, exportar=False, filename="ingresos.png"):
    """Grafica un bar chart de ingresos por producto. Si exportar=True
    (Reto B), guarda la figura con plt.savefig(filename)."""
    if ingresos_por_producto is None or ingresos_por_producto.empty:
        print("No hay datos para graficar.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ingresos_por_producto.sort_values(ascending=True).plot(kind="barh", ax=ax, color="#4C72B0")
    ax.set_xlabel("Ingresos ($)")
    ax.set_ylabel("Producto")
    ax.set_title("Ingresos por producto - MiniTienda")
    fig.tight_layout()

    if exportar:
        fig.savefig(filename, dpi=150)
        print(f"Grafico exportado como '{filename}'.")

    return fig


# ----------------------------------------------------------------------
# MENU PRINCIPAL (BUCLE WHILE + CONTROL DE FLUJO COMPLETO)
# ----------------------------------------------------------------------

def menu():
    catalogo = CATALOGO
    precios = dict(PRECIOS)
    stock = dict(STOCK)
    ventas = []          # buffer de ventas (lista)
    ids_venta = []        # lista de IDs

    opciones_validas = {"1", "2", "3", "4", "5", "6", "7", "0"}

    while True:
        print("\n===== MENU MINITIENDA =====")
        print("1) Ver catalogo")
        print("2) Registrar venta")
        print("3) Guardar ventas en CSV")
        print("4) Leer ventas desde CSV y ver metricas")
        print("5) Graficar ingresos por producto")
        print("6) Exportar grafico a PNG")        # Reto B
        print("7) Agregar producto al catalogo")   # Reto A
        print("0) Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion not in opciones_validas:
            print("Opcion invalida, intente de nuevo.")
            continue

        try:
            if opcion == "1":
                mostrar_catalogo(catalogo, precios, stock)

            elif opcion == "2":
                try:
                    pid = int(input("ID de producto: "))
                    cant = int(input("Cantidad: "))
                except ValueError:
                    print("Error: debe ingresar numeros enteros.")
                    continue
                registrar_venta(pid, cant, ventas, ids_venta, catalogo, precios, stock)

            elif opcion == "3":
                guardar_ventas_csv(ventas, VENTAS_CSV)

            elif opcion == "4":
                df = leer_ventas_csv(VENTAS_CSV)
                calcular_metricas(df)

            elif opcion == "5":
                df = leer_ventas_csv(VENTAS_CSV)
                if df is not None:
                    _, ingresos = calcular_metricas(df)
                    graficar_ingresos(ingresos)

            elif opcion == "6":
                df = leer_ventas_csv(VENTAS_CSV)
                if df is not None:
                    _, ingresos = calcular_metricas(df)
                    graficar_ingresos(ingresos, exportar=True, filename="ingresos.png")

            elif opcion == "7":
                try:
                    pid = int(input("Nuevo ID: "))
                    nombre = input("Nombre: ")
                    categoria = input("Categoria: ")
                    precio = float(input("Precio: "))
                    stock_ini = int(input("Stock inicial: "))
                except ValueError:
                    print("Error: datos numericos invalidos.")
                    continue
                catalogo = agregar_producto(catalogo, precios, stock, pid, nombre, categoria, precio, stock_ini)

            elif opcion == "0":
                print("Guardando ventas antes de salir...")
                if ventas:
                    guardar_ventas_csv(ventas, VENTAS_CSV)
                print("Hasta luego.")
                break

        except Exception as e:
            escribir_log(f"Error inesperado: {e}")
            print(f"Ocurrio un error inesperado: {e}")


if __name__ == "__main__":
    menu()
