# 📊 Dashboard de Ventas E-commerce

Proyecto de análisis de datos de principio a fin: desde una base de datos relacional con datos "sucios" hasta un dashboard interactivo en Power BI, pasando por limpieza y análisis exploratorio en Python.

## Objetivo

Simular el flujo de trabajo de un analista de datos en una empresa real: extraer datos de una base de datos relacional, limpiarlos, analizarlos, y comunicar hallazgos de negocio a través de un dashboard.

## Tecnologías usadas

- **PostgreSQL** — base de datos relacional (4 tablas: clientes, productos, pedidos, detalle_pedidos)
- **Python** (pandas, SQLAlchemy, Faker, matplotlib) — generación de datos sintéticos, limpieza y análisis exploratorio
- **Power BI** — modelado de datos y dashboard interactivo

## Hallazgos principales

- La categoría **Deportes** lidera las ventas por un margen amplio sobre el resto, señal de que vale la pena priorizar inventario y promociones en esa línea de producto.
- Las ventas alcanzaron su punto más alto en **agosto**, pero mostraron una caída notable en los meses de cierre de año — un comportamiento atípico si se considera que noviembre y diciembre suelen ser meses de alta demanda por temporada de fiestas. Esto sugiere investigar la causa: un problema de stock, una campaña que no se ejecutó, o un cambio real en el comportamiento de los clientes.

## Estructura del proyecto

```
├── schema.sql              # Esquema de la base de datos (4 tablas)
├── generar_datos.py        # Genera datos sintéticos con imperfecciones intencionales
├── analisis_ecommerce.ipynb # Limpieza de datos y análisis exploratorio
├── requirements.txt         # Dependencias de Python
└── README.md
```

## Problemas de datos simulados (y cómo se resolvieron)

Los datos se generaron con imperfecciones intencionales, típicas de un entorno real:

| Problema | Solución aplicada |
|---|---|
| Emails nulos en clientes (5%) | Se marcaron en vez de inventar datos falsos |
| Clientes duplicados | Se eliminaron duplicados exactos |
| Categorías con mayúsculas/minúsculas inconsistentes | Normalizadas a formato título |
| Fechas en 4 formatos distintos | Conversión automática con `pd.to_datetime(format='mixed')` |
| Líneas de pedido con cantidad = 0 | Descartadas (errores de captura) |

## Cómo correrlo

1. Clona el repositorio e instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

2. Crea la base de datos en PostgreSQL y ejecuta el esquema:
   ```
   createdb ecommerce_portfolio
   psql -d ecommerce_portfolio -f schema.sql
   ```

3. Abre `generar_datos.py` y ajusta `DB_CONFIG` con tus propias credenciales de PostgreSQL. Luego ejecuta:
   ```
   python generar_datos.py
   ```

4. Abre `analisis_ecommerce.ipynb` en Jupyter, ajusta las credenciales en la celda de conexión, y corre todas las celdas.

5. Abre Power BI Desktop y conéctate a las tablas `limpio_*` generadas en PostgreSQL (o importa los CSV exportados por el notebook).

## Autor

Juan David Burbano — [LinkedIn](https://www.linkedin.com/in/juan-david-burbano-pineda-181b61296/) · [GitHub](#)
