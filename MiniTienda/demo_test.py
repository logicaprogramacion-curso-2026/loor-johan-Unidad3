"""
Script de demostración: simula la interacción del usuario con el programa
(equivalente a las celdas de prueba del notebook), generando >= 10 ventas,
probando errores controlados, los retos A-D y las salidas requeridas.
"""
import mini_tienda as mt

print("#" * 70)
print("# 1) CATALOGO INICIAL")
print("#" * 70)
catalogo = mt.CATALOGO
precios = dict(mt.PRECIOS)
stock = dict(mt.STOCK)
ventas = []
ids_venta = []
mt.mostrar_catalogo(catalogo, precios, stock)

print("\n" + "#" * 70)
print("# 2) REGISTRO DE VENTAS (>= 10 ventas, incluye casos validos e invalidos)")
print("#" * 70)

# Lista de intentos de venta: (producto_id, cantidad)
intentos_venta = [
    (1, 5),    # ok
    (2, 3),    # ok
    (3, 12),   # ok, dispara descuento (Reto C)
    (4, 2),    # ok
    (5, 1),    # ok
    (1, 10),   # ok, dispara descuento (Reto C)
    (2, 4),    # ok
    (99, 2),   # FALLA: producto no existe -> Reto D (log.txt)
    (3, 6),    # ok
    (4, 15),   # ok, dispara descuento (Reto C)
    (5, 2),    # ok
    (2, -3),   # FALLA: cantidad invalida
    (1, 3),    # ok
    (3, 4),    # ok
]

for pid, cant in intentos_venta:
    mt.registrar_venta(pid, cant, ventas, ids_venta, catalogo, precios, stock)

print(f"\nTotal de ventas exitosas registradas: {len(ventas)}")
print(f"IDs de venta (lista): {ids_venta}")

print("\n" + "#" * 70)
print("# RETO A: agregar producto nuevo y actualizar precio/stock")
print("#" * 70)
catalogo = mt.agregar_producto(catalogo, precios, stock,
                                producto_id=6, nombre="Yogurt 1L",
                                categoria="Lacteos", precio=2.75, stock_inicial=30)
mt.actualizar_precio_stock(precios, stock, producto_id=6, nuevo_precio=2.90, nuevo_stock=28)

# Vendemos algunas unidades del producto nuevo
mt.registrar_venta(6, 11, ventas, ids_venta, catalogo, precios, stock)  # con descuento
mt.registrar_venta(6, 2, ventas, ids_venta, catalogo, precios, stock)

mt.mostrar_catalogo(catalogo, precios, stock)

print("\n" + "#" * 70)
print("# 3) GUARDAR VENTAS EN CSV (Pandas)")
print("#" * 70)
df_guardado = mt.guardar_ventas_csv(ventas, mt.VENTAS_CSV)
print(df_guardado.to_string(index=False))

print("\n" + "#" * 70)
print("# 4) LEER VENTAS DESDE CSV (manejo de archivo inexistente)")
print("#" * 70)
# Caso de error controlado: archivo que no existe
df_error = mt.leer_ventas_csv("archivo_que_no_existe.csv")

# Caso correcto
df = mt.leer_ventas_csv(mt.VENTAS_CSV)

print("\n" + "#" * 70)
print("# 5) METRICAS CON NUMPY + GROUPBY CON PANDAS")
print("#" * 70)
resumen, ingresos_por_producto = mt.calcular_metricas(df)

print("\n" + "#" * 70)
print("# 6) GRAFICAR INGRESOS POR PRODUCTO (Matplotlib)")
print("#" * 70)
fig = mt.graficar_ingresos(ingresos_por_producto)
fig.savefig("ingresos_preview.png", dpi=150)
print("Vista previa del grafico guardada en 'ingresos_preview.png'.")

print("\n" + "#" * 70)
print("# RETO B: Exportar grafico a PNG (opcion 6 del menu)")
print("#" * 70)
fig2 = mt.graficar_ingresos(ingresos_por_producto, exportar=True, filename="ingresos.png")

print("\n" + "#" * 70)
print("# RETO D: verificar que el intento fallido quedo en log.txt")
print("#" * 70)
with open(mt.LOG_TXT, "r", encoding="utf-8") as f:
    print(f.read())

print("\nDEMO COMPLETADA CORRECTAMENTE.")
