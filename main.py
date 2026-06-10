import sys
sys.stdout.reconfigure(encoding="utf-8")

from tienda import Tienda
from datos_ejemplo import cargar_datos


# ------------------------------------------------------------------ #
# Utilidades de display
# ------------------------------------------------------------------ #

def linea(ancho=60):
    print("-" * ancho)

def titulo(texto, ancho=60):
    linea(ancho)
    print(f"  {texto}")
    linea(ancho)

def stats(tienda):
    disponibles = len(tienda.listar_disponibles())
    activos     = len(tienda.listar_alquileres_activos())
    vencidos    = len(tienda.listar_alquileres_vencidos())
    clientes    = len(tienda.listar_clientes())
    venc_txt    = f"  !! {vencidos} vencido(s)" if vencidos else ""
    print(f"  Disponibles: {disponibles}  |  Alquileres activos: {activos}{venc_txt}  |  Clientes: {clientes}")

def mostrar_lista(items, vacio="No hay elementos para mostrar."):
    if not items:
        print(f"    {vacio}")
    else:
        for item in items:
            print(f"  {item}")

def pedir_condicion():
    print("  Condicion:")
    print("  1. Nuevo")
    print("  2. Usado - Excelente")
    print("  3. Usado - Bueno")
    print("  4. Usado - Regular")
    opciones = {"1": "Nuevo", "2": "Usado - Excelente", "3": "Usado - Bueno", "4": "Usado - Regular"}
    while True:
        op = input("  Opcion [1-4]: ").strip()
        if op in opciones:
            return opciones[op]
        print("  Opcion invalida.")


def pedir_cliente(tienda):
    """Busca un cliente por DNI. Si no existe, ofrece registrarlo en el momento."""
    while True:
        dni = input("  DNI del cliente: ").strip()
        if not dni:
            print("  El DNI no puede estar vacio.")
            continue

        cliente = tienda.buscar_cliente_por_dni(dni)
        if cliente:
            print(f"  Cliente: {cliente.nombre_completo()} (DNI {cliente.dni})")
            return cliente

        print(f"  No se encontro un cliente con DNI {dni}.")
        respuesta = input("  Desea registrarlo ahora? [s/n]: ").strip().lower()
        if respuesta != "s":
            return None

        try:
            nombre    = input("  Nombre: ").strip()
            apellido  = input("  Apellido: ").strip()
            email     = input("  Email: ").strip()
            telefono  = input("  Telefono (opcional): ").strip()
            direccion = input("  Direccion (opcional): ").strip()
            cliente = tienda.registrar_cliente(nombre, apellido, dni, email, telefono, direccion)
            print(f"  Cliente registrado: {cliente.nombre_completo()}")
            return cliente
        except ValueError as e:
            print(f"  Error: {e}")



# ------------------------------------------------------------------ #
# Menu: Ventas
# ------------------------------------------------------------------ #

