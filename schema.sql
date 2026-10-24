-- ============================================================
-- Esquema de base de datos: E-commerce
-- Motor: PostgreSQL
-- ============================================================

DROP TABLE IF EXISTS detalle_pedidos CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

-- ------------------------------------------------------------
-- Tabla: clientes
-- ------------------------------------------------------------
CREATE TABLE clientes (
    cliente_id      SERIAL PRIMARY KEY,
    nombre          VARCHAR(150),
    email           VARCHAR(150),
    ciudad          VARCHAR(100),
    pais            VARCHAR(100),
    fecha_registro  DATE
);

-- ------------------------------------------------------------
-- Tabla: productos
-- ------------------------------------------------------------
CREATE TABLE productos (
    producto_id     SERIAL PRIMARY KEY,
    nombre_producto VARCHAR(150),
    categoria       VARCHAR(100),
    precio_unitario NUMERIC(10,2),
    costo_unitario  NUMERIC(10,2)
);

-- ------------------------------------------------------------
-- Tabla: pedidos (cabecera de cada pedido)
-- ------------------------------------------------------------
CREATE TABLE pedidos (
    pedido_id       SERIAL PRIMARY KEY,
    cliente_id      INTEGER REFERENCES clientes(cliente_id),
    fecha_pedido    VARCHAR(20),  -- se deja como texto a propósito: formatos inconsistentes
    estado          VARCHAR(30),  -- 'Completado', 'Cancelado', 'Pendiente', etc.
    metodo_pago     VARCHAR(50)
);

-- ------------------------------------------------------------
-- Tabla: detalle_pedidos (líneas de cada pedido)
-- ------------------------------------------------------------
CREATE TABLE detalle_pedidos (
    detalle_id      SERIAL PRIMARY KEY,
    pedido_id       INTEGER REFERENCES pedidos(pedido_id),
    producto_id     INTEGER REFERENCES productos(producto_id),
    cantidad        INTEGER,
    precio_unitario NUMERIC(10,2)  -- precio al momento de la venta (puede diferir del actual)
);

-- Índices útiles para el análisis
CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX idx_detalle_pedido ON detalle_pedidos(pedido_id);
CREATE INDEX idx_detalle_producto ON detalle_pedidos(producto_id);
