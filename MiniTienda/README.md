# MiniTienda — Registro y análisis de ventas

Programa de consola en Python que administra un catálogo de productos, registra
ventas, persiste datos en CSV, calcula métricas con NumPy, agrupa y analiza con
Pandas, y grafica ingresos por producto con Matplotlib.

## Contenido del directorio

| Archivo | Descripción |
|---|---|
| `mini_tienda.py` | Módulo principal con toda la lógica modular del programa (catálogo, ventas, CSV, métricas, gráfico y menú). |
| `demo_test.py` | Script de prueba que simula el uso del programa (≥ 10 ventas, casos válidos e inválidos, Retos A–D). |
| `MiniTienda.ipynb` | Notebook (Jupyter/Colab) con el código ejecutable y celdas de prueba ya ejecutadas. |
| `evidencia_minitienda.pdf` | Evidencia del desarrollo: capturas de ejecución, explicación del algoritmo y checklist de cumplimiento. |
| `ventas.csv` | CSV generado con 14 ventas de ejemplo. |
| `log.txt` | Log de intentos de venta fallidos (Reto D) y errores controlados. |
| `ingresos.png` | Gráfico de barras de ingresos por producto, exportado con `plt.savefig` (Reto B). |

## Cómo ejecutar

```bash
pip install pandas numpy matplotlib
python mini_tienda.py
```

Esto abre el menú interactivo:

```
1) Ver catalogo
2) Registrar venta
3) Guardar ventas en CSV
4) Leer ventas desde CSV y ver metricas
5) Graficar ingresos por producto
6) Exportar grafico a PNG
7) Agregar producto al catalogo
0) Salir
```

Para ver la demostración automática (sin interacción por teclado):

```bash
python demo_test.py
```

## Estructuras de datos utilizadas

- **Tuplas** → `CATALOGO`: tupla de tuplas `(producto_id, nombre, categoría)`.
- **Diccionarios** → `PRECIOS` (`id → precio`) y `STOCK` (`id → cantidad`).
- **Listas** → `ventas` (buffer de diccionarios de venta) e `ids_venta` (lista de IDs).
- **Pandas** → `DataFrame` de ventas, `groupby("producto_nombre")`, `to_csv` / `read_csv`.
- **NumPy** → `np.mean`, `np.std`, `np.sum` sobre el arreglo de subtotales.
- **Matplotlib** → gráfico de barras horizontales de ingresos por producto.

## Manejo de errores

- `try/except ValueError` al convertir la entrada de teclado a número.
- `try/except FileNotFoundError` / `pd.errors.EmptyDataError` con `else`/`finally` al leer `ventas.csv`.
- `try/except ZeroDivisionError` (controlado) al calcular el ingreso por unidad vendida si no hay unidades.
- `try/except Exception` general envolviendo cada opción del menú.
- Validación de `producto_id` inexistente y `cantidad` inválida, con registro en `log.txt`.

## Retos implementados

- **Reto A** — `agregar_producto()` agrega un producto nuevo (reconstruyendo el catálogo como tupla nueva) y `actualizar_precio_stock()` actualiza precio/stock de un producto existente.
- **Reto B** — Opción **6) Exportar grafico a PNG** del menú, que llama a `plt.savefig("ingresos.png")`.
- **Reto C** — `calcular_descuento()` aplica 5% de descuento cuando la cantidad vendida es `>= 10` unidades.
- **Reto D** — Todo intento de venta con un `producto_id` que no está en el catálogo (u otra validación fallida) se registra en `log.txt` mediante `escribir_log()`.

## Respuestas del entregable

**¿Qué parte la hizo Pandas? ¿Qué parte NumPy?**
Pandas construye el `DataFrame` de ventas, lee/escribe el CSV y agrupa ingresos y
unidades por producto con `groupby`. NumPy calcula las métricas agregadas
(`mean`, `std`, `sum`) sobre el arreglo de subtotales y protege la división para
el ingreso por unidad vendida.

**¿Dónde usaste try/except y por qué?**
En `leer_ventas_csv` (archivo inexistente o vacío), en `calcular_metricas`
(división por cero controlada), al convertir texto a número en el menú
(`ValueError`), y como red de seguridad general alrededor de cada opción del
menú (`Exception`), para evitar que el programa se detenga ante un error
inesperado.

**¿Qué estructuras son tuplas, listas y diccionarios en el código?**
Tuplas: `CATALOGO` y cada producto individual. Listas: `ventas` e `ids_venta`.
Diccionarios: `PRECIOS`, `STOCK` y cada venta individual dentro de `ventas`.

## Notas

Antes de modificar el repositorio local, sincronizar con:

```bash
git pull
```