def menu_ventas(tienda):
    while True:
        titulo("VENTAS")
        print("  1. Registrar venta")
        print("  2. Historial de ventas")
        print("  0. Volver")
        linea()
        op = input("  Opcion: ").strip()

        if op == "1":
            try:
                codigo = input("  Codigo del articulo: ").strip()
                cliente = pedir_cliente(tienda)
                if cliente is None:
                    continue
                venta = tienda.registrar_venta(codigo, cliente.numero)
                print(f"\n  Venta registrada: {venta}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "2":
            mostrar_lista(tienda.listar_ventas(), "No hay ventas registradas.")

        elif op == "0":
            break
        else:
            print("  Opcion invalida.")


# ------------------------------------------------------------------ #
# Menu: Alquileres
# ------------------------------------------------------------------ #

def menu_alquileres(tienda):
    while True:
        titulo("ALQUILERES")
        print("  1. Registrar alquiler")
        print("  2. Registrar devolucion")
        print("  3. Ver alquileres activos")
        print("  4. Ver alquileres vencidos")
        print("  0. Volver")
        linea()
        op = input("  Opcion: ").strip()

        if op == "1":
            try:
                codigo         = input("  Codigo del articulo: ").strip()
                cliente = pedir_cliente(tienda)
                if cliente is None:
                    continue
                dias           = int(input("  Dias de alquiler: "))
                precio_por_dia = int(input("  Precio por dia ($): "))
                alquiler = tienda.registrar_alquiler(codigo, cliente.numero, dias, precio_por_dia)
                print(f"\n  Alquiler registrado: {alquiler}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "2":
            activos = tienda.listar_alquileres_activos()
            if not activos:
                print("  No hay alquileres activos.\n")
                continue
            print("  Alquileres activos:")
            mostrar_lista(activos)
            linea()
            try:
                id_a = int(input("  ID del alquiler a devolver: "))
                alquiler = tienda.devolver_alquiler(id_a)
                print(f"\n  Devolucion registrada: {alquiler}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "3":
            mostrar_lista(tienda.listar_alquileres_activos(), "No hay alquileres activos.")

        elif op == "4":
            mostrar_lista(tienda.listar_alquileres_vencidos(), "No hay alquileres vencidos.")

        elif op == "0":
            break
        else:
            print("  Opcion invalida.")


# ------------------------------------------------------------------ #
# Menu: Consignaciones
# ------------------------------------------------------------------ #

def menu_consignaciones(tienda):
    while True:
        titulo("CONSIGNACIONES")
        print("  1. Recibir articulo de cliente")
        print("  2. Registrar venta de consignacion")
        print("  3. Ver consignaciones activas")
        print("  4. Ver consignaciones vendidas")
        print("  5. Devolver articulo al cliente")
        print("  0. Volver")
        linea()
        op = input("  Opcion: ").strip()

        if op == "1":
            try:
                print("  Tipo de articulo:")
                print("  1. Comic")
                print("  2. Manga")
                print("  3. Carta")
                print("  4. Pack de cartas")
                tipo = input("  Tipo [1-4]: ").strip()
                if tipo not in ("1", "2", "3", "4"):
                    print("  Tipo invalido.")
                    continue

                titulo_a  = input("  Titulo: ").strip()
                condicion = pedir_condicion()

                if tipo == "1":
                    editorial = input("  Editorial: ").strip()
                    num_ed    = int(input("  Numero de edicion: "))
                    personaje = input("  Personaje/Serie: ").strip()
                elif tipo == "2":
                    editorial = input("  Editorial: ").strip()
                    volumen   = int(input("  Volumen: "))
                    autor     = input("  Autor: ").strip()
                elif tipo == "3":
                    juego  = input("  Juego: ").strip()
                    rareza = input("  Rareza: ").strip()
                else:
                    juego    = input("  Juego: ").strip()
                    cantidad = int(input("  Cantidad de cartas: "))
                    edicion  = input("  Edicion: ").strip()

                cliente = pedir_cliente(tienda)
                if cliente is None:
                    continue

                precio     = int(input("  Precio de venta acordado ($): "))
                porcentaje = input("  Porcentaje para el cliente [Enter = 70%]: ").strip()
                porcentaje = int(porcentaje) if porcentaje else 70

                if tipo == "1":
                    codigo = tienda.generar_codigo("C")
                    tienda.registrar_comic(codigo, titulo_a, precio, editorial, num_ed, personaje, condicion)
                elif tipo == "2":
                    codigo = tienda.generar_codigo("M")
                    tienda.registrar_manga(codigo, titulo_a, precio, editorial, volumen, autor, condicion)
                elif tipo == "3":
                    codigo = tienda.generar_codigo("CT")
                    tienda.registrar_carta(codigo, titulo_a, precio, juego, rareza, condicion)
                else:
                    codigo = tienda.generar_codigo("P")
                    tienda.registrar_pack(codigo, titulo_a, precio, juego, cantidad, edicion, condicion)

                cons = tienda.registrar_consignacion(codigo, cliente.numero, precio, porcentaje)
                print(f"\n  Consignacion registrada (codigo interno: {codigo})")
                print(f"  {cons}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "2":
            activas = tienda.listar_consignaciones_activas()
            if not activas:
                print("  No hay consignaciones activas.\n")
                continue
            print("  Consignaciones activas:")
            mostrar_lista(activas)
            linea()
            try:
                id_c = int(input("  ID de la consignacion a vender: "))
                cons = tienda.vender_consignacion(id_c)
                print(f"\n  Vendido. Pago al cliente: ${cons.calcular_pago_cliente():,}\n")
                print(f"  {cons}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "3":
            mostrar_lista(tienda.listar_consignaciones_activas(), "No hay consignaciones activas.")

        elif op == "4":
            mostrar_lista(tienda.listar_consignaciones_vendidas(), "No hay consignaciones vendidas.")

        elif op == "5":
            activas = tienda.listar_consignaciones_activas()
            if not activas:
                print("  No hay consignaciones activas.\n")
                continue
            print("  Consignaciones activas:")
            mostrar_lista(activas)
            linea()
            try:
                id_c = int(input("  ID de la consignacion a retirar: "))
                cons = tienda.retirar_consignacion(id_c)
                print(f"\n  Articulo devuelto al cliente. {cons}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "0":
            break
        else:
            print("  Opcion invalida.")


# ------------------------------------------------------------------ #
# Menu: Catalogo
# ------------------------------------------------------------------ #

def menu_catalogo(tienda):
    while True:
        titulo("CATALOGO")
        print("  1. Buscar articulo")
        print("  2. Ver articulos disponibles")
        print("  3. Ver catalogo completo")
        print("  4. Agregar comic")
        print("  5. Agregar manga")
        print("  6. Agregar carta")
        print("  7. Agregar pack de cartas")
        print("  0. Volver")
        linea()
        op = input("  Opcion: ").strip()

        if op == "1":
            termino = input("  Buscar por titulo, editorial, personaje, juego...: ").strip()
            mostrar_lista(tienda.buscar_material(termino), "Sin resultados.")

        elif op == "2":
            mostrar_lista(tienda.listar_disponibles(), "No hay articulos disponibles.")

        elif op == "3":
            mostrar_lista(tienda.listar_catalogo(), "El catalogo esta vacio.")

        elif op == "4":
            try:
                titulo_m  = input("  Titulo: ").strip()
                precio    = int(input("  Precio ($): "))
                editorial = input("  Editorial: ").strip()
                numero    = int(input("  Numero de edicion: "))
                personaje = input("  Personaje/Serie: ").strip()
                condicion = pedir_condicion()
                codigo = tienda.generar_codigo("C")
                m = tienda.registrar_comic(codigo, titulo_m, precio, editorial, numero, personaje, condicion)
                print(f"\n  Registrado con codigo {codigo}: {m}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "5":
            try:
                titulo_m  = input("  Titulo: ").strip()
                precio    = int(input("  Precio ($): "))
                editorial = input("  Editorial: ").strip()
                volumen   = int(input("  Volumen: "))
                autor     = input("  Autor: ").strip()
                condicion = pedir_condicion()
                codigo = tienda.generar_codigo("M")
                m = tienda.registrar_manga(codigo, titulo_m, precio, editorial, volumen, autor, condicion)
                print(f"\n  Registrado con codigo {codigo}: {m}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "6":
            try:
                titulo_m  = input("  Nombre de la carta: ").strip()
                precio    = int(input("  Precio ($): "))
                juego     = input("  Juego (Pokemon TCG / Magic: The Gathering / Yu-Gi-Oh!): ").strip()
                rareza    = input("  Rareza (Comun / Rara / Ultra Rara / Mitica): ").strip()
                condicion = pedir_condicion()
                codigo = tienda.generar_codigo("CT")
                m = tienda.registrar_carta(codigo, titulo_m, precio, juego, rareza, condicion)
                print(f"\n  Registrada con codigo {codigo}: {m}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "7":
            try:
                titulo_m  = input("  Nombre del pack: ").strip()
                precio    = int(input("  Precio ($): "))
                juego     = input("  Juego: ").strip()
                cantidad  = int(input("  Cantidad de cartas: "))
                edicion   = input("  Edicion: ").strip()
                condicion = pedir_condicion()
                codigo = tienda.generar_codigo("P")
                m = tienda.registrar_pack(codigo, titulo_m, precio, juego, cantidad, edicion, condicion)
                print(f"\n  Registrado con codigo {codigo}: {m}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "0":
            break
        else:
            print("  Opcion invalida.")


# ------------------------------------------------------------------ #
# Menu: Clientes
# ------------------------------------------------------------------ #

def menu_clientes(tienda):
    while True:
        titulo("CLIENTES")
        print("  1. Buscar cliente por DNI")
        print("  2. Registrar cliente")
        print("  3. Ver todos los clientes")
        print("  0. Volver")
        linea()
        op = input("  Opcion: ").strip()

        if op == "1":
            dni = input("  DNI a buscar: ").strip()
            c = tienda.buscar_cliente_por_dni(dni)
            if c:
                print(f"\n  {c}\n")
            else:
                print("\n  Cliente no encontrado.\n")

        elif op == "2":
            try:
                nombre    = input("  Nombre: ").strip()
                apellido  = input("  Apellido: ").strip()
                dni       = input("  DNI: ").strip()
                email     = input("  Email: ").strip()
                telefono  = input("  Telefono (opcional): ").strip()
                direccion = input("  Direccion (opcional): ").strip()
                c = tienda.registrar_cliente(nombre, apellido, dni, email, telefono, direccion)
                print(f"\n  Registrado: {c}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif op == "3":
            mostrar_lista(tienda.listar_clientes(), "No hay clientes registrados.")

        elif op == "0":
            break
        else:
            print("  Opcion invalida.")


# ------------------------------------------------------------------ #
# Punto de entrada
# ------------------------------------------------------------------ #

def main():
    tienda = Tienda("El Universo - Tienda de Comics y Coleccionables")
    tienda.cargar_clientes()
    cargar_datos(tienda)

    print("=" * 60)
    print(f"  {tienda.nombre}")
    print(f"  Sistema de gestion v1.0")
    print(f"  {len(tienda.listar_catalogo())} articulos | {len(tienda.listar_clientes())} clientes")
    print("=" * 60)

    while True:
        titulo("MENU PRINCIPAL")
        stats(tienda)
        linea()
        print("  1. Ventas")
        print("  2. Alquileres")
        print("  3. Consignaciones")
        print("  4. Catalogo")
        print("  5. Clientes")
        print("  0. Salir")
        linea()
        op = input("  Opcion: ").strip()

        if op == "1":
            menu_ventas(tienda)
        elif op == "2":
            menu_alquileres(tienda)
        elif op == "3":
            menu_consignaciones(tienda)
        elif op == "4":
            menu_catalogo(tienda)
        elif op == "5":
            menu_clientes(tienda)
        elif op == "0":
            print("\n  Hasta luego.\n")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    main()
