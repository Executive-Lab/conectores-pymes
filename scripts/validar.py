#!/usr/bin/env python3
"""Valida los datos del catálogo contra datos/esquema.json.

Comprueba cada datos/plataformas/<id>.json (campos obligatorios, tipos, enums de
dificultad, demo_resumen y veredicto, fechas ISO, fuentes) y cada
datos/categorias/<id>.json. Devuelve 0 si todo está bien y 1 si hay errores.

Uso:
    python3 scripts/validar.py
    python3 scripts/validar.py --datos otra/carpeta/datos

Solo usa la librería estándar de Python 3.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parent.parent
DATOS_POR_DEFECTO = RAIZ / "datos"

RE_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")

TIPOS_JSON = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "number": (int, float),
    "integer": int,
}


# --------------------------------------------------------------------------
# Mini validador de JSON Schema (subconjunto de draft 2020-12 que usa esquema.json)
# --------------------------------------------------------------------------

def _tipo_ok(valor: Any, tipo: str) -> bool:
    if tipo in ("number", "integer") and isinstance(valor, bool):
        return False
    return isinstance(valor, TIPOS_JSON[tipo])


def validar_esquema(valor: Any, esquema: dict, ruta: str) -> list[str]:
    """Devuelve una lista de errores legibles. Soporta: type, enum, pattern,
    minLength, format=date, required, properties, additionalProperties,
    minProperties, items, minItems, oneOf, anyOf."""
    errores: list[str] = []

    if "oneOf" in esquema:
        validas = [s for s in esquema["oneOf"] if not validar_esquema(valor, s, ruta)]
        if len(validas) != 1:
            tipos = " o ".join(s.get("type", "?") for s in esquema["oneOf"])
            errores.append(f"{ruta}: debe ser {tipos}")
        return errores

    if "anyOf" in esquema:
        if not any(not validar_esquema(valor, s, ruta) for s in esquema["anyOf"]):
            opciones = []
            for s in esquema["anyOf"]:
                if "enum" in s:
                    opciones.extend(repr(e) for e in s["enum"])
                if "pattern" in s:
                    opciones.append(f"patrón {s['pattern']}")
            errores.append(f"{ruta}: {valor!r} no es válido (se admite {', '.join(opciones)})")
        return errores

    tipo = esquema.get("type")
    if tipo and not _tipo_ok(valor, tipo):
        errores.append(f"{ruta}: se esperaba {tipo} y hay {type(valor).__name__}")
        return errores

    if "enum" in esquema and valor not in esquema["enum"]:
        errores.append(f"{ruta}: {valor!r} no está entre {esquema['enum']}")

    if isinstance(valor, str):
        if "minLength" in esquema and len(valor.strip()) < esquema["minLength"]:
            errores.append(f"{ruta}: no puede estar vacío")
        if "pattern" in esquema and not re.search(esquema["pattern"], valor):
            errores.append(f"{ruta}: {valor!r} no cumple el patrón {esquema['pattern']}")
        if esquema.get("format") == "date":
            errores.extend(validar_fecha(valor, ruta))

    if isinstance(valor, dict):
        for campo in esquema.get("required", []):
            if campo not in valor:
                errores.append(f"{ruta}: falta el campo obligatorio '{campo}'")
        props = esquema.get("properties", {})
        extra = esquema.get("additionalProperties", True)
        for campo, sub in valor.items():
            ruta_campo = f"{ruta}.{campo}" if ruta else campo
            if campo in props:
                errores.extend(validar_esquema(sub, props[campo], ruta_campo))
            elif extra is False:
                errores.append(f"{ruta_campo}: campo no previsto en el esquema")
            elif isinstance(extra, dict):
                errores.extend(validar_esquema(sub, extra, ruta_campo))
        if "minProperties" in esquema and len(valor) < esquema["minProperties"]:
            errores.append(f"{ruta}: el objeto está vacío")

    if isinstance(valor, list):
        if "minItems" in esquema and len(valor) < esquema["minItems"]:
            errores.append(f"{ruta}: necesita al menos {esquema['minItems']} elemento(s)")
        if "items" in esquema:
            for i, item in enumerate(valor):
                errores.extend(validar_esquema(item, esquema["items"], f"{ruta}[{i}]"))

    return errores


def validar_fecha(valor: str, ruta: str) -> list[str]:
    if not RE_FECHA.match(valor):
        return [f"{ruta}: {valor!r} no es una fecha ISO AAAA-MM-DD"]
    try:
        fecha = dt.date.fromisoformat(valor)
    except ValueError:
        return [f"{ruta}: {valor!r} no es una fecha real"]
    manana = dt.date.today() + dt.timedelta(days=1)
    if fecha > manana:
        return [f"{ruta}: {valor} está en el futuro"]
    return []


# --------------------------------------------------------------------------
# Validación del catálogo
# --------------------------------------------------------------------------

ESQUEMA_CATEGORIA = {
    "type": "object",
    "required": ["id", "nombre", "hallazgos", "verificado_el"],
    "additionalProperties": False,
    "properties": {
        "id": {"type": "string", "pattern": RE_ID.pattern},
        "nombre": {"type": "string", "minLength": 1},
        "hallazgos": {"type": "array", "items": {"type": "string", "minLength": 1}},
        "normativa": {"type": "string", "minLength": 1},
        "asistentes_ia": {"type": "array", "items": {"type": "string", "minLength": 1}},
        "verificado_el": {"type": "string", "format": "date"},
    },
}


def _leer_json(ruta: Path, errores: list[str]) -> Any:
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errores.append(f"{ruta.parent.name}/{ruta.name}: JSON inválido (línea {e.lineno}, columna {e.colno}): {e.msg}")
    except OSError as e:
        errores.append(f"{ruta.parent.name}/{ruta.name}: no se puede leer: {e}")
    return None


def validar(datos: Path = DATOS_POR_DEFECTO) -> tuple[list[str], list[str], list[dict], list[dict]]:
    """Valida la carpeta de datos. Devuelve (errores, avisos, plataformas, categorias)."""
    errores: list[str] = []
    avisos: list[str] = []
    plataformas: list[dict] = []
    categorias: list[dict] = []

    ruta_esquema = datos / "esquema.json"
    esquema = _leer_json(ruta_esquema, errores)
    if not isinstance(esquema, dict):
        errores.append("esquema.json: no existe o no es un objeto")
        return errores, avisos, plataformas, categorias

    # Categorías
    dir_cat = datos / "categorias"
    ids_categoria: set[str] = set()
    for ruta in sorted(dir_cat.glob("*.json")):
        cat = _leer_json(ruta, errores)
        if cat is None:
            continue
        prefijo = f"categorias/{ruta.name}"
        errs = validar_esquema(cat, ESQUEMA_CATEGORIA, "")
        errores.extend(f"{prefijo}: {e.lstrip(': ')}" for e in errs)
        if isinstance(cat, dict) and cat.get("id") != ruta.stem:
            errores.append(f"{prefijo}: el id {cat.get('id')!r} no coincide con el nombre del fichero")
        if isinstance(cat, dict):
            ids_categoria.add(ruta.stem)
            categorias.append(cat)
    if not categorias:
        errores.append("categorias/: no hay ninguna categoría")

    # Plataformas
    dir_plat = datos / "plataformas"
    ficheros = sorted(dir_plat.glob("*.json"))
    if not ficheros:
        errores.append("plataformas/: no hay ninguna plataforma")
    nombres_vistos: dict[str, str] = {}
    for ruta in ficheros:
        p = _leer_json(ruta, errores)
        if p is None:
            continue
        prefijo = f"plataformas/{ruta.name}"
        errs = validar_esquema(p, esquema, "")
        errores.extend(f"{prefijo}: {e.lstrip(': ')}" for e in errs)
        if not isinstance(p, dict):
            continue
        if p.get("id") != ruta.stem:
            errores.append(f"{prefijo}: el id {p.get('id')!r} no coincide con el nombre del fichero")
        if p.get("categoria") and p["categoria"] not in ids_categoria:
            errores.append(f"{prefijo}: la categoría {p['categoria']!r} no tiene fichero en categorias/")
        nombre = str(p.get("nombre", "")).casefold()
        if nombre in nombres_vistos:
            avisos.append(f"{prefijo}: el nombre {p.get('nombre')!r} se repite en {nombres_vistos[nombre]}")
        nombres_vistos[nombre] = ruta.name
        fuentes = p.get("fuentes") or []
        if isinstance(fuentes, list) and len(set(fuentes)) != len(fuentes):
            avisos.append(f"{prefijo}: hay fuentes repetidas")
        plataformas.append(p)

    return errores, avisos, plataformas, categorias


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida los datos del catálogo Conectores para pymes.")
    parser.add_argument("--datos", type=Path, default=DATOS_POR_DEFECTO,
                        help="carpeta de datos (por defecto: datos/ del repo)")
    parser.add_argument("--silencioso", action="store_true", help="no muestra los avisos")
    args = parser.parse_args(argv)

    errores, avisos, plataformas, categorias = validar(args.datos)

    if avisos and not args.silencioso:
        print(f"Avisos ({len(avisos)}):")
        for a in avisos:
            print(f"  - {a}")
    if errores:
        print(f"ERROR: {len(errores)} problema(s) en {args.datos}:", file=sys.stderr)
        for e in errores:
            print(f"  - {e}", file=sys.stderr)
        print("\nCorrígelos y vuelve a ejecutar: python3 scripts/validar.py", file=sys.stderr)
        return 1

    fechas = sorted(p["verificado_el"] for p in plataformas)
    print(f"OK: {len(plataformas)} plataformas y {len(categorias)} categorías válidas.")
    print(f"Verificación más antigua: {fechas[0]} · más reciente: {fechas[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
