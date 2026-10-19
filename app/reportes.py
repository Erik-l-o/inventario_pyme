import csv
import os
from datetime import datetime
from app.database import obtener_conexion

def generar_reporte_ventas():
    """Genera un archivo CSV con el detalle de ventas realizadas."""
    os.makedirs("reportes_generados", exist_ok=True)
    
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Consulta uniendo detalle_ventas con productos y ventas
    cursor.execute("""
        SELECT 
            v.id AS venta_id,
            v.fecha,
            p.nombre AS producto,
            d.cantidad,
            d.precio_unitario,
            (d.cantidad * d.precio_unitario) AS subtotal
        FROM detalle_ventas d
        JOIN ventas v ON d.venta_id = v.id
        JOIN productos p ON d.producto_id = p.id
        ORDER BY v.fecha DESC
    """)
    filas = cursor.fetchall()
    conn.close()

    if not filas:
        print(">> No hay ventas registradas para generar el reporte.")
        return None

    # Nombre de archivo con fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"reportes_generados/reporte_ventas_{timestamp}.csv"

    # Escribir el archivo CSV
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8-sig") as archivo:
        writer = csv.writer(archivo)
        # Encabezados de columna
        writer.writerow(["ID Venta", "Fecha y Hora", "Producto", "Cantidad", "Precio Unitario", "Subtotal"])
        
        total_acumulado = 0.0
        for f in filas:
            writer.writerow([
                f["venta_id"],
                f["fecha"],
                f["producto"],
                f["cantidad"],
                f"${f['precio_unitario']:.2f}",
                f"${f['subtotal']:.2f}"
            ])
            total_acumulado += f["subtotal"]
        
        # Renglón de total global
        writer.writerow([])
        writer.writerow(["", "", "", "", "TOTAL ACUMULADO:", f"${total_acumulado:.2f}"])

    print(f">> Reporte generado exitosamente en: {nombre_archivo}")
    return nombre_archivo

if __name__ == "__main__":
    generar_reporte_ventas()