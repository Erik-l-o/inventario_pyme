import sqlite3

DB_NAME = "inventario.db"

def obtener_conexion():
    """Crea y retorna una conexión a la base de datos local."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_bd():
    """Crea las tablas necesarias si no existen."""
    conn = obtener_conexion()
    cursor = conn.cursor()

    # 1. Tabla de Productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            precio_compra REAL NOT NULL,
            precio_venta REAL NOT NULL,
            stock_actual INTEGER NOT NULL,
            stock_minimo INTEGER NOT NULL DEFAULT 5
        )
    """)

    # 2. Tabla de Ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL
        )
    """)

    # 3. Tabla de Detalle de Venta
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas (id),
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    """)

    conn.commit()
    conn.close()
    print(">> Base de datos inicializada correctamente.")

if __name__ == "__main__":
    inicializar_bd()