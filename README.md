# 🌾 AgroControl - Sistema de Gestión de Inventarios

Sistema en consola desarrollado en Python para la administración de productos, lotes, inventario, ventas y reportes de un negocio agrícola o de suministros.

---

## 🛠️ Tecnologías y Módulos Utilizados

El proyecto fue desarrollado completamente en **Python 3** utilizando únicamente librerías estándar nativas (no requiere instalación de paquetes externos):

* **`os`**: Para la gestión de rutas de archivos y creación automática de directorios del sistema.
* **`json`**: Para la persistencia de datos (lectura y escritura de productos, lotes, movimientos y ventas).
* **`csv`**: Para la generación y exportación del reporte de inventario a hojas de cálculo.
* **`datetime`**: Para el registro automatizado con fecha y hora de movimientos y transacciones.

---

## 🚀 Características Principales

* **Gestión de Productos:** Registro, actualización, búsqueda y cambio de estado (Activo/Inactivo).
* **Control de Lotes:** Registro de lotes con fechas de vencimiento, ubicaciones y adición de stock.
* **Movimientos de Inventario:** Historial de entradas/salidas y ajustes manuales por merma.
* **Punto de Venta:** Registro de ventas con salida de inventario automatizada (metodología FIFO por lotes) y comprobante.
* **Módulo de Anulación:** Reingreso automático de stock al anular una venta.

* **Reportes e Indicadores:**
  * Alertas de stock mínimo.
  * Valoración total del inventario.
  * Reporte de utilidad e ingresos.
  * Ranking de productos más vendidos y rotación por categoría.
  * Exportación de productos a formato `.csv`.


---

## 📂 Estructura del Proyecto

AgroControl/
├── data/                  # Archivos de base de datos JSON
│   ├── productos.json
│   ├── lotes.json
│   ├── movimientos.json
│   └── ventas.json
├── main.py                # Código fuente principal del sistema
└── README.md