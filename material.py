from abc import ABC, abstractmethod

CONDICIONES = ("Nuevo", "Usado - Excelente", "Usado - Bueno", "Usado - Regular")


class Material(ABC):
    """Clase base abstracta para todos los artículos de la tienda."""

    def __init__(self, codigo, titulo, precio, condicion="Nuevo"):
        self._codigo = codigo
        self._titulo = titulo
        self._precio = precio
        self._condicion = condicion
        self._disponible = True
        self._vendido = False

    @property
    def codigo(self):
        return self._codigo

    @property
    def titulo(self):
        return self._titulo

    @property
    def precio(self):
        return self._precio

    @property
    def condicion(self):
        return self._condicion

    @property
    def disponible(self):
        return self._disponible and not self._vendido

    @property
    def vendido(self):
        return self._vendido

    @property
    def estado(self):
        if self._vendido:
            return "Vendido"
        if not self._disponible:
            return "Alquilado"
        return "Disponible"

    def prestar(self):
        """Marca el artículo como alquilado (temporalmente no disponible)."""
        if not self.disponible:
            raise ValueError(f"'{self._titulo}' no está disponible.")
        self._disponible = False

    def devolver(self):
        """Restaura la disponibilidad tras devolver un alquiler."""
        self._disponible = True

    def vender(self):
        """Marca el artículo como vendido definitivamente."""
        if not self.disponible:
            raise ValueError(f"'{self._titulo}' no está disponible para venta.")
        self._disponible = False
        self._vendido = True

    def campos_busqueda(self):
        """Campos sobre los que actúa la búsqueda por texto."""
        return [self._codigo, self._titulo]

    @abstractmethod
    def tipo(self):
        pass

    def __str__(self):
        return (
            f"[{self.tipo():5}] {self._codigo} | {self._titulo} | "
            f"${self._precio:,} | {self._condicion} | {self.estado}"
        )


class Comic(Material):
    """Comic occidental (Marvel, DC, Image, etc.)"""

    def __init__(self, codigo, titulo, precio, editorial, numero, personaje, condicion="Nuevo"):
        super().__init__(codigo, titulo, precio, condicion)
        self._editorial = editorial
        self._numero = numero       # número de edición
        self._personaje = personaje

    @property
    def editorial(self):
        return self._editorial

    @property
    def numero(self):
        return self._numero

    @property
    def personaje(self):
        return self._personaje

    def tipo(self):
        return "Comic"

    def campos_busqueda(self):
        return super().campos_busqueda() + [self._editorial, self._personaje]

    def __str__(self):
        return f"{super().__str__()} | {self._editorial} #{self._numero} | {self._personaje}"


class Manga(Material):
    """Manga japonés."""

    def __init__(self, codigo, titulo, precio, editorial, volumen, autor, condicion="Nuevo"):
        super().__init__(codigo, titulo, precio, condicion)
        self._editorial = editorial
        self._volumen = volumen
        self._autor = autor

    @property
    def editorial(self):
        return self._editorial

    @property
    def volumen(self):
        return self._volumen

    @property
    def autor(self):
        return self._autor

    def tipo(self):
        return "Manga"

    def campos_busqueda(self):
        return super().campos_busqueda() + [self._editorial, self._autor]

    def __str__(self):
        return f"{super().__str__()} | Vol. {self._volumen} | {self._autor} | {self._editorial}"


class Carta(Material):
    """Carta individual de juego de cartas coleccionables."""

    def __init__(self, codigo, titulo, precio, juego, rareza, condicion="Nuevo"):
        super().__init__(codigo, titulo, precio, condicion)
        self._juego = juego     # "Pokemon TCG", "Magic: The Gathering", "Yu-Gi-Oh!", etc.
        self._rareza = rareza   # "Comun", "Rara", "Ultra Rara", "Mitica", etc.

    @property
    def juego(self):
        return self._juego

    @property
    def rareza(self):
        return self._rareza

    def tipo(self):
        return "Carta"

    def campos_busqueda(self):
        return super().campos_busqueda() + [self._juego, self._rareza]

    def __str__(self):
        return f"{super().__str__()} | {self._juego} | {self._rareza}"


class Pack(Material):
    """Pack de cartas coleccionables cerrado."""

    def __init__(self, codigo, titulo, precio, juego, cantidad_cartas, edicion, condicion="Nuevo"):
        super().__init__(codigo, titulo, precio, condicion)
        self._juego = juego
        self._cantidad_cartas = cantidad_cartas
        self._edicion = edicion

    @property
    def juego(self):
        return self._juego

    @property
    def cantidad_cartas(self):
        return self._cantidad_cartas

    @property
    def edicion(self):
        return self._edicion

    def tipo(self):
        return "Pack"

    def campos_busqueda(self):
        return super().campos_busqueda() + [self._juego, self._edicion]

    def __str__(self):
        return (
            f"{super().__str__()} | {self._juego} | "
            f"{self._cantidad_cartas} cartas | Ed. {self._edicion}"
        )
