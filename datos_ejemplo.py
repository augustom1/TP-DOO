from tienda import Tienda


def cargar_articulos(tienda):
    # ---- Comics (13) -------------------------------------------------------
    tienda.registrar_comic("C001", "Amazing Spider-Man #1",   2500,  "Marvel",       1,   "Spider-Man")
    tienda.registrar_comic("C002", "Batman: Year One",        3500,  "DC Comics",    404, "Batman",          "Usado - Excelente")
    tienda.registrar_comic("C003", "Saga #1",                 1800,  "Image Comics", 1,   "Saga")
    tienda.registrar_comic("C004", "X-Men #1 (1963)",         95000, "Marvel",       1,   "X-Men",           "Usado - Bueno")
    tienda.registrar_comic("C005", "Watchmen #1",             8000,  "DC Comics",    1,   "Watchmen",        "Usado - Excelente")
    tienda.registrar_comic("C006", "The Dark Knight Returns", 6500,  "DC Comics",    1,   "Batman",          "Usado - Excelente")
    tienda.registrar_comic("C007", "Maus Vol. 1",             4200,  "Pantheon",     1,   "Maus")
    tienda.registrar_comic("C008", "Invincible #1",           2200,  "Image Comics", 1,   "Invincible")
    tienda.registrar_comic("C009", "Justice League #1",       3800,  "DC Comics",    1,   "Justice League")
    tienda.registrar_comic("C010", "Uncanny X-Men #1 (1981)", 72000, "Marvel",       1,   "X-Men",           "Usado - Bueno")
    tienda.registrar_comic("C011", "Spawn #1",                5500,  "Image Comics", 1,   "Spawn",           "Usado - Excelente")
    tienda.registrar_comic("C012", "Preacher #1",             9000,  "DC Comics",    1,   "Preacher",        "Usado - Excelente")
    tienda.registrar_comic("C013", "Y: The Last Man #1",      4500,  "DC Comics",    1,   "Y")

    # ---- Manga (11) --------------------------------------------------------
    tienda.registrar_manga("M001", "One Piece Vol. 1",           1200, "Shueisha",    1, "Eiichiro Oda")
    tienda.registrar_manga("M002", "Naruto Vol. 1",              1100, "Shueisha",    1, "Masashi Kishimoto")
    tienda.registrar_manga("M003", "Attack on Titan Vol. 1",     1400, "Kodansha",    1, "Hajime Isayama",    "Usado - Excelente")
    tienda.registrar_manga("M004", "Demon Slayer Vol. 1",        1300, "Shueisha",    1, "Koyoharu Gotouge")
    tienda.registrar_manga("M005", "Fullmetal Alchemist Vol. 1", 1250, "Square Enix", 1, "Hiromu Arakawa")
    tienda.registrar_manga("M006", "Dragon Ball Vol. 1",         1150, "Shueisha",    1, "Akira Toriyama",    "Usado - Bueno")
    tienda.registrar_manga("M007", "Berserk Vol. 1",             1800, "Hakusensha",  1, "Kentaro Miura",     "Usado - Excelente")
    tienda.registrar_manga("M008", "Death Note Vol. 1",          1350, "Shueisha",    1, "Tsugumi Ohba")
    tienda.registrar_manga("M009", "Hunter x Hunter Vol. 1",     1200, "Shueisha",    1, "Yoshihiro Togashi")
    tienda.registrar_manga("M010", "My Hero Academia Vol. 1",    1100, "Shueisha",    1, "Kohei Horikoshi")
    tienda.registrar_manga("M011", "Chainsaw Man Vol. 1",        1500, "Shueisha",    1, "Tatsuki Fujimoto")

    # ---- Cartas individuales (11) ------------------------------------------
    tienda.registrar_carta("CT001", "Pikachu V",                        5500,   "Pokemon TCG",          "Rara")
    tienda.registrar_carta("CT002", "Charizard VMAX",                   12000,  "Pokemon TCG",          "Rara",       "Usado - Excelente")
    tienda.registrar_carta("CT003", "Dark Magician (Blue-Eyes Art)",    3200,   "Yu-Gi-Oh!",            "Ultra Rara")
    tienda.registrar_carta("CT004", "Black Lotus",                      85000,  "Magic: The Gathering", "Mitica",     "Usado - Bueno")
    tienda.registrar_carta("CT005", "Mox Sapphire",                     45000,  "Magic: The Gathering", "Mitica",     "Usado - Bueno")
    tienda.registrar_carta("CT006", "Mewtwo EX",                        8500,   "Pokemon TCG",          "Ultra Rara")
    tienda.registrar_carta("CT007", "Blue-Eyes White Dragon (LOB)",     15000,  "Yu-Gi-Oh!",            "Ultra Rara", "Usado - Bueno")
    tienda.registrar_carta("CT008", "Ancestral Recall",                 120000, "Magic: The Gathering", "Mitica",     "Usado - Bueno")
    tienda.registrar_carta("CT009", "Exodia the Forbidden One (LOB)",   25000,  "Yu-Gi-Oh!",            "Ultra Rara", "Usado - Bueno")
    tienda.registrar_carta("CT010", "Umbreon EX (Evolutions)",          6800,   "Pokemon TCG",          "Ultra Rara")
    tienda.registrar_carta("CT011", "Time Walk",                        98000,  "Magic: The Gathering", "Mitica",     "Usado - Bueno")

    # ---- Packs (5) ---------------------------------------------------------
    tienda.registrar_pack("P001", "Scarlet & Violet Booster Pack",   3500, "Pokemon TCG",          10, "Scarlet & Violet")
    tienda.registrar_pack("P002", "Bloomburrow Draft Booster",       2800, "Magic: The Gathering", 15, "Bloomburrow")
    tienda.registrar_pack("P003", "Phantom Nightmare Booster",       2600, "Yu-Gi-Oh!",            9,  "Phantom Nightmare")
    tienda.registrar_pack("P004", "Temporal Forces Booster",         3800, "Pokemon TCG",          10, "Temporal Forces")
    tienda.registrar_pack("P005", "Modern Horizons 3 Draft Booster", 3200, "Magic: The Gathering", 15, "Modern Horizons 3")


def cargar_transacciones(tienda):
    tienda.registrar_venta("C002", 1)                    # Juan compra Batman: Year One
    tienda.registrar_alquiler("M001", 2, 7, 150)         # Maria alquila One Piece por 7 dias
    tienda.registrar_alquiler("C003", 4, 3, 200)         # Ana alquila Saga #1 por 3 dias
    tienda.registrar_consignacion("CT005", 3, 45000, 75) # Carlos trae Mox Sapphire (75% para el)
    tienda.registrar_consignacion("C006", 5, 7000, 70)   # Pedro trae Dark Knight Returns


def cargar_datos(tienda):
    cargar_articulos(tienda)
    cargar_transacciones(tienda)
