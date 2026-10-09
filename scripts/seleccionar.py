#!/usr/bin/env python3
"""Elige qué fichas revisar en la verificación semanal.

Por defecto, las N (10) plataformas con el `verificado_el` más antiguo (a
igualdad de fecha, por orden alfabético de id). Con --ids, exactamente esas.

Uso:
    python3 scripts/seleccionar.py                       # las 10 más antiguas
    python3 scripts/seleccionar.py --n 5
    python3 scripts/seleccionar.py --ids holded,sage-50
    python3 scripts/seleccionar.py --github-output       # escribe ids, ficheros y fecha en $GITHUB_OUTPUT
    python3 scripts/seleccionar.py --comprobar-secreto   # falla con explicación si no hay credencial de Claude

Funciona sin ningún secreto: la selección no lo necesita. --comprobar-secreto
solo se usa en el workflow, después de seleccionar, para parar con un mensaje
claro antes de llamar a Claude.

Solo usa la librería estándar de Python 3.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RE_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

MENSAJE_SIN_SECRETO = """\
No hay credencial para Claude, así que no se puede hacer la verificación.

Configura UNO de estos dos secretos en GitHub
(Settings > Secrets and variables > Actions > New repository secret):

  - ANTHROPIC_API_KEY        clave de la API de Anthropic (platform.claude.com),
                             se paga por uso.
  - CLAUDE_CODE_OAUTH_TOKEN  token de una suscripción Claude (Pro, Max, Team o Enterprise);
                             se genera en tu ordenador con: claude setup-token

Después vuelve a lanzar el workflow «Verificación semanal» desde la pestaña Actions
(botón «Run workflow»). Arriba tienes las fichas que tocaba revisar; en cada
ejecución se vuelven a elegir, así que no se pierde nada."""


def cargar(datos: Path) -> list[dict]:
    plataformas = []
    for ruta in sorted((datos / "plataformas").glob("*.json")):
        p = json.loads(ruta.read_text(encoding="utf-8"))
        plataformas.append({"id": p.get("id", ruta.stem), "verificado_el": p.get("verificado_el", "0000-00-00"),
                            "nombre": p.get("nombre", ruta.stem)})
    return plataformas


def seleccionar(plataformas: list[dict], n: int, ids: list[str]) -> list[dict]:
    if ids:
        por_id = {p["id"]: p for p in plataformas}
        desconocidos = [i for i in ids if i not in por_id]
        if desconocidos:
            raise ValueError("ids que no existen en datos/plataformas/: " + ", ".join(desconocidos))
        vistos: list[str] = []
        for i in ids:
            if i not in vistos:
                vistos.append(i)
        return [por_id[i] for i in vistos]
    return sorted(plataformas, key=lambda p: (p["verificado_el"], p["id"]))[:n]


def parsear_ids(texto: str) -> list[str]:
    ids = [t.strip().lower() for t in re.split(r"[,\s]+", texto or "") if t.strip()]
    malos = [i for i in ids if not RE_ID.match(i)]
    if malos:
        raise ValueError("ids con formato no válido (solo minúsculas, números y guiones): " + ", ".join(malos))
    return ids


def hay_secreto() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY", "").strip()
                or os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "").strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Elige las fichas que se verificarán esta semana.")
    parser.add_argument("--n", type=int, default=10, help="cuántas fichas elegir (por defecto: 10)")
    parser.add_argument("--ids", default="", help="lista de ids separada por comas; si se da, ignora --n")
    parser.add_argument("--datos", type=Path, default=RAIZ / "datos", help="carpeta de datos (por defecto: datos/)")
    parser.add_argument("--formato", choices=["texto", "json", "lista"], default="texto",
                        help="texto (legible), json o lista (una ruta de fichero por línea)")
    parser.add_argument("--github-output", action="store_true",
                        help="escribe ids, ficheros, n y fecha en el fichero $GITHUB_OUTPUT")
    parser.add_argument("--comprobar-secreto", action="store_true",
                        help="termina con error y explicación si no hay ANTHROPIC_API_KEY ni CLAUDE_CODE_OAUTH_TOKEN")
    args = parser.parse_args(argv)

    if args.n < 1:
        print("ERROR: --n tiene que ser 1 o más.", file=sys.stderr)
        return 2
    try:
        ids = parsear_ids(args.ids)
        elegidas = seleccionar(cargar(args.datos), args.n, ids)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if not elegidas:
        print("ERROR: no hay plataformas en datos/plataformas/.", file=sys.stderr)
        return 2

    ficheros = [f"datos/plataformas/{p['id']}.json" for p in elegidas]
    hoy = dt.datetime.now(dt.timezone.utc).date().isoformat()

    if args.formato == "json":
        print(json.dumps({"fecha": hoy, "ids": [p["id"] for p in elegidas], "ficheros": ficheros},
                         ensure_ascii=False, indent=2))
    elif args.formato == "lista":
        print("\n".join(ficheros))
    else:
        motivo = "elegidas a mano (--ids)" if ids else f"las {len(elegidas)} con la verificación más antigua"
        print(f"Fichas a verificar ({motivo}):")
        for p in elegidas:
            print(f"  - {p['id']:<22} verificado el {p['verificado_el']}  ({p['nombre']})")

    if args.github_output:
        destino = os.environ.get("GITHUB_OUTPUT")
        if not destino:
            print("ERROR: --github-output necesita la variable GITHUB_OUTPUT (solo existe en GitHub Actions).",
                  file=sys.stderr)
            return 2
        with open(destino, "a", encoding="utf-8") as f:
            f.write(f"ids={','.join(p['id'] for p in elegidas)}\n")
            f.write(f"ficheros={' '.join(ficheros)}\n")
            f.write(f"n={len(elegidas)}\n")
            f.write(f"fecha={hoy}\n")

    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen and args.github_output:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write("### Fichas seleccionadas\n\n")
            f.write("\n".join(f"- `{p['id']}` (verificado el {p['verificado_el']})" for p in elegidas) + "\n\n")

    if args.comprobar_secreto and not hay_secreto():
        print("\n" + MENSAJE_SIN_SECRETO, file=sys.stderr)
        print("::error title=Falta el secreto de Claude::Configura ANTHROPIC_API_KEY o CLAUDE_CODE_OAUTH_TOKEN "
              "en Settings > Secrets and variables > Actions y vuelve a lanzar el workflow.")
        if resumen:
            with open(resumen, "a", encoding="utf-8") as f:
                f.write("### No se ha verificado nada: falta el secreto\n\n```\n" + MENSAJE_SIN_SECRETO + "\n```\n")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
