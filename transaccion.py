from datetime import date, timedelta

MULTA_ALQUILER_POR_DIA = 1000   # pesos adicionales por dia de atraso en devolucion


class Venta:
    """Registra la venta definitiva de un articulo a un cliente."""

    def __init__(self, id_venta, material, cliente, precio_final):
        self._id = id_venta
        self._material = material
        self._cliente = cliente
        self._precio_final = precio_final
        self._fecha = date.today()

    @property
    def id(self):
        return self._id

    @property
    def material(self):
        return self._material

    @property
    def cliente(self):
        return self._cliente

    @property
    def precio_final(self):
        return self._precio_final

    @property
    def fecha(self):
        return self._fecha

    def __str__(self):
        return (
            f"Venta #{self._id} | {self._material.titulo} -> {self._cliente.nombre_completo()} | "
            f"${self._precio_final:,} | {self._fecha}"
        )


class Alquiler:
    """Registra el alquiler temporal de un articulo a un cliente."""

    def __init__(self, id_alquiler, material, cliente, dias, precio_por_dia):
        self._id = id_alquiler
        self._material = material
        self._cliente = cliente
        self._dias = dias
        self._precio_por_dia = precio_por_dia
        self._fecha_inicio = date.today()
        self._fecha_vencimiento = date.today() + timedelta(days=dias)
        self._fecha_devolucion = None

    @property
    def id(self):
        return self._id

    @property
    def material(self):
        return self._material

    @property
    def cliente(self):
        return self._cliente

    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @property
    def fecha_vencimiento(self):
        return self._fecha_vencimiento

    @property
    def fecha_devolucion(self):
        return self._fecha_devolucion

    def esta_activo(self):
        return self._fecha_devolucion is None

    def esta_vencido(self):
        return self.esta_activo() and date.today() > self._fecha_vencimiento

    def calcular_costo_base(self):
        """Costo acordado: dias x precio por dia."""
        return self._dias * self._precio_por_dia

    def calcular_multa(self):
        """Multa adicional por cada dia de atraso en la devolucion."""
        if not self.esta_vencido():
            return 0
        dias_atraso = (date.today() - self._fecha_vencimiento).days
        return dias_atraso * MULTA_ALQUILER_POR_DIA

    def devolver(self):
        if not self.esta_activo():
            raise ValueError(f"El alquiler #{self._id} ya fue devuelto.")
        self._fecha_devolucion = date.today()
        self._material.devolver()

    def __str__(self):
        if self.esta_activo():
            if self.esta_vencido():
                estado = f"VENCIDO | Multa acumulada: ${self.calcular_multa():,}"
            else:
                estado = f"Activo | Vence: {self._fecha_vencimiento}"
        else:
            costo = self.calcular_costo_base()
            estado = f"Devuelto el {self._fecha_devolucion} | Total cobrado: ${costo:,}"
        return (
            f"Alquiler #{self._id} | {self._material.titulo} -> {self._cliente.nombre_completo()} | "
            f"{self._dias} dias a ${self._precio_por_dia}/dia | {estado}"
        )


class Consignacion:
    """
    Un cliente trae un articulo propio para que la tienda lo venda.
    Al concretarse la venta, el cliente recibe un porcentaje del precio.
    La tienda retiene el porcentaje restante como comision.
    """

    PORCENTAJE_DEFAULT = 70   # el cliente se lleva el 70% por defecto

    def __init__(self, id_consignacion, material, cliente, precio_venta, porcentaje_cliente=None):
        self._id = id_consignacion
        self._material = material
        self._cliente = cliente
        self._precio_venta = precio_venta
        self._porcentaje_cliente = (
            porcentaje_cliente if porcentaje_cliente is not None
            else self.PORCENTAJE_DEFAULT
        )
        self._fecha_ingreso = date.today()
        self._fecha_venta = None
        self._estado = "en_venta"   # "en_venta" | "vendido" | "retirado"

    @property
    def id(self):
        return self._id

    @property
    def material(self):
        return self._material

    @property
    def cliente(self):
        return self._cliente

    @property
    def precio_venta(self):
        return self._precio_venta

    @property
    def porcentaje_cliente(self):
        return self._porcentaje_cliente

    @property
    def fecha_ingreso(self):
        return self._fecha_ingreso

    @property
    def estado(self):
        return self._estado

    def esta_activa(self):
        return self._estado == "en_venta"

    def calcular_pago_cliente(self):
        """Monto que le corresponde al cliente cuando se vende."""
        return round(self._precio_venta * self._porcentaje_cliente / 100)

    def calcular_ganancia_tienda(self):
        """Comision que retiene la tienda."""
        return self._precio_venta - self.calcular_pago_cliente()

    def vender(self):
        """Registra la venta del articulo en consignacion."""
        if not self.esta_activa():
            raise ValueError(f"La consignacion #{self._id} no esta activa.")
        self._estado = "vendido"
        self._fecha_venta = date.today()
        self._material.vender()

    def retirar(self):
        """El cliente decide retirar su articulo sin venderlo."""
        if not self.esta_activa():
            raise ValueError(f"La consignacion #{self._id} no esta activa.")
        self._estado = "retirado"

    def __str__(self):
        pago = self.calcular_pago_cliente()
        ganancia = self.calcular_ganancia_tienda()
        if self._estado == "vendido":
            detalle = (
                f"Vendido el {self._fecha_venta} | "
                f"Pago al cliente: ${pago:,} | Ganancia tienda: ${ganancia:,}"
            )
        elif self._estado == "retirado":
            detalle = "Retirado por el cliente"
        else:
            detalle = (
                f"En venta | Precio: ${self._precio_venta:,} | "
                f"Cliente ({self._porcentaje_cliente}%): ${pago:,} | "
                f"Tienda: ${ganancia:,}"
            )
        return (
            f"Consignacion #{self._id} | {self._material.titulo} "
            f"(de {self._cliente.nombre_completo()}) | {detalle}"
        )
