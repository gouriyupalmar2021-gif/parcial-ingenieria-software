"""Suite de pruebas - Parcial 3. Estudiante 0182310007.
Valores esperados calculados a mano segun la especificacion personal:
PMAX=45, L1=3 (incluido, D=0), L2=10, RR=10%, RN=45%, V=10%, S=$2.000 (antes
de descuentos, E=0), cliente y cupon se aplican ambos (B=1), cupon inexistente
= error (F=7).
"""
import inspect
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from envios import calc  # noqa: E402

ERR = "ERR"

# (id, entradas (p, zona, cliente, dia, cupon), esperado)
CAJA_NEGRA = [
    ("CN-01", (0, "urbana", "normal", 1, None), ERR),
    ("CN-02", (0.1, "urbana", "normal", 1, None), 6000),
    ("CN-03", (3, "urbana", "normal", 1, None), 6000),
    ("CN-04", (3.01, "urbana", "normal", 1, None), 9000),
    ("CN-05", (10, "urbana", "normal", 1, None), 9000),
    ("CN-06", (10.5, "urbana", "normal", 1, None), 9400),
    ("CN-07", (45, "urbana", "normal", 1, None), 37000),
    ("CN-08", (45.01, "urbana", "normal", 1, None), ERR),
    ("CN-09", (-1, "urbana", "normal", 1, None), ERR),
    ("CN-10", (5, "maritima", "normal", 1, None), ERR),
    ("CN-11", (5, "urbana", "normal", 0, None), ERR),
    ("CN-12", (5, "urbana", "normal", 8, None), ERR),
    ("CN-13", (3, "rural", "normal", 1, None), 6600),
    ("CN-14", (3, "nacional", "normal", 1, None), 8700),
    ("CN-15", (5, "urbana", "normal", 6, None), 11000),
    ("CN-16", (5, "urbana", "normal", 7, None), 11000),
    ("CN-17", (5, "urbana", "frecuente", 1, None), 8600),
    ("CN-18", (5, "urbana", "vip", 1, None), 8100),
    ("CN-19", (5, "urbana", "normal", 1, "ENVIO10"), 8100),
    ("CN-20", (5, "urbana", "vip", 1, "ENVIO10"), 7300),
    ("CN-21", (5, "urbana", "frecuente", 1, "ENVIO10"), 7700),
    ("CN-22", (5, "urbana", "normal", 1, "PROMO"), ERR),
    ("CN-23", (5, "rural", "vip", 6, "ENVIO10"), 9600),
    ("CN-24", (3, "urbana", "vip", 1, "ENVIO10"), 5000),
    ("CN-25", (20, "nacional", "frecuente", 7, "ENVIO10"), 22800),
    ("CN-26", (5, "urbana", "vip", 7, None), 9900),
    ("CN-27", (45, "nacional", "vip", 7, "ENVIO10"), 45100),
    ("CN-28", (5, "rural", "frecuente", 1, None), 9400),
    ("CN-29", (5, "urbana", "normal", 6, "ENVIO10"), 9900),
    ("CN-30", (10, "urbana", "frecuente", 6, None), 10500),
]

# Caminos independientes del grafo de flujo (V(G) = 15)
CAJA_BLANCA = [
    ("WB-00", (20, "urbana", "normal", 1, None), 17000),
    ("WB-01", (0, "urbana", "normal", 1, None), ERR),
    ("WB-02", (51, "urbana", "normal", 1, None), ERR),
    ("WB-03", (3, "urbana", "normal", 1, None), 6000),
    ("WB-04", (5, "urbana", "normal", 1, None), 9000),
    ("WB-05", (20, "rural", "normal", 1, None), 18700),
    ("WB-06", (20, "nacional", "normal", 1, None), 24700),
    ("WB-07", (20, "maritima", "normal", 1, None), ERR),
    ("WB-08", (20, "urbana", "normal", 7, None), 19000),
    ("WB-09", (20, "urbana", "frecuente", 1, None), 16200),
    ("WB-10", (20, "urbana", "vip", 1, None), 15300),
    ("WB-11", (20, "urbana", "normal", 1, "XYZ"), ERR),
    ("WB-12", (20, "urbana", "normal", 1, "ENVIO10"), 15300),
    ("WB-13", (3, "urbana", "vip", 1, "ENVIO10"), 5000),
]


def _verificar(entradas, esperado):
    if esperado == ERR:
        with pytest.raises(ValueError):
            calc(*entradas)
    else:
        assert calc(*entradas) == esperado


@pytest.mark.parametrize("cid,entradas,esperado", CAJA_NEGRA,
                         ids=[c[0] for c in CAJA_NEGRA])
def test_caja_negra(cid, entradas, esperado):
    _verificar(entradas, esperado)


@pytest.mark.parametrize("cid,entradas,esperado", CAJA_BLANCA,
                         ids=[c[0] for c in CAJA_BLANCA])
def test_caja_blanca(cid, entradas, esperado):
    _verificar(entradas, esperado)


TIENE_FLAG = "flag" in inspect.signature(calc).parameters


@pytest.mark.skipif(not TIENE_FLAG, reason="flag eliminado en v2.0.0")
def test_wb14_flag_imprime_legacy(capsys):
    assert calc(20, "urbana", "normal", 1, None, True) == 17000
    assert "costo:" in capsys.readouterr().out


@pytest.mark.skipif(TIENE_FLAG, reason="solo aplica desde v2.0.0")
def test_wb14_sin_flag_no_imprime(capsys):
    assert calc(20, "urbana", "normal", 1, None) == 17000
    assert capsys.readouterr().out == ""
    with pytest.raises(TypeError):
        calc(20, "urbana", "normal", 1, None, True)


def test_cliente_desconocido_es_error():
    with pytest.raises(ValueError):
        calc(5, "urbana", "platino", 1, None)
