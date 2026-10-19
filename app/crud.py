import sqlite3
from app.database import obtener_conexion

def registrar_producto(nombre: str, precio_compra: float, precio_venta: float, stock_actual: int, stock_minimo: int = 5):
    """Inserta un nuevo producto en la base de datos."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO productos (nombre, precio_compra, precio_venta, stock_actual, stock_minimo)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre.strip(), precio_compra, precio_venta, stock_actual, stock_minimo))
        conn.commit()
        print(f">> Producto '{nombre}' guardado con éxito.")
    except sqlite3.IntegrityError:
        print(f">> Aviso: El producto '{nombre}' ya existe en la base de datos.")
    finally:
        conn.close()

def listar_productos():
    """Consulta y retorna todos los productos registrados."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio_compra, precio_venta, stock_actual, stock_minimo FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def registrar_venta(producto_id: int, cantidad: int):
    """Registra una venta y descuenta el stock de manera transaccional."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # 1. Verificar si el producto existe y cuánto stock tiene
    cursor.execute("SELECT nombre, precio_venta, stock_actual FROM productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()

    if not producto:
        print(f">> Error: El producto con ID {producto_id} no existe.")
        conn.close()
        return False

    nombre = producto["nombre"]
    precio_venta = producto["precio_venta"]
    stock_actual = producto["inventario_actual"]

    if stock_actual < cantidad:
        print(f">> Stock insuficiente para '{nombre}'. Solicitado: {cantidad}, Disponible: {stock_actual}")
        conn.close()
        return False

    # 2. Calcular total
    total = precio_venta * cantidad

    # 3. Guardar en tabla ventas
    cursor.execute("INSERT INTO ventas (total) VALUES (?)", (total,))
    venta_id = cursor.lastrowid

    # 4. Guardar en tabla detalle_ventas
    cursor.execute("""
        INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario)
        VALUES (?, ?, ?, ?)
    """, (venta_id, producto_id, cantidad, precio_venta))

    # 5. Descontar el stock del producto
    nuevo_stock = stock_actual - cantidad
    cursor.execute("UPDATE productos SET stock_actual = ? WHERE id = ?", (nuevo_stock, producto_id))

    conn.commit()
    conn.close()
    print(f">> Venta registrada: {cantidad}x '{nombre}' por ${total:.2f}. Stock restante: {nuevo_stock}")
    return True

def obtener_alertas_stock():
    """Retorna los productos que están en o por debajo de su stock mínimo."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, stock_actual, stock_minimo 
        FROM productos 
        WHERE stock_actual <= stock_minimo
    """)
    alertas = cursor.fetchall()
    conn.close()
    return alertas

if __name__ == "__main__":
    print("--- 1. Probando una venta exitosa ---")
    # Vendemos 2 libretas (ID: 1)
    registrar_venta(producto_id=1, cantidad=2)

    print("\n--- 2. Probando vender más de lo disponible ---")
    # Intentamos vender 50 bolígrafos (ID: 2) cuando solo hay 3
    registrar_venta(producto_id=2, cantidad=50)

    print("\n--- 3. Revisando Alertas de Stock Crítico ---")
    alertas = obtener_alertas_stock()
    if alertas:
        for a in alertas:
            print(f" ALERTA: '{a['nombre']}' tiene {a['stock_actual']} piezas (Mínimo requerido: {a['stock_minimo']})")
    else:
        print("Todo el stock está en niveles óptimos.")
