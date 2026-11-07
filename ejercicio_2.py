import json
import os


class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock no válido."""


class DispositivoEcologico:
    def __init__(self, nombre, precio, stock):
        if not nombre or not str(nombre).strip():
            raise ValueError("El nombre del dispositivo no puede estar vacío.")
        if precio <= 0:
            raise ValueError(f"El precio debe ser mayor a cero: {precio}.")

        self.nombre = str(nombre).strip()
        self.precio = precio
        self.stock = stock

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise StockInvalidoError(f"El stock debe ser un número entero, se recibió {valor!r}.")
        if valor < 0:
            raise StockInvalidoError(f"El stock no puede ser negativo: {valor}.")

        self.__stock = valor

    def ficha_tecnica(self):
        return (
            f"Producto: {self.nombre}\n"
            f"Precio: ${self.precio:,.2f}\n"
            f"Stock disponible: {self.stock} unidades"
        )

    def a_diccionario(self):
        return {
            "tipo": type(self).__name__,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcologico):
    def __init__(self, nombre, precio, stock, potencia_pico_w, eficiencia_porcentaje):
        super().__init__(nombre, precio, stock)

        if potencia_pico_w <= 0:
            raise ValueError(f"La potencia pico debe ser mayor a cero: {potencia_pico_w}.")
        if not 0 < eficiencia_porcentaje <= 100:
            raise ValueError(f"La eficiencia debe estar entre 0 y 100: {eficiencia_porcentaje}.")

        self.potencia_pico_w = potencia_pico_w
        self.eficiencia_porcentaje = eficiencia_porcentaje

    def ficha_tecnica(self):
        return (
            "=== PANEL SOLAR ===\n"
            f"Modelo: {self.nombre}\n"
            f"Precio: ${self.precio:,.2f}\n"
            f"Potencia pico: {self.potencia_pico_w} W\n"
            f"Eficiencia: {self.eficiencia_porcentaje}%\n"
            f"Stock disponible: {self.stock} unidades"
        )

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["potencia_pico_w"] = self.potencia_pico_w
        datos["eficiencia_porcentaje"] = self.eficiencia_porcentaje
        return datos


class GestorInventario:
    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        for dispositivo in lista_dispositivos:
            if not isinstance(dispositivo, DispositivoEcologico):
                raise TypeError(f"Elemento no válido para el catálogo: {dispositivo!r}")

        catalogo = [dispositivo.a_diccionario() for dispositivo in lista_dispositivos]

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(catalogo, archivo, ensure_ascii=False, indent=4)

        return len(catalogo)


RUTA_CATALOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalogo_ecotech.json")


if __name__ == "__main__":
    dispositivos = []

    compostera = DispositivoEcologico("Compostera doméstica", 45000, 12)
    dispositivos.append(compostera)

    panel = PanelSolar("Panel monocristalino 450W", 180000, 8, 450, 21.5)
    dispositivos.append(panel)

    print("--- Captura de stock inválido ---")
    try:
        panel.stock = -3
    except StockInvalidoError as error:
        print(f"Error controlado: {error}")
    print(f"Stock del panel tras el intento: {panel.stock}")

    print("\n--- Alta de producto con stock inválido ---")
    try:
        panel_defectuoso = PanelSolar("Panel defectuoso", 150000, -1, 400, 20)
        dispositivos.append(panel_defectuoso)
    except StockInvalidoError as error:
        print(f"Producto descartado: {error}")

    print("\n--- Fichas técnicas ---")
    for dispositivo in dispositivos:
        print(dispositivo.ficha_tecnica())
        print()

    gestor = GestorInventario()
    cantidad = gestor.guardar_catalogo_json(dispositivos, RUTA_CATALOGO)
    print(f"Se exportaron {cantidad} productos válidos a {RUTA_CATALOGO}")
