# Guion de Git (ejecútalo TÚ, repartido a lo largo del día)

Los commits deben tener la hora real en que los haces. No cambies fechas.
Cada bloque va después de que realmente hayas hecho ese trabajo.

## 1. Código heredado (mañana)
```bash
git init -b main
cp heredado/envios_v1_0_0.py envios.py        # CONFIG ya lleno con tus valores
printf '__pycache__/\n.pytest_cache/\n.coverage\nhtmlcov/\n' > .gitignore
git add . && git commit -m "chore: importar código heredado EnvíaYa v1.0.0 con CONFIG personalizado"
git tag -a v1.0.0 -m "Código heredado"
```

## 2. Suite de pruebas (después de diseñar los casos)
```bash
git switch -c test/suite
# crea tests/test_envios.py (sin la última prueba test_cliente_desconocido_es_error) y requirements.txt
git add . && git commit -m "test: suite de caja negra y caja blanca"
python -m pytest -q          # captura: 18 fallan
git switch main && git merge --no-ff test/suite -m "Merge test/suite"
```

## 3. Una rama por defecto (aplica el cambio, corre pytest, commit, merge)
| Rama | Cambio en envios.py (legado) |
|---|---|
| fix/DEF-01 | CONFIG += `"PMAX": 45`; `p > 50` -> `p > CONFIG["PMAX"]` |
| fix/DEF-02 | tras la rama `nacional` agregar `else: raise ValueError("zona invalida")` |
| fix/DEF-03 | antes del tramo: `if d < 1 or d > 7: raise ValueError("dia invalido")` |
| fix/DEF-04 | `if d > 6:` -> `if d >= 6:` |
| fix/DEF-05 | tras `if cup == "ENVIO10": ...` agregar `else: raise ValueError("cupon inexistente")` |
| fix/DEF-06 | `return int(t / 100) * 100` -> `return int(round(t, 2) / 100 + 0.5) * 100` |
```bash
git switch -c fix/DEF-01      # (cambia DEF-01 por cada defecto)
# edita, prueba
git add -A && git commit -m "fix(DEF-01): PMAX de 50 a 45 kg (R1)"
git switch main && git merge --no-ff fix/DEF-01 -m "Merge fix/DEF-01"
```
Fallos esperados tras cada merge: 17, 15, 13, 10, 8 y 0.

## 4. Refactor
```bash
git switch -c refactor/estrategia
# 1) envios.py con funciones extraídas, constantes y sin flag (+ prueba de cliente desconocido)
git add -A && git commit -m "refactor: extraer funciones, constantes con nombre y eliminar argumento flag"
# 2) envios.py con patrón Estrategia (versión final de la carpeta)
git add -A && git commit -m "refactor: patrón Estrategia para zonas y descuentos"
git switch main && git merge --no-ff refactor/estrategia -m "Merge refactor/estrategia"
# CHANGELOG.md de la versión 2.0.0
git add -A && git commit -m "docs: CHANGELOG y notas de la versión 2.0.0"
git tag -a v2.0.0 -m "Refactor + corrección de defectos (breaking: sin flag)"
```

## 5. Solicitud de cambio (CR-01, cliente empresarial)
```bash
git switch -c feature/cliente-empresarial
# primero SOLO tests/test_cambio_empresarial.py
python -m pytest -q          # captura: 9 fallan (rojo)
git add -A && git commit -m "test(CR-01): casos del cliente empresarial (rojo)"
# luego implementa en envios.py
python -m pytest -q          # 56 pasan
git add -A && git commit -m "feat(CR-01): cliente empresarial 12 % y sin recargo de zona si peso > L2"
# actualiza CHANGELOG.md (2.1.0)
git add -A && git commit -m "docs: CHANGELOG 2.1.0"
git switch main && git merge --no-ff feature/cliente-empresarial -m "Merge feature/cliente-empresarial"
git tag -a v2.1.0 -m "Cliente empresarial"
git log --oneline --graph --all     # pega esta salida en el informe
```

## Capturas que debes tomar
```bash
python -m pytest -v                                       # fallando (heredado) y pasando
python -m pytest --cov=envios --cov-branch --cov-report=term-missing
```
