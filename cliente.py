class Cliente:
    """Representa a un cliente de la tienda."""

    def __init__(self, numero, nombre, apellido, dni, email, telefono="", direccion=""):
        self._numero = numero
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni
        self._email = email
        self._telefono = telefono
        self._direccion = direccion
        self._activo = True

    @property
    def numero(self):
        return self._numero

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    @property
    def dni(self):
        return self._dni

    @property
    def email(self):
        return self._email

    @property
    def telefono(self):
        return self._telefono

    @property
    def direccion(self):
        return self._direccion

    @property
    def activo(self):
        return self._activo

    def nombre_completo(self):
        return f"{self._nombre} {self._apellido}"

    def __str__(self):
        estado = "Activo" if self._activo else "Inactivo"
        partes = [
            f"Cliente #{self._numero}",
            self.nombre_completo(),
            f"DNI: {self._dni}",
            self._email,
        ]
        if self._telefono:
            partes.append(f"Tel: {self._telefono}")
        if self._direccion:
            partes.append(self._direccion)
        partes.append(estado)
        return " | ".join(partes)
