import json
import os

from material import Comic, Manga, Carta, Pack
from cliente import Cliente
from transaccion import Venta, Alquiler, Consignacion

ARCHIVO_CLIENTES = "clientes.json"


class Tienda:
    """
    Clase principal del sistema. Gestiona el catalogo de articulos, los clientes
    y todas las operaciones: ventas, alquileres y consignaciones.
    Actua como fachada del dominio: el menu solo interactua con esta clase.
    """

    def __init__(self, nombre):
        self._nombre = nombre
        self._materiales = {}           # codigo -> Material
        self._clientes = {}             # numero -> Cliente
        self._ventas = []
        self._alquileres = []
        self._consignaciones = []
        self._contador_clientes = 1
        self._contador_ventas = 1
        self._contador_alquileres = 1
        self._contador_consignaciones = 1

    @property
    def nombre(self):
        return self._nombre

    # ------------------------------------------------------------------ #
    # Catalogo
    # ------------------------------------------------------------------ #

    def registrar_comic(self, codigo, titulo, precio, editorial, numero, personaje, condicion="Nuevo"):
        self._validar_codigo_unico(codigo)
        comic = Comic(codigo, titulo, precio, editorial, numero, personaje, condicion)
        self._materiales[codigo] = comic
        return comic

    def registrar_manga(self, codigo, titulo, precio, editorial, volumen, autor, condicion="Nuevo"):
        self._validar_codigo_unico(codigo)
        manga = Manga(codigo, titulo, precio, editorial, volumen, autor, condicion)
        self._materiales[codigo] = manga
        return manga

    def registrar_carta(self, codigo, titulo, precio, juego, rareza, condicion="Nuevo"):
        self._validar_codigo_unico(codigo)
        carta = Carta(codigo, titulo, precio, juego, rareza, condicion)
        self._materiales[codigo] = carta
        return carta

    def registrar_pack(self, codigo, titulo, precio, juego, cantidad_cartas, edicion, condicion="Nuevo"):
        self._validar_codigo_unico(codigo)
        pack = Pack(codigo, titulo, precio, juego, cantidad_cartas, edicion, condicion)
        self._materiales[codigo] = pack
        return pack

    def generar_codigo(self, prefijo):
        numero = 1
        while f"{prefijo}{numero:03d}" in self._materiales:
            numero += 1
        return f"{prefijo}{numero:03d}"

    def buscar_material(self, termino):
        termino = termino.lower()
        resultados = []
        for m in self._materiales.values():
            for campo in m.campos_busqueda():
                if termino in campo.lower():
                    resultados.append(m)
                    break
        return resultados

    def listar_disponibles(self):
        return [m for m in self._materiales.values() if m.disponible]

    def listar_catalogo(self):
        return list(self._materiales.values())

    def obtener_material(self, codigo):
        return self._materiales.get(codigo)

    # ------------------------------------------------------------------ #
    # Clientes
    # ------------------------------------------------------------------ #

    def cargar_clientes(self, ruta=ARCHIVO_CLIENTES):
        """Carga los clientes desde un archivo JSON. Si no existe, no hace nada."""
        if not os.path.exists(ruta):
            return
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
        for d in datos:
            cliente = Cliente(
                d["numero"], d["nombre"], d["apellido"],
                d["dni"], d["email"],
                d.get("telefono", ""), d.get("direccion", "")
            )
            self._clientes[d["numero"]] = cliente
        if self._clientes:
            self._contador_clientes = max(self._clientes.keys()) + 1

    def _guardar_clientes(self, ruta=ARCHIVO_CLIENTES):
        datos = []
        for c in self._clientes.values():
            datos.append({
                "numero":    c.numero,
                "nombre":    c.nombre,
                "apellido":  c.apellido,
                "dni":       c.dni,
                "email":     c.email,
                "telefono":  c.telefono,
                "direccion": c.direccion,
            })
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def registrar_cliente(self, nombre, apellido, dni, email, telefono="", direccion=""):
        if self.buscar_cliente_por_dni(dni):
            raise ValueError(f"Ya existe un cliente con DNI {dni}.")
        cliente = Cliente(self._contador_clientes, nombre, apellido, dni, email, telefono, direccion)
        self._clientes[self._contador_clientes] = cliente
        self._contador_clientes += 1
        self._guardar_clientes()
        return cliente

    def buscar_cliente_por_dni(self, dni):
        for c in self._clientes.values():
            if c.dni == dni:
                return c
        return None

    def obtener_cliente(self, numero):
        return self._clientes.get(numero)

    def listar_clientes(self):
        return list(self._clientes.values())

    # ------------------------------------------------------------------ #
    # Ventas
    # ------------------------------------------------------------------ #

    def registrar_venta(self, codigo_material, numero_cliente):
        """Vende un articulo del catalogo propio de la tienda a un cliente."""
        self._verificar_no_en_consignacion(codigo_material)
        material = self._get_material_disponible(codigo_material)
        cliente = self._get_cliente_activo(numero_cliente)

        venta = Venta(self._contador_ventas, material, cliente, material.precio)
        material.vender()
        self._ventas.append(venta)
        self._contador_ventas += 1
        return venta

    def listar_ventas(self):
        return list(self._ventas)

    # ------------------------------------------------------------------ #
    # Alquileres
    # ------------------------------------------------------------------ #

    def registrar_alquiler(self, codigo_material, numero_cliente, dias, precio_por_dia):
        """Alquila un articulo a un cliente por una cantidad de dias."""
        self._verificar_no_en_consignacion(codigo_material)
        material = self._get_material_disponible(codigo_material)
        cliente = self._get_cliente_activo(numero_cliente)

        alquiler = Alquiler(self._contador_alquileres, material, cliente, dias, precio_por_dia)
        material.prestar()
        self._alquileres.append(alquiler)
        self._contador_alquileres += 1
        return alquiler

    def devolver_alquiler(self, id_alquiler):
        for a in self._alquileres:
            if a.id == id_alquiler and a.esta_activo():
                a.devolver()
                return a
        raise ValueError(f"No se encontro un alquiler activo con ID {id_alquiler}.")

    def listar_alquileres_activos(self):
        return [a for a in self._alquileres if a.esta_activo()]

    def listar_alquileres_vencidos(self):
        return [a for a in self._alquileres if a.esta_vencido()]

    # ------------------------------------------------------------------ #
    # Consignaciones
    # ------------------------------------------------------------------ #

    def registrar_consignacion(self, codigo_material, numero_cliente, precio_venta, porcentaje_cliente=70):
        """
        Registra un articulo traido por un cliente para que la tienda lo venda.
        El articulo debe estar previamente registrado en el catalogo.
        """
        material = self._get_material_disponible(codigo_material)
        cliente = self._get_cliente_activo(numero_cliente)

        consignacion = Consignacion(
            self._contador_consignaciones, material, cliente,
            precio_venta, porcentaje_cliente
        )
        self._consignaciones.append(consignacion)
        self._contador_consignaciones += 1
        return consignacion

    def vender_consignacion(self, id_consignacion):
        """Registra que alguien compro el articulo en consignacion."""
        consignacion = self._get_consignacion_activa(id_consignacion)
        consignacion.vender()
        return consignacion

    def retirar_consignacion(self, id_consignacion):
        """El cliente decide retirar su articulo sin venderlo."""
        consignacion = self._get_consignacion_activa(id_consignacion)
        consignacion.retirar()
        del self._materiales[consignacion.material.codigo]
        return consignacion

    def listar_consignaciones_activas(self):
        return [c for c in self._consignaciones if c.esta_activa()]

    def listar_consignaciones_vendidas(self):
        return [c for c in self._consignaciones if c.estado == "vendido"]

    # ------------------------------------------------------------------ #
    # Helpers internos
    # ------------------------------------------------------------------ #

    def _validar_codigo_unico(self, codigo):
        if codigo in self._materiales:
            raise ValueError(f"Ya existe un articulo con codigo '{codigo}'.")

    def _get_material_disponible(self, codigo):
        material = self.obtener_material(codigo)
        if not material:
            raise ValueError(f"No existe un articulo con codigo '{codigo}'.")
        if not material.disponible:
            raise ValueError(f"'{material.titulo}' no esta disponible ({material.estado}).")
        return material

    def _get_cliente_activo(self, numero):
        cliente = self.obtener_cliente(numero)
        if not cliente:
            raise ValueError(f"No existe un cliente con numero {numero}.")
        if not cliente.activo:
            raise ValueError(f"El cliente {cliente.nombre_completo()} no esta activo.")
        return cliente

    def _get_consignacion_activa(self, id_consignacion):
        for c in self._consignaciones:
            if c.id == id_consignacion and c.esta_activa():
                return c
        raise ValueError(f"No se encontro una consignacion activa con ID {id_consignacion}.")

    def _verificar_no_en_consignacion(self, codigo):
        for c in self._consignaciones:
            if c.material.codigo == codigo and c.esta_activa():
                raise ValueError(
                    f"El articulo '{codigo}' esta en consignacion activa. "
                    "Use la opcion de Consignaciones para venderlo."
                )
