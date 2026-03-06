from game_core.Zone import Zone

class Tableboard():
    def __init__(self):
        print(f"[Tableboard] Create Tableboard")
        
        # TODO: definir mapa en un JSON y cargarlo aqui, para no hardcodearlo, poner cuales son adyacentes y tal
        self.zones = {
            "Campamento": Zone("Campamento"),
            "Explanada": Zone("Explanada"),
            "Muralla Este": Zone("Muralla Este"),
            "Zona Este": Zone("Zona Este"),
            "Lengua de tierra": Zone("Lengua de tierra"),
            "Laguna": Zone("Laguna"),
            "Muralla Norte": Zone("Muralla Norte"),
            "Zona Norte": Zone("Zona Norte"),
            "Bahía": Zone("Bahía"),
            "Playa/Puerto": Zone("Playa/Puerto"),
            "Muralla Sur": Zone("Muralla Sur"),
            "Zona Sur": Zone("Zona Sur"),
            "Centro Ciudad": Zone("Centro Ciudad"),
            "Foro": Zone("Foro"),
            "Ciudadela": Zone("Ciudadela")
        }

        self.print_zones()

    def print_zones(self):
        for zone in self.zones:
            print(zone)