import pandas as pd

# Ruta del archivo de inventario
inventario_path = "/Users/santi/Documents/Universidad/Primer Semestre ICESI/Introducción a la Ingeniería de Sistemas/Python/inventario.xlsx"

def actualizar_inventario_pandas(pedido):
    """
    Actualiza el inventario utilizando pandas para modificar el archivo de Excel.
    """
    try:
        # Leer el archivo de inventario
        df_inventario = pd.read_excel(inventario_path)

        # Iterar por cada producto en el pedido y actualizar el inventario
        for item in pedido:
            nombre_producto = item["nombre"]
            cantidad_vendida = item["cantidad"]
            
            # Filtrar el DataFrame para el producto vendido
            if nombre_producto in df_inventario["Nombre"].values:
                index = df_inventario[df_inventario["Nombre"] == nombre_producto].index[0]
                nueva_cantidad = max(0, df_inventario.at[index, "Cantidad"] - cantidad_vendida)
                df_inventario.at[index, "Cantidad"] = nueva_cantidad
            else:
                print(f"Producto '{nombre_producto}' no encontrado en el inventario.")

        # Guardar los cambios de vuelta al archivo Excel
        df_inventario.to_excel(inventario_path, index=False)
        print("Inventario actualizado exitosamente.")
    
    except FileNotFoundError:
        print(f"Archivo de inventario no encontrado en la ruta: {inventario_path}")
    except Exception as e:
        print(f"Error al actualizar el inventario: {e}")

def registrar_pedido_pandas(tipo):
    mostrar_menu()
    pedido = []
    total = 0

    while True:
        try:
            seleccion = int(input("\nSelecciona el número del producto (0 para finalizar): "))
            if seleccion == 0:
                break
            cantidad = int(input(f"¿Cuántos deseas de {productos[seleccion - 1]['nombre']}? "))
            producto = productos[seleccion - 1]
            pedido.append({"nombre": producto["nombre"], "cantidad": cantidad, "subtotal": producto["precio"] * cantidad})
            total += producto["precio"] * cantidad
        except (ValueError, IndexError):
            print("Selección inválida. Intenta de nuevo.")

    if pedido:
        print("entre peduido")
        actualizar_inventario_pandas(pedido)  # Actualizar el inventario con pandas

    return pedido, total

def atencion_mesa_pandas():
    print("\n--- Mesas disponibles ---")
    for mesa in mesas:
        estado = "Ocupada" if mesa["ocupada"] else "Libre"
        print(f"Mesa {mesa['numero']}: {estado}")
    
    try:
        mesa_num = int(input("\nSelecciona el número de la mesa: "))
        mesa = mesas[mesa_num - 1]
        if mesa["ocupada"]:
            print("Esta mesa ya está ocupada. Por favor selecciona otra.")
        else:
            mesa["pedidos"], mesa["total"] = registrar_pedido_pandas("mesa")
            mesa["ocupada"] = True
            print(f"\nPedido registrado para la mesa {mesa_num}.")
    except (ValueError, IndexError):
        print("Número de mesa inválido.")

def compra_para_llevar_pandas():
    print("\n--- Compra para llevar ---")
    pedido, total = registrar_pedido_pandas("llevar")
    
    if total > 0:
        print(f"\nTotal a pagar: ${total}")
        try:
            pago = float(input("Introduce el monto pagado: "))
            if pago >= total:
                cambio = pago - total
                print(f"Cambio: ${cambio}")
                ventas.append({"tipo": "llevar", "pedido": pedido, "total": total})
                print("\nCompra registrada con éxito.")
            else:
                print("El monto es insuficiente. No se pudo completar la compra.")
        except ValueError:
            print("Monto de pago inválido. No se pudo completar la compra.")
    else:
        print("No se registraron productos en el pedido.")

#Inventario
productos = [
    {"nombre": "Empanada", "categoria": "Alimento", "precio": 1200},
    {"nombre": "Papa", "categoria": "Alimento", "precio": 1600},
    {"nombre": "Papa rellena", "categoria": "Alimento", "precio": 3500},
    {"nombre": "Salchichón", "categoria": "Alimento", "precio": 600},
    {"nombre": "Ala de pollo", "categoria": "Alimento", "precio": 4000},
    {"nombre": "Pescado", "categoria": "Alimento", "precio": 7000},
    {"nombre": "Aborrajado", "categoria": "Alimento", "precio": 2000},
    {"nombre": "Coca cola 500ml", "categoria": "Bebida", "precio": 3000},
    {"nombre": "Coca cola 250ml", "categoria": "Bebida", "precio": 1600},
    {"nombre": "Jugo hit 1200ml", "categoria": "Bebida", "precio": 3500},
    {"nombre": "Jugo hit 400ml", "categoria": "Bebida", "precio": 2200},
    {"nombre": "Jugo hit 250ml", "categoria": "Bebida", "precio": 1500},
    {"nombre": "Postobon Acqua 400ml", "categoria": "Bebida", "precio": 1500},
    {"nombre": "Speedmax 400ml", "categoria": "Bebida", "precio": 1500},
    {"nombre": "Natumalta p 200ml", "categoria": "Bebida", "precio": 1300},
    {"nombre": "Natumalta m 400ml", "categoria": "Bebida", "precio": 2000},
    {"nombre": "Agua cristal 500ml", "categoria": "Bebida", "precio": 1500},
    {"nombre": "Postobon personal vidrio 400ml", "categoria": "Bebida", "precio": 1200},
    {"nombre": "Pepsi grande 1000ml", "categoria": "Bebida", "precio": 3500}, 
    {"nombre": "Natumalta grande 1000ml", "categoria": "Bebida", "precio": 3650}, 
    {"nombre": "Tropikola 400ml", "categoria":"Bebida", "precio" : 1500}, 
    {"nombre" : "Squash Personal", "categoría" : "Bebida", "precio":2500}, 
    {"nombre" : "Mr tea personal 400ml", "categoria" : "Bebida", "precio" : 2000}, 
    {"nombre" : "Tutti frutti 400ml", "categoria" : "Bebida", "precio" : 1200}, 
    {"nombre" : "H20h 600ml", "categoria" : "Bebida", "precio" : 1800}
]

