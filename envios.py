"""Calculo del costo de envios de EnvíaYa (v2.1.0)."""
from abc import ABC, abstractmethod
from fractions import Fraction
from math import floor

# --- Constantes de negocio (parametros del estudiante 0182310007) ---
PESO_MAXIMO = 45
LIMITE_TRAMO_1 = 3          # incluido (D par)
LIMITE_TRAMO_2 = 10
TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
TARIFA_KG_EXTRA = 800
RECARGO_FINDE = 2000        # se suma antes de descuentos (E par)
COSTO_MINIMO = 5000
MULTIPLO_REDONDEO = 100
DIAS_FINDE = (6, 7)
CUPON_ENVIO10 = "ENVIO10"


def _pct(valor):
    return Fraction(valor, 100)


# --- Patron Estrategia: zonas ---
class Zona(ABC):
    @abstractmethod
    def aplicar(self, costo):
        """Devuelve el costo con el recargo de la zona."""


class ZonaUrbana(Zona):
    def aplicar(self, costo):
        return costo


class ZonaRural(Zona):
    RECARGO = _pct(10)

    def aplicar(self, costo):
        return costo * (1 + self.RECARGO)


class ZonaNacional(Zona):
    RECARGO = _pct(45)

    def aplicar(self, costo):
        return costo * (1 + self.RECARGO)


ZONAS = {"urbana": ZonaUrbana(), "rural": ZonaRural(), "nacional": ZonaNacional()}


# --- Patron Estrategia: descuentos ---
class Descuento(ABC):
    @abstractmethod
    def aplicar(self, costo):
        """Devuelve el costo con el descuento."""


class SinDescuento(Descuento):
    def aplicar(self, costo):
        return costo


class DescuentoPorcentual(Descuento):
    def __init__(self, porcentaje):
        self._factor = 1 - _pct(porcentaje)

    def aplicar(self, costo):
        return costo * self._factor


DESCUENTOS_CLIENTE = {
    "normal": SinDescuento(),
    "frecuente": DescuentoPorcentual(5),
    "vip": DescuentoPorcentual(10),
    "empresarial": DescuentoPorcentual(12),
}
DESCUENTOS_CUPON = {None: SinDescuento(), CUPON_ENVIO10: DescuentoPorcentual(10)}


# --- Funciones extraidas ---
def _validar(peso, zona, cliente, dia, cupon):
    if not 0 < peso <= PESO_MAXIMO:
        raise ValueError("peso inválido")
    if cliente not in DESCUENTOS_CLIENTE:
        raise ValueError("cliente inválido")
    if zona not in ZONAS:
        raise ValueError("zona inválida")
    if dia not in range(1, 8):
        raise ValueError("día inválido")
    if cupon not in DESCUENTOS_CUPON:
        raise ValueError("cupón inexistente")


def _tarifa_base(peso):
    peso = Fraction(str(peso))
    if peso <= LIMITE_TRAMO_1:
        return Fraction(TARIFA_TRAMO_1)
    if peso <= LIMITE_TRAMO_2:
        return Fraction(TARIFA_TRAMO_2)
    return TARIFA_TRAMO_2 + (peso - LIMITE_TRAMO_2) * TARIFA_KG_EXTRA


def _cobra_recargo_zona(peso, cliente):
    """El cliente empresarial no paga recargo de zona si peso > L2."""
    return not (cliente == "empresarial" and peso > LIMITE_TRAMO_2)


def _recargo_finde(costo, dia):
    return costo + RECARGO_FINDE if dia in DIAS_FINDE else costo


def _redondear(costo):
    """Al multiplo de $100 mas cercano; $50 hacia arriba."""
    return int(floor(costo / MULTIPLO_REDONDEO + Fraction(1, 2)) * MULTIPLO_REDONDEO)


def calcular_costo(peso, zona, cliente, dia, cupon=None):
    _validar(peso, zona, cliente, dia, cupon)
    costo = _tarifa_base(peso)
    if _cobra_recargo_zona(peso, cliente):
        costo = ZONAS[zona].aplicar(costo)
    costo = _recargo_finde(costo, dia)
    costo = DESCUENTOS_CLIENTE[cliente].aplicar(costo)
    costo = DESCUENTOS_CUPON[cupon].aplicar(costo)
    return _redondear(max(costo, Fraction(COSTO_MINIMO)))


# Alias de compatibilidad con el nombre heredado
calc = calcular_costo
