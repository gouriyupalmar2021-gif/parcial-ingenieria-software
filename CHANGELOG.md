# Changelog
Todos los cambios notables de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el
proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [2.1.0] - 2026-11-11
### Added
- Cliente `empresarial` con 12 % de descuento.
- El cliente empresarial no paga recargo de zona si el peso es mayor que 10 kg.

## [2.0.0] - 2026-11-11
### Changed
- **BREAKING:** se elimina el parámetro `flag` de `calc`; la función ya no imprime.
- Función principal renombrada a `calcular_costo` (`calc` queda como alias).
- Cliente desconocido ahora lanza `ValueError` (antes se trataba como normal).
- Refactorización: funciones extraídas, constantes con nombre y patrón Estrategia
  para zonas y descuentos.
### Fixed
- DEF-01: el peso máximo es 45 kg, no 50 (R1).
- DEF-02: una zona inexistente lanza error (R2).
- DEF-03: un día fuera de 1..7 lanza error (R2).
- DEF-04: el sábado también paga el recargo de fin de semana (R5).
- DEF-05: un cupón inexistente lanza error (R7).
- DEF-06: el costo se redondea al $100 más cercano, con $50 hacia arriba (R8).
### Added
- Suite de pruebas pytest (caja negra y caja blanca).

## [1.0.0] - 2026-11-11
### Added
- Versión heredada de `calc` con configuración personalizada.

[Unreleased]: https://github.com/USUARIO/envios/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/USUARIO/envios/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/USUARIO/envios/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/USUARIO/envios/releases/tag/v1.0.0
