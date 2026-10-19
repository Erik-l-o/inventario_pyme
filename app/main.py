import sys
from app.database import inicializar_bd
from app.crud import registrar_producto, listar_productos, registrar_venta, obtener_alertas_stock
from app.reportes import generar_reporte_ventas

def mostrar_menu():
    print("\n" + "=" * 48)
    print(" BIENVENIDO A TU SISTEMA DE CONTROL")
    print("=" * 48)
    print("1. Registrar nuevo producto")
    print("2. Consultar inventario completo")
    print("3. Registrar una venta")
    print("4. Ver alertas de stock crítico")
    print("5. Generar reporte de ventas (.csv)")
    print("6. Salir")
    print("-" * 48)

def ejecutar_sistema():
    inicializar_bd()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción [1-6]: ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR PRODUCTO ---")
            nombre = input("Nombre del producto: ").strip()
            try:
                precio_compra = float(input("Precio de compra: $"))
                precio_venta = float(input("Precio de venta: $"))
                stock = int(input("Cantidad inicial en inventario: "))
                minimo = int(input("cantidad de inventario mínimo de alerta (por defecto 5): ") or 5)
                registrar_producto(nombre, precio_compra, precio_venta, stock, minimo)
            except ValueError:
                print(">> Error: Ingresa números válidos.")

        elif opcion == "2":
            print("\n--- INVENTARIO ACTUAL ---")
            productos = listar_productos()
            if not productos:
                print("No hay productos registrados en el sistema.")
            else:
                for p in productos:
                    print(f"ID: {p['id']:<3} | {p['nombre']:<20} | Stock: {p['stock_actual']:<4} | Precio: ${p['precio_venta']:.2f}")

        elif opcion == "3":
            print("\n--- REGISTRAR VENTA ---")
            try:
                prod_id = int(input("ID del producto a vender: "))
                cantidad = int(input("Cantidad a vender: "))
                if cantidad <= 0:
                    print(">> La cantidad debe ser mayor a 0.")
                else:
                    registrar_venta(prod_id, cantidad)
            except ValueError:
                print(">> Error: Ingresa valores numéricos válidos.")

        elif opcion == "4":
            print("\n--- ALERTAS DE STOCK CRÍTICO ---")
            alertas = obtener_alertas_stock()
            if alertas:
                for a in alertas:
                    print(f"  ALERTA: '{a['nombre']}' tiene {a['stock_actual']} uds (Mínimo: {a['stock_minimo']})")
            else:
                print(" Todo el inventario se encuentra en niveles óptimos.")

        elif opcion == "5":
            print("\n--- GENERANDO REPORTE ---")
            generar_reporte_ventas()

        elif opcion == "6":
            print("\n>> Saliendo del sistema. ¡Hasta luego!")
            sys.exit(0)

        else:
            print(">> Opción no válida. Intente con un número del 1 al 6.")

if __name__ == "__main__":
    ejecutar_sistema()