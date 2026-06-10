# El Universo — Sistema de gestión de tienda de cómics

Sistema por consola para gestionar una tienda de cómics y coleccionables. Desarrollado en Python 3, sin librerías externas.

Soporta tres tipos de operaciones:
- **Ventas**: registro de ventas del stock propio de la tienda
- **Alquileres**: préstamo temporal con cálculo de multa por atraso
- **Consignaciones**: un cliente trae su propio artículo para que la tienda lo venda; al concretarse, cobra su porcentaje acordado

Los clientes se guardan en `clientes.json` y persisten entre sesiones.

---

## Cómo ejecutar

```bash
python main.py
```

Requiere Python 3.10 o superior. Sin dependencias externas.

Al arrancar, el sistema carga 40 artículos de ejemplo (13 cómics, 11 mangas, 11 cartas y 5 packs) y lee los clientes desde `clientes.json`.

---

## Estructura del proyecto

```
main.py          — menú por consola
tienda.py        — fachada del sistema: toda la lógica de negocio pasa por acá
material.py      — jerarquía de artículos: Material (abstracta), Comic, Manga, Carta, Pack
cliente.py       — clase Cliente
transaccion.py   — Venta, Alquiler y Consignacion
datos_ejemplo.py — artículos y transacciones de demo (se carga al iniciar)
clientes.json    — base de datos de clientes (se actualiza automáticamente)
```

---

## Estado inicial al arrancar

El sistema arranca con 5 transacciones de ejemplo ya cargadas:

| # | Tipo | Artículo | Cliente |
|---|------|----------|---------|
| Venta #1 | Venta | Batman: Year One | Lionel Messi |
| Alquiler #1 | Alquiler (7 días) | One Piece Vol. 1 | Angel Di Maria |
| Alquiler #2 | Alquiler (3 días) | Saga #1 | Javier Mascherano |
| Consignación #1 | Consignación | Mox Sapphire — $45.000 (75% cliente → $33.750) | Lautaro Martinez |
| Consignación #2 | Consignación | The Dark Knight Returns — $7.000 (70% cliente → $4.900) | Emiliano Martinez |

---

## Flujo de prueba por operación

### Consignación completa
1. **Consignaciones → 3** (ver activas): vas a ver los IDs disponibles
2. **Consignaciones → 2** (registrar venta): ingresás el ID, el sistema muestra cuánto le corresponde al cliente
3. **Consignaciones → 4** (ver vendidas): confirmás que quedó registrada

Para devolver un artículo sin vender: **Consignaciones → 5** (muestra la lista y pedí el ID).

### Alquiler y devolución
1. **Alquileres → 1**: ingresás código del artículo, DNI del cliente, días y precio/día
2. **Alquileres → 2**: muestra los alquileres activos, elegís el ID para registrar la devolución
3. Si ya venció la fecha, **Alquileres → 4** muestra los vencidos con la multa acumulada

### Venta directa
**Ventas → 1**: pedí código del artículo y DNI del cliente. Si el cliente no está registrado, lo podés agregar en el momento.

---

## Diagrama de clases

```mermaid
classDiagram
    class Material {
        <<abstract>>
        -_codigo : str
        -_titulo : str
        -_precio : int
        -_condicion : str
        -_disponible : bool
        -_vendido : bool
        +disponible : bool
        +vendido : bool
        +estado : str
        +prestar() void
        +devolver() void
        +vender() void
        +campos_busqueda() list
        +tipo()* str
    }

    class Comic {
        -_editorial : str
        -_numero : int
        -_personaje : str
        +tipo() str
    }

    class Manga {
        -_editorial : str
        -_volumen : int
        -_autor : str
        +tipo() str
    }

    class Carta {
        -_juego : str
        -_rareza : str
        +tipo() str
    }

    class Pack {
        -_juego : str
        -_cantidad_cartas : int
        -_edicion : str
        +tipo() str
    }

    class Cliente {
        -_numero : int
        -_nombre : str
        -_apellido : str
        -_dni : str
        -_email : str
        -_activo : bool
        +nombre_completo() str
    }

    class Venta {
        -_id : int
        -_material : Material
        -_cliente : Cliente
        -_precio_final : int
        -_fecha : date
    }

    class Alquiler {
        -_id : int
        -_material : Material
        -_cliente : Cliente
        -_dias : int
        -_precio_por_dia : int
        -_fecha_inicio : date
        -_fecha_vencimiento : date
        -_fecha_devolucion : date
        +esta_activo() bool
        +esta_vencido() bool
        +calcular_costo_base() int
        +calcular_multa() int
        +devolver() void
    }

    class Consignacion {
        -_id : int
        -_material : Material
        -_cliente : Cliente
        -_precio_venta : int
        -_porcentaje_cliente : int
        -_estado : str
        +esta_activa() bool
        +calcular_pago_cliente() int
        +calcular_ganancia_tienda() int
        +vender() void
        +retirar() void
    }

    class Tienda {
        -_nombre : str
        -_materiales : dict
        -_clientes : dict
        -_ventas : list
        -_alquileres : list
        -_consignaciones : list
        +cargar_clientes() void
        +generar_codigo() str
        +registrar_comic() Comic
        +registrar_manga() Manga
        +registrar_carta() Carta
        +registrar_pack() Pack
        +buscar_material() list
        +listar_disponibles() list
        +registrar_cliente() Cliente
        +buscar_cliente_por_dni() Cliente
        +registrar_venta() Venta
        +registrar_alquiler() Alquiler
        +devolver_alquiler() Alquiler
        +registrar_consignacion() Consignacion
        +vender_consignacion() Consignacion
        +retirar_consignacion() Consignacion
    }

    Material <|-- Comic : herencia
    Material <|-- Manga : herencia
    Material <|-- Carta : herencia
    Material <|-- Pack : herencia
    Tienda "1" *-- "0..*" Material : composicion
    Tienda "1" *-- "0..*" Cliente : composicion
    Tienda "1" *-- "0..*" Venta : composicion
    Tienda "1" *-- "0..*" Alquiler : composicion
    Tienda "1" *-- "0..*" Consignacion : composicion
    Venta "1" --> "1" Material : asociacion
    Venta "1" --> "1" Cliente : asociacion
    Alquiler "1" --> "1" Material : asociacion
    Alquiler "1" --> "1" Cliente : asociacion
    Consignacion "1" --> "1" Material : asociacion
    Consignacion "1" --> "1" Cliente : asociacion
```
