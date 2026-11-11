"""CR-01: cliente empresarial (12 %). Si peso > L2 (10 kg), no se cobra el
recargo de zona (supuesto: aplica solo al cliente empresarial)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from envios import calc  # noqa: E402

CASOS = [
    ("CR-01", (5, "rural", "empresarial", 1, None), 8700),
    ("CR-02", (10, "rural", "empresarial", 1, None), 8700),
    ("CR-03", (10.5, "nacional", "empresarial", 1, None), 8300),
    ("CR-04", (20, "rural", "empresarial", 1, None), 15000),
    ("CR-05", (20, "nacional", "empresarial", 1, None), 15000),
    ("CR-06", (20, "urbana", "empresarial", 1, None), 15000),
    ("CR-07", (20, "rural", "empresarial", 7, "ENVIO10"), 15000),
    ("CR-08", (20, "rural", "frecuente", 1, None), 17800),
    ("CR-09", (3, "urbana", "empresarial", 1, "ENVIO10"), 5000),
    ("CR-10", (20, "rural", "empresarial", 1, "ENVIO10"), 13500),
]


@pytest.mark.parametrize("cid,entradas,esperado", CASOS, ids=[c[0] for c in CASOS])
def test_cliente_empresarial(cid, entradas, esperado):
    assert calc(*entradas) == esperado