mesas = [{"numero": i + 1, "ocupada": False, "pedidos": [], "total": 0} for i in range(5)]
ventas = []

def mostrar_menu():
    print("\n--- Menú de productos ---")
    for idx, producto in enumerate(productos):
        print(f"{idx + 1}. {producto['nombre']} - ${producto['precio']}")

# Función para pagar una mesa
def pagar_mesa():
    print("\n--- Mesas ocupadas ---")
    ocupadas = [mesa for mesa in mesas if mesa["ocupada"]]
    if not ocupadas:
        print("No hay mesas ocupadas.")
        return

    for mesa in ocupadas:
        print(f"Mesa {mesa['numero']} - Total a pagar: ${mesa['total']}")
    
    try:
        mesa_num = int(input("\nSelecciona el número de la mesa que va a pagar: "))
        mesa = mesas[mesa_num - 1]
        if not mesa["ocupada"]:
            print("Esta mesa no está ocupada.")
        else:
            print(f"\nTotal a pagar: ${mesa['total']}")
            pago = float(input("Introduce el monto pagado: "))
            if pago >= mesa["total"]:
                cambio = pago - mesa["total"]
                print(f"Cambio: ${cambio}")
                ventas.append({"tipo": "mesa", "pedido": mesa["pedidos"], "total": mesa["total"]})
                mesa["ocupada"] = False
                mesa["pedidos"] = []
                mesa["total"] = 0
            else:
                print("El monto es insuficiente.")
    except (ValueError, IndexError):
        print("Número de mesa inválido.")


# Función para generar reporte de ventas
def generar_reporte():
    """
    Genera un reporte detallado de las ventas, incluyendo cuántas unidades se vendieron
    de cada producto y cuánto dinero generaron.
    Permite ordenar el reporte según el criterio elegido (nombre, cantidad, dinero recaudado).
    """
    # Calcular la cantidad total de unidades vendidas y el dinero recaudado por producto
    productos_reporte = {}
    for venta in ventas:
        for item in venta["pedido"]:
            nombre = item["nombre"]
            cantidad = item["cantidad"]
            subtotal = item["subtotal"]
            if nombre in productos_reporte:
                productos_reporte[nombre]["cantidad"] += cantidad
                productos_reporte[nombre]["total"] += subtotal
            else:
                productos_reporte[nombre] = {"cantidad": cantidad, "total": subtotal}

    # Convertir el diccionario en una lista para ordenarlo
    reporte = [{"nombre": nombre, **datos} for nombre, datos in productos_reporte.items()]

    # Menú de opciones para ordenar el reporte
    print("\n--- Opciones de ordenamiento del reporte ---")
    print("1. Ordenar por nombre")
    print("2. Ordenar por cantidad vendida")
    print("3. Ordenar por dinero recaudado")
    try:
        criterio = int(input("Selecciona un criterio de ordenamiento: "))
        if criterio not in [1, 2, 3]:
            raise ValueError("Criterio no válido")
        ascendente = input("¿Orden ascendente? (s/n): ").strip().lower() == "s"

        # Ordenar el reporte según el criterio seleccionado
        if criterio == 1:
            bubble_sort_reporte(reporte, clave="nombre", ascendente=ascendente)
        elif criterio == 2:
            bubble_sort_reporte(reporte, clave="cantidad", ascendente=ascendente)
        elif criterio == 3:
            bubble_sort_reporte(reporte, clave="total", ascendente=ascendente)

        # Mostrar el reporte ordenado
        print("\n--- Reporte de ventas ---")
        for item in reporte:
            print(f"{item['nombre']}: {item['cantidad']} unidades, total: ${item['total']}")
        print(f"\nTotal del día: ${sum(venta['total'] for venta in ventas)}")

    except ValueError:
        print("Entrada no válida. No se pudo generar el reporte.")


def bubble_sort_reporte(lista, clave, ascendente=True):
    """
    Ordena el reporte según la clave especificada (nombre, cantidad, total) usando Bubble Sort.
    """
    n = len(lista)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if (ascendente and lista[j][clave] > lista[j + 1][clave]) or \
               (not ascendente and lista[j][clave] < lista[j + 1][clave]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]




# Función principal
def menu():
    while True:
        print("\n--- Sistema Frito's Maritza ---")
        print("1. Atención en mesa")
        print("2. Compra para llevar")
        print("3. Pagar una mesa")
        print("4. Generar reporte de ventas")
        print("5. Salir")
        try:
            opcion = int(input("Selecciona una opción: "))
            if opcion == 1:
                atencion_mesa_pandas()
            elif opcion == 2:
                compra_para_llevar_pandas()
            elif opcion == 3:
                pagar_mesa()
            elif opcion == 4:
                generar_reporte()
            elif opcion == 5:
                flag = all(not mesa["ocupada"] for mesa in mesas)
                if flag == True:
                    break
                else:
                    print("Faltan mesas por cobrar")
                
            else:
                print("Opción no válida.")
        except ValueError:
            print("Entrada no válida. Intenta de nuevo.")

# Ejecutar el menú principal
menu()