"""
Genera datos sintéticos de un e-commerce y los inserta en PostgreSQL.

Los datos incluyen imperfecciones A PROPÓSITO (nulos, duplicados,
formatos de fecha inconsistentes, mayúsculas/minúsculas mezcladas)
para que el proceso de limpieza en Python tenga sentido real.

Requisitos:
    pip install psycopg2-binary faker

Antes de ejecutar, ajusta los datos de conexión en DB_CONFIG.
"""

import random
import psycopg2
from faker import Faker
from datetime import timedelta

fake = Faker("es_CO")  # nombres/direcciones con sabor colombiano
random.seed(42)
Faker.seed(42)

# ------------------------------------------------------------
# CONFIGURACIÓN DE CONEXIÓN — AJUSTA ESTOS VALORES
# ------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "ecommerce_portfolio",
    "user": "soporte",
    "password": "contraseña",
}

N_CLIENTES = 300
N_PRODUCTOS = 60
N_PEDIDOS = 1200

CATEGORIAS = ["Electrónica", "Ropa", "Hogar", "Deportes", "Juguetes", "Libros"]
METODOS_PAGO = ["Tarjeta de crédito", "PSE", "Efectivo contra entrega", "Nequi"]
ESTADOS = ["Completado", "Completado", "Completado", "Cancelado", "Pendiente"]

# Formatos de fecha variados, simulando que los datos vienen de
# distintos sistemas de origen (a propósito, para practicar limpieza)
FORMATOS_FECHA = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"]


def formatear_fecha_sucia(fecha):
    """Devuelve la fecha en un formato aleatorio, y a veces vacía."""
    if random.random() < 0.03:
        return None  # 3% de fechas faltantes
    formato = random.choice(FORMATOS_FECHA)
    return fecha.strftime(formato)


def generar_clientes(n):
    clientes = []
    for i in range(n):
        nombre = fake.name()
        # 5% de emails nulos, simulando datos incompletos del formulario
        email = None if random.random() < 0.05 else fake.email()
        ciudad = fake.city()
        pais = "Colombia"
        fecha_registro = fake.date_between(start_date="-3y", end_date="-1m")
        clientes.append((nombre, email, ciudad, pais, fecha_registro))

    # Insertamos duplicados a propósito (mismo cliente registrado dos veces)
    duplicados = random.sample(clientes, k=max(1, n // 30))
    clientes.extend(duplicados)
    return clientes


def generar_productos(n):
    productos = []
    for i in range(n):
        nombre = fake.word().capitalize() + " " + fake.word().capitalize()
        # Categoría con inconsistencias de mayúsculas/minúsculas a propósito
        categoria_base = random.choice(CATEGORIAS)
        categoria = random.choice([categoria_base, categoria_base.upper(), categoria_base.lower()])
        costo = round(random.uniform(5000, 300000), 2)
        margen = random.uniform(1.2, 2.5)
        precio = round(costo * margen, 2)
        productos.append((nombre, categoria, precio, costo))
    return productos


def generar_pedidos_y_detalle(n_pedidos, n_clientes, n_productos):
    pedidos = []
    detalles = []
    for i in range(n_pedidos):
        cliente_id = random.randint(1, n_clientes)
        fecha = fake.date_time_between(start_date="-1y", end_date="now")
        fecha_str = formatear_fecha_sucia(fecha)
        estado = random.choice(ESTADOS)
        metodo_pago = random.choice(METODOS_PAGO)
        pedidos.append((cliente_id, fecha_str, estado, metodo_pago))

        # cada pedido tiene entre 1 y 5 líneas de producto
        n_lineas = random.randint(1, 5)
        productos_pedido = random.sample(range(1, n_productos + 1), k=min(n_lineas, n_productos))
        for producto_id in productos_pedido:
            cantidad = random.randint(1, 4)
            # 1% de cantidades en cero, simulando un error de captura
            if random.random() < 0.01:
                cantidad = 0
            precio_unitario = round(random.uniform(5000, 500000), 2)
            detalles.append((i + 1, producto_id, cantidad, precio_unitario))

    return pedidos, detalles


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("Generando clientes...")
    clientes = generar_clientes(N_CLIENTES)
    cur.executemany(
        "INSERT INTO clientes (nombre, email, ciudad, pais, fecha_registro) VALUES (%s, %s, %s, %s, %s)",
        clientes,
    )

    print("Generando productos...")
    productos = generar_productos(N_PRODUCTOS)
    cur.executemany(
        "INSERT INTO productos (nombre_producto, categoria, precio_unitario, costo_unitario) VALUES (%s, %s, %s, %s)",
        productos,
    )

    print("Generando pedidos y detalle...")
    pedidos, detalles = generar_pedidos_y_detalle(N_PEDIDOS, N_CLIENTES, N_PRODUCTOS)
    cur.executemany(
        "INSERT INTO pedidos (cliente_id, fecha_pedido, estado, metodo_pago) VALUES (%s, %s, %s, %s)",
        pedidos,
    )
    cur.executemany(
        "INSERT INTO detalle_pedidos (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
        detalles,
    )

    conn.commit()
    cur.close()
    conn.close()
    print(f"Listo: {len(clientes)} clientes, {len(productos)} productos, "
          f"{len(pedidos)} pedidos, {len(detalles)} líneas de detalle.")


if __name__ == "__main__":
    main()
