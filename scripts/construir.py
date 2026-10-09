#!/usr/bin/env python3
"""Genera la web estática del catálogo en sitio/.

Salida:
    sitio/index.html        página autocontenida (CSS y JS en línea)
    sitio/catalogo.json     todas las plataformas y categorías (API pública)
    sitio/esquema.json      el JSON Schema de una plataforma
    sitio/guias/<slug>.html una página por guía de guias/*.md

Uso:
    python3 scripts/construir.py
    python3 scripts/construir.py --salida /tmp/sitio --base-url http://localhost:8000/

Solo usa la librería estándar de Python 3. Valida los datos antes de construir
(con scripts/validar.py) y no genera nada si hay errores.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validar  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
BASE_URL = "https://executive-lab.github.io/conectores-pymes/"
REPO_URL = "https://github.com/Executive-Lab/conectores-pymes"

AVISO = ("Información orientativa. Los planes, precios y MCP cambian cada mes: "
         "verifica en la fuente antes de decidir.")

ORDEN_CATEGORIAS = [
    "erp-contabilidad",
    "ofimatica-mensajeria",
    "crm-email",
    "ads-ecommerce-bi",
    "hosteleria-nicho",
]

# slug -> descripción corta para la portada (el orden es el de la portada)
GUIAS = {
    "conectar-una-plataforma-con-rsc": "Las cinco vías (MCP, API con clave, app OAuth, "
    "programa instalado y RPA), cómo elegir y cómo hacerlo con permisos acotados.",
    "hablar-con-el-informatico": "Qué pedir, con qué palabras y qué no aceptar: "
    "textos listos para tu informático, tu distribuidor o tu gestoría.",
    "conectar-o-migrar": "Señales de que una herramienta frena, cuándo no conviene "
    "cambiar, cómo hacer la cuenta y cómo migrar sin perder datos.",
}

DIFICULTAD = {
    "Fácil": ("🟢", "facil"),
    "Media": ("🟡", "media"),
    "Difícil": ("🟠", "dificil"),
    "Muy difícil": ("🔴", "muy-dificil"),
}
VEREDICTO_CORTO = {
    "conectar tal cual": "conectar",
    "conectar con puente (export/BD/partner)": "puente",
    "valorar migración": "migrar",
}
VEREDICTO_ETIQUETA = {
    "conectar": "Conectar tal cual",
    "puente": "Conectar con puente",
    "migrar": "Valorar migración",
}
MCP_ETIQUETA = {"oficial": "Oficial", "comunitario": "Comunitario", "ninguno": "No hay"}
API_ETIQUETA = {"sí": "Sí", "limitada": "Limitada", "no": "No"}
ETIQUETAS_OBJETO = {
    "opcion": "Opción",
    "api_incluida": "¿Incluye la API?",
    "limites": "Límites",
    "plan": "Plan",
    "precio": "Precio",
    "facturacion": "Facturación",
    "verificado": "¿Verificado?",
}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]

RE_TERCERO = re.compile(
    r"\b(distribuidor|partner|informático|gestoría|comercial|franquicia|banco|BSP|Tech Provider|CSM)\b"
    # Administrador del tenant de Microsoft o Google (no el admin de un SaaS, que suele ser el propio dueño).
    r"|Entra ID|\btenant\b|admin\.google\.com|consentimiento de administrador"
    r"|admin(?:istrador)? de (?:Microsoft|Google|Workspace|Fabric)",
    re.IGNORECASE,
)
RE_URL = re.compile(r"https?://[^\s<>\"'\]]+")


# --------------------------------------------------------------------------
# Derivados
# --------------------------------------------------------------------------

def via_principal(p: dict) -> str:
    if p["dificultad"] == "Muy difícil":
        return "RPA"
    if p["mcp"]["estado"] == "oficial":
        return "MCP oficial"
    if p["api"]["existe"] == "sí":
        return "API + MCP comunitario" if p["mcp"]["estado"] == "comunitario" else "API"
    if p["api"]["existe"] == "limitada":
        return "API limitada / puente"
    if p["rpa"].strip().lower().startswith("no hace falta"):
        return "Puente (export / BD)"
    return "RPA o export"


def pide_informatico(p: dict) -> bool:
    """Necesita a un tercero (informático, distribuidor, partner, gestoría...).

    Criterio: programa de escritorio u on-premise, dificultad 'Difícil', o que
    el texto de 'qué pedir' se dirija a un distribuidor, partner, gestoría,
    comercial, franquicia, banco, proveedor (BSP) o al administrador del
    tenant (Google Workspace, Microsoft 365: consentimiento de administrador)."""
    return (
        p["tipo"] == "escritorio/on-premise"
        or p["dificultad"] == "Difícil"
        or bool(RE_TERCERO.search(p["pedir_al_informatico"]))
    )


def derivados(p: dict, base_url: str) -> dict:
    return {
        "via_principal": via_principal(p),
        "veredicto_corto": VEREDICTO_CORTO[p["migracion"]["veredicto"]],
        "hay_demo_gratis": p["demo_resumen"] != "no hay",
        "pide_informatico": pide_informatico(p),
        "url": f"{base_url}#p-{p['id']}",
    }


# --------------------------------------------------------------------------
# Utilidades de HTML
# --------------------------------------------------------------------------

def esc(texto: object) -> str:
    return html.escape(str(texto), quote=True)


def sin_acentos(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def slug(texto: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", sin_acentos(texto).lower()).strip("-")


def fecha_larga(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def url_corta(url: str, maximo: int = 64) -> str:
    corta = re.sub(r"^https?://(www\.)?", "", url).rstrip("/")
    if len(corta) <= maximo:
        return corta
    # recorta por el medio para que se distingan dos URL del mismo sitio
    cabeza = maximo // 2 - 4
    return corta[:cabeza] + "…" + corta[-(maximo - cabeza - 1):]


def _partir_url(bruto: str) -> tuple[str, str]:
    """Separa la puntuación final que no forma parte de la URL."""
    url = bruto
    cola = ""
    while url and url[-1] in ".,;:)":
        if url[-1] == ")" and url.count("(") >= url.count(")"):
            break
        cola = url[-1] + cola
        url = url[:-1]
    return url, cola


def enlazar(texto: str) -> str:
    """Escapa el texto y convierte las URL en enlaces."""
    partes: list[str] = []
    pos = 0
    for m in RE_URL.finditer(texto):
        url, cola = _partir_url(m.group(0))
        partes.append(esc(texto[pos:m.start()]))
        partes.append(f'<a href="{esc(url)}">{esc(url_corta(url, 80))}</a>{esc(cola)}')
        pos = m.end()
    partes.append(esc(texto[pos:]))
    return "".join(partes).replace("\n", "<br>")


# --------------------------------------------------------------------------
# Markdown -> HTML (mínimo, sin dependencias)
# --------------------------------------------------------------------------

RE_ITEM = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
RE_SEPARADOR_TABLA = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")


class Markdown:
    """Conversor mínimo: títulos, párrafos, listas (con anidado), citas,
    tablas, código, separadores, negrita, cursiva, código en línea y enlaces."""

    def __init__(self, reescribir_enlace=None):
        self.reescribir = reescribir_enlace or (lambda u: u)
        self.ids: set[str] = set()

    # --- en línea
    def en_linea(self, texto: str) -> str:
        guardados: dict[str, str] = {}

        def guardar(fragmento: str) -> str:
            clave = f"\x00{len(guardados)}\x00"
            guardados[clave] = fragmento
            return clave

        t = re.sub(r"\\([\\`*_{}\[\]()#+\-.!<>|])", lambda m: guardar(esc(m.group(1))), texto)
        t = re.sub(r"`([^`]+)`", lambda m: guardar(f"<code>{esc(m.group(1))}</code>"), t)

        def enlace(m: re.Match) -> str:
            href = esc(self.reescribir(m.group(2)))
            return guardar(f'<a href="{href}">{self._enfasis(esc(m.group(1)))}</a>')

        t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", enlace, t)
        t = self._enfasis(esc(t))
        for _ in range(5):
            if "\x00" not in t:
                break
            for clave, valor in guardados.items():
                t = t.replace(clave, valor)
        return t

    @staticmethod
    def _enfasis(t: str) -> str:
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", t)
        return t

    # --- bloques
    def convertir(self, texto: str) -> str:
        return self._bloques(texto.replace("\r\n", "\n").split("\n"))

    @staticmethod
    def _empieza_bloque(linea: str) -> bool:
        s = linea.lstrip()
        return (
            s.startswith(("#", ">", "|", "```"))
            or bool(RE_ITEM.match(linea))
        )

    def _id_titulo(self, texto: str) -> str:
        base = slug(re.sub(r"<[^>]+>", "", texto)) or "seccion"
        candidato, n = base, 2
        while candidato in self.ids:
            candidato, n = f"{base}-{n}", n + 1
        self.ids.add(candidato)
        return candidato

    def _bloques(self, lineas: list[str]) -> str:
        salida: list[str] = []
        i, n = 0, len(lineas)
        while i < n:
            linea = lineas[i]
            if not linea.strip():
                i += 1
                continue
            s = linea.lstrip()

            if s.startswith("```"):
                j, buf = i + 1, []
                while j < n and not lineas[j].lstrip().startswith("```"):
                    buf.append(lineas[j])
                    j += 1
                salida.append(f"<pre><code>{esc(chr(10).join(buf))}</code></pre>")
                i = j + 1
                continue

            m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", s)
            if m:
                nivel = len(m.group(1))
                contenido = self.en_linea(m.group(2))
                salida.append(f'<h{nivel} id="{self._id_titulo(contenido)}">{contenido}</h{nivel}>')
                i += 1
                continue

            if re.match(r"^([-*_])(\s*\1){2,}\s*$", s):
                salida.append("<hr>")
                i += 1
                continue

            if s.startswith(">"):
                buf = []
                while i < n and lineas[i].lstrip().startswith(">"):
                    buf.append(re.sub(r"^\s*>\s?", "", lineas[i]))
                    i += 1
                salida.append(f"<blockquote>{self._bloques(buf)}</blockquote>")
                continue

            if s.startswith("|") and i + 1 < n and RE_SEPARADOR_TABLA.match(lineas[i + 1]):
                cabecera = self._celdas(linea)
                i += 2
                filas = []
                while i < n and lineas[i].lstrip().startswith("|"):
                    filas.append(self._celdas(lineas[i]))
                    i += 1
                th = "".join(f'<th scope="col">{self.en_linea(c)}</th>' for c in cabecera)
                cuerpo = "".join(
                    "<tr>" + "".join(f"<td>{self.en_linea(c)}</td>" for c in fila) + "</tr>"
                    for fila in filas
                )
                salida.append(
                    f'<div class="tabla-env"><table><thead><tr>{th}</tr></thead>'
                    f"<tbody>{cuerpo}</tbody></table></div>"
                )
                continue

            if RE_ITEM.match(linea):
                html_lista, i = self._lista(lineas, i)
                salida.append(html_lista)
                continue

            buf = [s.strip()]
            i += 1
            while i < n and lineas[i].strip() and not self._empieza_bloque(lineas[i]):
                buf.append(lineas[i].strip())
                i += 1
            salida.append(f"<p>{self.en_linea(' '.join(buf))}</p>")
        return "\n".join(salida)

    @staticmethod
    def _celdas(linea: str) -> list[str]:
        s = linea.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        return [c.strip() for c in s.split("|")]

    def _lista(self, lineas: list[str], i: int) -> tuple[str, int]:
        primera = RE_ITEM.match(lineas[i])
        sangria = len(primera.group(1))
        ordenada = primera.group(2)[0].isdigit()
        inicio = int(re.sub(r"\D", "", primera.group(2))) if ordenada else 1
        elementos: list[list[str]] = []
        n = len(lineas)
        while i < n:
            linea = lineas[i]
            m = RE_ITEM.match(linea)
            if m and len(m.group(1)) == sangria and m.group(2)[0].isdigit() == ordenada:
                elementos.append([m.group(3)])
                i += 1
                continue
            if not linea.strip():
                j = i + 1
                while j < n and not lineas[j].strip():
                    j += 1
                if j < n:
                    mj = RE_ITEM.match(lineas[j])
                    sangria_j = len(lineas[j]) - len(lineas[j].lstrip())
                    if (mj and len(mj.group(1)) == sangria and mj.group(2)[0].isdigit() == ordenada) \
                            or sangria_j > sangria:
                        elementos[-1].append("")
                        i = j
                        continue
                break
            sangria_l = len(linea) - len(linea.lstrip())
            if sangria_l > sangria:
                # quita la sangría del elemento y conserva la que sobre (listas anidadas)
                elementos[-1].append(linea[min(sangria_l, sangria + 4):])
                i += 1
                continue
            if self._empieza_bloque(linea):
                break
            elementos[-1].append(linea.strip())  # continuación perezosa
            i += 1

        items_html = []
        for el in elementos:
            if len(el) == 1:
                items_html.append(f"<li>{self.en_linea(el[0])}</li>")
                continue
            interior = self._bloques(el)
            # un solo párrafo (con o sin lista anidada) va sin <p>, como en las listas compactas
            if interior.startswith("<p>") and interior.count("<p>") == 1:
                fin = interior.find("</p>")
                interior = interior[3:fin] + interior[fin + 4:]
            items_html.append(f"<li>{interior}</li>")
        etiqueta = "ol" if ordenada else "ul"
        atr_inicio = f' start="{inicio}"' if ordenada and inicio != 1 else ""
        return f"<{etiqueta}{atr_inicio}>" + "".join(items_html) + f"</{etiqueta}>", i


def quitar_frontmatter(texto: str) -> str:
    m = re.match(r"^---\n.*?\n---\n+", texto, re.S)
    return texto[m.end():] if m else texto


# --------------------------------------------------------------------------
# CSS y JS compartidos
# --------------------------------------------------------------------------

CSS = r"""
:root{
  --papel:#e9e1d9;--superficie:#f6f2ed;--superficie-2:#efe8e0;
  --tinta:#161310;--tinta-suave:#5c534b;--linea:#cbbfb2;--linea-fuerte:#161310;
  --rojo:#ec4429;--rojo-texto:#a82b16;--sobre-rojo:#161310;--foco:#a82b16;
  --radio:2px;
  --fuente:"Helvetica Neue",Helvetica,Arial,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){
  :root{
    --papel:#161310;--superficie:#211c18;--superficie-2:#2a241f;
    --tinta:#e9e1d9;--tinta-suave:#a89d92;--linea:#3d352e;--linea-fuerte:#e9e1d9;
    --rojo:#ec4429;--rojo-texto:#ff8a6e;--sobre-rojo:#161310;--foco:#ff8a6e;
    color-scheme:dark;
  }
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{margin:0;background:var(--papel);color:var(--tinta);font-family:var(--fuente);font-size:1rem;line-height:1.55;overflow-wrap:break-word}
a{color:var(--rojo-texto);text-decoration-thickness:1px;text-underline-offset:2px}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--foco);outline-offset:2px}
[hidden]{display:none!important}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.saltar{position:absolute;left:16px;top:-200px;background:var(--tinta);color:var(--papel);padding:8px 12px;z-index:10}
.saltar:focus{top:8px}
.envoltura{max-width:1200px;margin:0 auto;padding:0 16px}
@media (min-width:720px){.envoltura{padding:0 32px}}
.franja{height:6px;background:var(--rojo)}
.barra{border-bottom:1px solid var(--linea)}
.barra .envoltura{display:flex;justify-content:space-between;align-items:center;gap:8px 16px;min-height:56px;flex-wrap:wrap;padding-top:8px;padding-bottom:8px}
.marca{display:inline-flex;align-items:center;gap:10px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;font-size:.8rem;color:var(--tinta);text-decoration:none}
.marca::before{content:"";width:14px;height:14px;background:var(--rojo);flex:none}
.barra-nota{font-size:.85rem;color:var(--tinta-suave)}
.cabecera{padding:40px 0 32px}
.kicker{margin:0 0 8px;font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--rojo-texto)}
h1{font-size:clamp(2.1rem,7vw,4rem);line-height:1.02;letter-spacing:-.025em;margin:0 0 16px;font-weight:800}
.entradilla{font-size:clamp(1.05rem,2.2vw,1.3rem);max-width:48ch;margin:0 0 12px}
.para-quien{color:var(--tinta-suave);max-width:64ch;margin:0}
.guias-titulo{font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin:32px 0 8px}
.guias{list-style:none;margin:0;padding:0;display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))}
.guia-enlace{display:block;height:100%;padding:16px;background:var(--superficie);border:1px solid var(--linea);border-top:3px solid var(--rojo);color:var(--tinta);text-decoration:none}
.guia-enlace strong{display:block;margin-bottom:4px;font-size:1.05rem;line-height:1.3}
.guia-enlace span{color:var(--tinta-suave);font-size:.92rem}
.guia-enlace:hover strong{text-decoration:underline}
.seccion{padding:32px 0;border-top:2px solid var(--linea-fuerte)}
.seccion-titulo{display:flex;align-items:baseline;gap:12px;font-size:clamp(1.4rem,3vw,1.9rem);line-height:1.15;margin:0 0 8px;letter-spacing:-.01em}
.num{font-size:.8rem;font-weight:700;color:var(--rojo-texto);letter-spacing:.1em;flex:none}
.intro{max-width:70ch;margin:0 0 16px;color:var(--tinta-suave)}
label,.etiqueta{display:block;font-size:.8rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px}
input[type=search],input[type=text],select{width:100%;font:inherit;padding:10px 12px;border:1px solid var(--tinta-suave);background:var(--papel);color:var(--tinta);border-radius:var(--radio);min-height:44px}
.boton{font:inherit;font-weight:600;display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:44px;padding:8px 14px;border:1px solid var(--tinta);background:transparent;color:var(--tinta);border-radius:var(--radio);cursor:pointer;text-align:center}
.boton:hover{background:var(--superficie-2)}
.boton:disabled{opacity:.5;cursor:not-allowed}
.boton-primario{background:var(--rojo);border-color:var(--rojo);color:var(--sobre-rojo)}
.boton-primario:hover{background:var(--rojo);box-shadow:inset 0 0 0 2px var(--sobre-rojo)}
.boton[aria-pressed=true]{background:var(--tinta);color:var(--papel)}
.boton-peq{min-height:36px;padding:4px 10px;font-size:.9rem}
.mh-form{display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end}
.mh-form .campo{flex:1 1 240px}
.mh-acciones{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
.mensaje{min-height:1.5em;margin:8px 0;font-size:.95rem}
.chips{list-style:none;padding:0;margin:12px 0;display:flex;flex-wrap:wrap;gap:8px}
.chip{display:inline-flex;align-items:center;gap:2px;border:1px solid var(--tinta);border-radius:999px;padding:2px 2px 2px 12px;background:var(--superficie);font-weight:600}
.chip button{border:0;background:transparent;color:inherit;font:inherit;font-size:1.2rem;line-height:1;width:32px;height:32px;border-radius:999px;cursor:pointer}
.chip button:hover{background:var(--superficie-2)}
.vacio{color:var(--tinta-suave)}
.cifras{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,140px),1fr));gap:8px;margin:16px 0}
.cifra{background:var(--superficie);border:1px solid var(--linea);border-top:3px solid var(--tinta);padding:12px}
.cifra b{display:block;font-size:2rem;line-height:1.1}
.cifra span{font-size:.9rem;color:var(--tinta-suave)}
.resumen-listas{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));margin:16px 0}
.resumen-listas h3{font-size:1rem;margin:0 0 6px}
.resumen-listas ul{margin:0;padding-left:1.2em}
.tabla-env{overflow-x:auto;max-width:100%;margin:16px 0}
table{border-collapse:collapse;width:100%;font-size:.95rem;background:var(--superficie)}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--linea);vertical-align:top}
th{font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;border-bottom:2px solid var(--linea-fuerte)}
.filtros{display:grid;gap:12px;grid-template-columns:1fr;margin:16px 0;padding:16px;background:var(--superficie);border:1px solid var(--linea)}
@media (min-width:720px){.filtros{grid-template-columns:2fr 1fr 1fr 1fr}}
.filtros-fila{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:8px 24px;align-items:center;justify-content:space-between}
.check{display:inline-flex;gap:10px;align-items:center;min-height:44px;font-size:1rem;font-weight:600;letter-spacing:0;text-transform:none;margin:0;cursor:pointer}
.check input{width:20px;height:20px;accent-color:var(--rojo);margin:0}
.recuento{font-weight:600;margin:8px 0}
.leyenda{margin:8px 0 0;background:var(--superficie-2);border:1px solid var(--linea);padding:0 16px}
.leyenda>summary,.hallazgos>summary{cursor:pointer;font-weight:700;padding:12px 0}
.leyenda[open],.hallazgos[open]{padding-bottom:16px}
.leyenda dl{margin:0;display:grid;gap:4px 16px}
@media (min-width:720px){.leyenda dl{grid-template-columns:minmax(160px,auto) 1fr}}
.leyenda dt{font-weight:700}
.leyenda dd{margin:0 0 8px}
.categoria{margin-top:40px}
.categoria-titulo{font-size:clamp(1.15rem,2.4vw,1.45rem);line-height:1.2;margin:0;padding-top:12px;border-top:1px solid var(--linea-fuerte);display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 16px;align-items:baseline}
.cat-recuento{font-size:.85rem;font-weight:600;color:var(--tinta-suave)}
.hallazgos{margin:12px 0 0;background:var(--superficie-2);border:1px solid var(--linea);padding:0 16px}
.hallazgos h4{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--rojo-texto);margin:12px 0 6px}
.hallazgos ul{margin:0;padding-left:1.2em}
.hallazgos li{margin-bottom:6px}
.hallazgos p{margin:0;max-width:90ch}
.hallazgos a,.detalle a,.normativa a{overflow-wrap:anywhere}
.rejilla{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));align-items:stretch}
.rejilla>li:has(details[open]){grid-column:1/-1}
.ficha{background:var(--superficie);border:1px solid var(--linea);border-top:3px solid var(--tinta);padding:16px;display:flex;flex-direction:column;gap:12px;height:100%;scroll-margin-top:16px}
.ficha.es-mia{border-color:var(--rojo);border-top-width:6px}
.ficha-cab{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}
.ficha-nombre{margin:0;font-size:1.2rem;line-height:1.2}
.ficha-tipo{margin:4px 0 0;font-size:.85rem;color:var(--tinta-suave)}
.insignia{white-space:nowrap;font-size:.85rem;font-weight:700;padding:3px 10px;border:1px solid var(--linea);background:var(--papel);border-radius:999px;flex:none}
.claves{display:grid;grid-template-columns:auto 1fr;gap:6px 12px;margin:0;font-size:.92rem}
.claves dt{color:var(--tinta-suave);font-weight:600}
.claves dd{margin:0}
.v-migrar{color:var(--rojo-texto);font-weight:700}
.v-puente{font-weight:700}
.v-conectar{font-weight:700}
.marca-tercero{display:inline-block;font-size:.8rem;font-weight:700;border:1px dashed var(--tinta-suave);padding:2px 8px;border-radius:var(--radio);align-self:flex-start}
.acciones-ficha{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto}
.detalle-ficha{border-top:1px solid var(--linea);padding-top:4px}
.detalle-ficha>summary{cursor:pointer;font-weight:700;padding:10px 0;min-height:44px}
.detalle{display:grid;gap:0 40px;grid-template-columns:1fr;font-size:.95rem}
@media (min-width:900px){.rejilla>li:has(details[open]) .detalle{grid-template-columns:1fr 1fr}}
.bloque h5{font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;margin:16px 0 4px;color:var(--rojo-texto)}
.bloque p,.bloque ul,.bloque ol,.bloque dl{margin:0 0 8px}
.bloque ul,.bloque ol{padding-left:1.3em}
.bloque li{margin-bottom:4px}
.bloque dl{display:grid;grid-template-columns:1fr;gap:2px}
.bloque dt{font-weight:700}
.bloque dd{margin:0 0 6px}
.pedir{background:var(--papel);border-left:3px solid var(--rojo);padding:8px 12px;margin:0 0 8px}
.meta{grid-column:1/-1;font-size:.85rem;color:var(--tinta-suave);border-top:1px solid var(--linea);padding-top:8px;margin:12px 0 0}
.sin-resultados{padding:24px;background:var(--superficie);border:1px dashed var(--tinta-suave)}
.pie{border-top:2px solid var(--linea-fuerte);margin-top:48px;padding:24px 0 48px;font-size:.92rem;color:var(--tinta-suave)}
.pie p{margin:0 0 8px;max-width:80ch}
.pie .aviso{color:var(--tinta);font-size:1rem}
.guia{max-width:780px;padding-top:24px;padding-bottom:16px}
.guia h1{font-size:clamp(1.8rem,5vw,2.8rem);line-height:1.08}
.guia h2{font-size:1.45rem;margin:2em 0 .5em;padding-top:.6em;border-top:2px solid var(--linea-fuerte)}
.guia h3{font-size:1.15rem;margin:1.6em 0 .4em}
.guia blockquote{margin:16px 0;padding:4px 16px;border-left:4px solid var(--rojo);background:var(--superficie)}
.guia li{margin-bottom:6px}
.guia code{font-family:var(--mono);font-size:.88em;background:var(--superficie-2);padding:.1em .3em;border-radius:2px;overflow-wrap:anywhere}
.guia pre{overflow-x:auto;background:var(--superficie-2);padding:12px}
.volver{display:inline-block;margin:0 0 8px;font-weight:600}
.otras-guias{border-top:2px solid var(--linea-fuerte);margin-top:40px;padding-top:16px}
@media print{.filtros,#mis-herramientas,.acciones-ficha,.saltar{display:none!important}}
"""

JS = r"""
(function () {
  'use strict';
  var nodoDatos = document.getElementById('indice');
  if (!nodoDatos || !('URLSearchParams' in window)) return;
  var datos = JSON.parse(nodoDatos.textContent);
  var porId = {};
  datos.forEach(function (p) { porId[p.id] = p; });

  var ORDEN_DIF = ['Fácil', 'Media', 'Difícil', 'Muy difícil'];
  var EMOJI = { 'Fácil': '🟢', 'Media': '🟡', 'Difícil': '🟠', 'Muy difícil': '🔴' };
  var VEREDICTO = { conectar: 'Conectar tal cual', puente: 'Conectar con puente', migrar: 'Valorar migración' };

  function norm(s) {
    return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
  }
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function el(tag, attrs, hijos) {
    var nodo = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) { nodo.setAttribute(k, attrs[k]); });
    }
    (hijos || []).forEach(function (h) {
      nodo.appendChild(typeof h === 'string' ? document.createTextNode(h) : h);
    });
    return nodo;
  }

  $$('[data-requiere-js]').forEach(function (n) { n.hidden = false; });

  var items = $$('.ficha').map(function (n) {
    return { el: n, li: n.parentNode, p: porId[n.getAttribute('data-id')], texto: norm(n.getAttribute('data-buscar')) };
  }).filter(function (it) { return it.p; });
  var secciones = $$('.categoria');

  var f = {
    q: $('#f-q'), cat: $('#f-cat'), dif: $('#f-dif'), ver: $('#f-ver'), demo: $('#f-demo'),
    form: $('#filtros'), limpiar: $('#f-limpiar'), recuento: $('#recuento'), vacio: $('#sin-resultados')
  };
  var mh = {
    form: $('#mh-form'), input: $('#mh-buscar'), chips: $('#mh-chips'), resumen: $('#mh-resumen'),
    msg: $('#mh-mensaje'), copiar: $('#mh-copiar'), solo: $('#mh-solo'), vaciar: $('#mh-vaciar')
  };

  var estado = { q: '', cat: '', dif: '', ver: '', demo: false, solo: false, mias: [] };

  function leerURL() {
    var params = new URLSearchParams(window.location.search);
    estado.mias = [];
    (params.get('h') || '').split(',').forEach(function (id) {
      id = id.trim().toLowerCase();
      if (id && porId[id] && estado.mias.indexOf(id) === -1) estado.mias.push(id);
    });
    estado.q = params.get('q') || '';
    estado.cat = params.get('cat') || '';
    estado.dif = params.get('dif') || '';
    estado.ver = params.get('ver') || '';
    estado.demo = params.get('demo') === '1';
    estado.solo = params.get('solo') === '1' && estado.mias.length > 0;
  }

  function query() {
    var partes = [];
    if (estado.mias.length) partes.push('h=' + estado.mias.join(','));
    if (estado.q) partes.push('q=' + encodeURIComponent(estado.q));
    if (estado.cat) partes.push('cat=' + encodeURIComponent(estado.cat));
    if (estado.dif) partes.push('dif=' + encodeURIComponent(estado.dif));
    if (estado.ver) partes.push('ver=' + encodeURIComponent(estado.ver));
    if (estado.demo) partes.push('demo=1');
    if (estado.solo) partes.push('solo=1');
    return partes.length ? '?' + partes.join('&') : '';
  }

  function escribirURL() {
    try {
      window.history.replaceState(null, '', window.location.pathname + query() + window.location.hash);
    } catch (e) { /* algunos navegadores no lo permiten en file:// */ }
  }

  function sincronizarControles() {
    f.q.value = estado.q;
    f.cat.value = estado.cat;
    f.dif.value = estado.dif;
    f.ver.value = estado.ver;
    f.demo.checked = estado.demo;
    estado.cat = f.cat.value;
    estado.dif = f.dif.value;
    estado.ver = f.ver.value;
  }

  function coincide(it, tokens) {
    var p = it.p;
    for (var i = 0; i < tokens.length; i++) {
      if (it.texto.indexOf(tokens[i]) === -1) return false;
    }
    if (estado.cat && p.categoria !== estado.cat) return false;
    if (estado.dif && p.dificultad !== estado.dif) return false;
    if (estado.ver && p.veredicto !== estado.ver) return false;
    if (estado.demo && !p.demo) return false;
    if (estado.solo && estado.mias.indexOf(p.id) === -1) return false;
    return true;
  }

  function aplicarFiltros() {
    var tokens = norm(estado.q).split(/\s+/).filter(Boolean);
    var visibles = 0;
    items.forEach(function (it) {
      var ok = coincide(it, tokens);
      it.li.hidden = !ok;
      if (ok) visibles++;
    });
    secciones.forEach(function (sec) {
      var n = $$('.rejilla > li', sec).filter(function (li) { return !li.hidden; }).length;
      sec.hidden = n === 0;
      var c = $('.cat-recuento', sec);
      if (c) c.textContent = n + (n === 1 ? ' herramienta' : ' herramientas');
    });
    var total = items.length;
    f.recuento.textContent = visibles === total
      ? 'Mostrando las ' + total + ' herramientas.'
      : 'Mostrando ' + visibles + ' de ' + total + ' herramientas.';
    f.vacio.hidden = visibles !== 0;
  }

  function enlaceFicha(p) {
    return el('a', { href: '#p-' + p.id, 'class': 'ir-ficha', 'data-id': p.id }, [p.nombre]);
  }

  function cifra(n, texto, emoji) {
    var etiqueta = el('span', null, []);
    if (emoji) etiqueta.appendChild(el('span', { 'aria-hidden': 'true' }, [emoji + ' ']));
    etiqueta.appendChild(document.createTextNode(texto));
    return el('div', { 'class': 'cifra' }, [el('b', null, [String(n)]), etiqueta]);
  }

  function bloqueLista(titulo, lista, siVacia) {
    var cont = el('div', null, [el('h3', null, [titulo + ' (' + lista.length + ')'])]);
    if (!lista.length) {
      cont.appendChild(el('p', { 'class': 'vacio' }, [siVacia]));
    } else {
      var ul = el('ul', null, []);
      lista.forEach(function (p) { ul.appendChild(el('li', null, [enlaceFicha(p)])); });
      cont.appendChild(ul);
    }
    return cont;
  }

  function renderResumen() {
    var r = mh.resumen;
    r.textContent = '';
    if (!estado.mias.length) {
      r.appendChild(el('p', { 'class': 'vacio' }, ['Aún no has elegido ninguna. Escribe su nombre arriba o pulsa «Añadir a mis herramientas» en cualquier ficha del catálogo.']));
      return;
    }
    var sel = estado.mias.map(function (id) { return porId[id]; });
    var cuenta = { 'Fácil': 0, 'Media': 0, 'Difícil': 0, 'Muy difícil': 0 };
    sel.forEach(function (p) { cuenta[p.dificultad]++; });
    var muy = cuenta['Muy difícil'];
    var textoDificiles = 'difíciles' + (muy ? ' (' + muy + (muy === 1 ? ' muy difícil)' : ' muy difíciles)') : '');
    r.appendChild(el('div', { 'class': 'cifras' }, [
      cifra(sel.length, sel.length === 1 ? 'herramienta elegida' : 'herramientas elegidas'),
      cifra(cuenta['Fácil'], 'fáciles', EMOJI['Fácil']),
      cifra(cuenta['Media'], 'medias', EMOJI['Media']),
      cifra(cuenta['Difícil'] + muy, textoDificiles, EMOJI['Difícil'])
    ]));
    var tercero = sel.filter(function (p) { return p.tercero; });
    var migrar = sel.filter(function (p) { return p.veredicto === 'migrar'; });
    r.appendChild(el('div', { 'class': 'resumen-listas' }, [
      bloqueLista('Piden a otra persona (informático, administrador de Microsoft o Google, distribuidor o partner)', tercero, 'Ninguna: las puedes conectar tú.'),
      bloqueLista('Conviene valorar migrar', migrar, 'Ninguna. Puedes conectarlas sin cambiar de herramienta.')
    ]));
    var ordenadas = sel.slice().sort(function (a, b) {
      return ORDEN_DIF.indexOf(a.dificultad) - ORDEN_DIF.indexOf(b.dificultad) || a.nombre.localeCompare(b.nombre, 'es');
    });
    var tbody = el('tbody', null, []);
    ordenadas.forEach(function (p) {
      tbody.appendChild(el('tr', null, [
        el('td', null, [enlaceFicha(p)]),
        el('td', null, [el('span', { 'aria-hidden': 'true' }, [EMOJI[p.dificultad] + ' ']), p.dificultad]),
        el('td', null, [p.via]),
        el('td', null, [VEREDICTO[p.veredicto]])
      ]));
    });
    var cab = el('tr', null, ['Herramienta', 'Dificultad', 'Vía principal', 'Veredicto'].map(function (t) {
      return el('th', { scope: 'col' }, [t]);
    }));
    r.appendChild(el('div', { 'class': 'tabla-env' }, [
      el('table', null, [el('caption', { 'class': 'sr-only' }, ['Resumen de mis herramientas']), el('thead', null, [cab]), tbody])
    ]));
  }

  function renderMias() {
    mh.chips.textContent = '';
    estado.mias.forEach(function (id) {
      var p = porId[id];
      mh.chips.appendChild(el('li', { 'class': 'chip' }, [
        el('span', null, [p.nombre]),
        el('button', { type: 'button', 'data-quitar': id, 'aria-label': 'Quitar ' + p.nombre + ' de mis herramientas' }, ['×'])
      ]));
    });
    items.forEach(function (it) {
      var sel = estado.mias.indexOf(it.p.id) !== -1;
      it.el.classList.toggle('es-mia', sel);
      var b = $('.boton-mia', it.el);
      if (b) {
        b.textContent = sel ? 'Quitar de mis herramientas' : 'Añadir a mis herramientas';
        b.setAttribute('aria-label', b.textContent + ': ' + it.p.nombre);
      }
    });
    var hay = estado.mias.length > 0;
    if (!hay) estado.solo = false;
    mh.copiar.disabled = !hay;
    mh.solo.disabled = !hay;
    mh.vaciar.disabled = !hay;
    mh.solo.setAttribute('aria-pressed', estado.solo ? 'true' : 'false');
    renderResumen();
  }

  function actualizar() {
    renderMias();
    aplicarFiltros();
    escribirURL();
  }

  function avisar(texto) { mh.msg.textContent = texto; }

  function anadir(id) {
    if (!porId[id] || estado.mias.indexOf(id) !== -1) return false;
    estado.mias.push(id);
    actualizar();
    return true;
  }

  function quitar(id) {
    var i = estado.mias.indexOf(id);
    if (i === -1) return;
    estado.mias.splice(i, 1);
    actualizar();
  }

  function buscarPorTexto(texto) {
    var t = norm(texto);
    if (!t) return { tipo: 'vacio' };
    var exactas = datos.filter(function (p) {
      return p.id === t || norm(p.nombre) === t || p.alias.some(function (a) { return norm(a) === t; });
    });
    if (exactas.length === 1) return { tipo: 'ok', p: exactas[0] };
    var candidatas = exactas.length > 1 ? exactas : datos.filter(function (p) {
      return [p.nombre, p.nombre_completo].concat(p.alias).some(function (s) { return norm(s).indexOf(t) !== -1; });
    });
    if (candidatas.length === 1) return { tipo: 'ok', p: candidatas[0] };
    if (candidatas.length > 1) return { tipo: 'varias', lista: candidatas };
    return { tipo: 'ninguna' };
  }

  function copiarTexto(texto, alTerminar) {
    function respaldo() {
      var ta = document.createElement('textarea');
      ta.value = texto;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      alTerminar(ok);
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(texto).then(function () { alTerminar(true); }, respaldo);
    } else {
      respaldo();
    }
  }

  function limpiarFiltros() {
    estado.q = ''; estado.cat = ''; estado.dif = ''; estado.ver = ''; estado.demo = false; estado.solo = false;
    sincronizarControles();
    renderMias();
    aplicarFiltros();
    escribirURL();
  }

  // --- Eventos: filtros
  var temporizador = null;
  f.form.addEventListener('submit', function (e) { e.preventDefault(); });
  f.q.addEventListener('input', function () {
    clearTimeout(temporizador);
    temporizador = setTimeout(function () {
      estado.q = f.q.value;
      aplicarFiltros();
      escribirURL();
    }, 150);
  });
  [f.cat, f.dif, f.ver].forEach(function (s) {
    s.addEventListener('change', function () {
      estado.cat = f.cat.value; estado.dif = f.dif.value; estado.ver = f.ver.value;
      aplicarFiltros();
      escribirURL();
    });
  });
  f.demo.addEventListener('change', function () {
    estado.demo = f.demo.checked;
    aplicarFiltros();
    escribirURL();
  });
  f.limpiar.addEventListener('click', limpiarFiltros);

  // --- Eventos: mis herramientas
  mh.form.addEventListener('submit', function (e) {
    e.preventDefault();
    var r = buscarPorTexto(mh.input.value);
    if (r.tipo === 'vacio') {
      avisar('Escribe el nombre de una herramienta.');
    } else if (r.tipo === 'ok') {
      if (anadir(r.p.id)) avisar('Añadida: ' + r.p.nombre + '.');
      else avisar(r.p.nombre + ' ya estaba en tu lista.');
      mh.input.value = '';
    } else if (r.tipo === 'varias') {
      avisar('Hay varias coincidencias: ' + r.lista.slice(0, 8).map(function (p) { return p.nombre; }).join(', ') + '. Escribe el nombre exacto.');
    } else {
      avisar('No encontramos «' + mh.input.value.trim() + '» en el catálogo. Puedes proponerla en el repositorio.');
    }
  });
  mh.copiar.addEventListener('click', function () {
    var base = window.location.href.split(/[?#]/)[0];
    var enlace = base + '?h=' + estado.mias.join(',') + '#mis-herramientas';
    copiarTexto(enlace, function (ok) {
      avisar(ok ? 'Enlace copiado. Quien lo abra verá esta misma selección.' : 'No se pudo copiar. Copia esta dirección: ' + enlace);
    });
  });
  mh.solo.addEventListener('click', function () {
    estado.solo = !estado.solo && estado.mias.length > 0;
    mh.solo.setAttribute('aria-pressed', estado.solo ? 'true' : 'false');
    aplicarFiltros();
    escribirURL();
  });
  mh.vaciar.addEventListener('click', function () {
    estado.mias = [];
    actualizar();
    avisar('Selección vaciada.');
    mh.input.focus();
  });

  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!(t instanceof Element)) return;
    var boton = t.closest('.boton-mia');
    if (boton) {
      var id = boton.closest('.ficha').getAttribute('data-id');
      if (estado.mias.indexOf(id) === -1) {
        anadir(id);
        avisar('Añadida: ' + porId[id].nombre + '.');
      } else {
        quitar(id);
        avisar('Quitada: ' + porId[id].nombre + '.');
      }
      boton.focus();
      return;
    }
    var quitarBtn = t.closest('[data-quitar]');
    if (quitarBtn) {
      var idq = quitarBtn.getAttribute('data-quitar');
      quitar(idq);
      avisar('Quitada: ' + porId[idq].nombre + '.');
      mh.input.focus();
      return;
    }
    var enlace = t.closest('.ir-ficha');
    if (enlace) {
      var it = items.filter(function (x) { return x.p.id === enlace.getAttribute('data-id'); })[0];
      if (it && it.li.hidden) limpiarFiltros();
      return;
    }
    var copiar = t.closest('[data-copiar]');
    if (copiar) {
      var origen = document.getElementById(copiar.getAttribute('data-copiar'));
      if (!origen) return;
      copiarTexto(origen.textContent.trim(), function (ok) {
        copiar.textContent = ok ? 'Copiado' : 'No se pudo copiar';
        setTimeout(function () { copiar.textContent = 'Copiar texto'; }, 2000);
      });
    }
  });

  // --- Arranque
  leerURL();
  sincronizarControles();
  renderMias();
  aplicarFiltros();
})();
"""

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E"
           "%3Crect width='16' height='16' fill='%23ec4429'/%3E%3C/svg%3E")


def pagina(titulo: str, descripcion: str, canonica: str, cuerpo: str, script: str = "") -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#e9e1d9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#161310" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{esc(canonica)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="Executive Lab">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:url" content="{esc(canonica)}">
<link rel="icon" href="{FAVICON}">
<style>{CSS}</style>
</head>
<body>
{cuerpo}
{script}
</body>
</html>
"""


def pie(ultima: str, prefijo: str) -> str:
    return f"""<footer class="pie">
  <div class="envoltura">
    <p class="aviso"><strong>Información orientativa.</strong> Los planes, precios y MCP cambian cada mes: verifica en la fuente antes de decidir.</p>
    <p>Última verificación: <time datetime="{esc(ultima)}">{esc(fecha_larga(ultima))}</time>. Cada lunes se revisan automáticamente las diez fichas con la verificación más antigua.</p>
    <p>Repositorio: <a href="{esc(REPO_URL)}">github.com/Executive-Lab/conectores-pymes</a>. ¿Falta tu herramienta o ves un dato desactualizado? <a href="{esc(REPO_URL)}/issues">Avísanos</a> o propón el cambio con un pull request.</p>
    <p>Datos y guías bajo <a href="https://creativecommons.org/licenses/by/4.0/deed.es">CC BY 4.0</a>; código bajo licencia MIT. Datos en bruto: <a href="{prefijo}catalogo.json">catalogo.json</a> · <a href="{prefijo}esquema.json">esquema.json</a>. Un proyecto de Executive Lab.</p>
  </div>
</footer>"""


# --------------------------------------------------------------------------
# Fichas
# --------------------------------------------------------------------------

def bloque(titulo: str, contenido: str) -> str:
    return f'<div class="bloque"><h5>{esc(titulo)}</h5>{contenido}</div>'


def parrafo(texto: str) -> str:
    return f"<p>{enlazar(texto)}</p>"


def objeto_o_texto(valor) -> str:
    if isinstance(valor, dict):
        filas = "".join(
            f"<dt>{esc(ETIQUETAS_OBJETO.get(k, k.replace('_', ' ').capitalize()))}</dt><dd>{enlazar(str(v))}</dd>"
            for k, v in valor.items()
        )
        return f"<dl>{filas}</dl>"
    return parrafo(str(valor))


def lista(valores: list[str], ordenada: bool = False) -> str:
    etiqueta = "ol" if ordenada else "ul"
    return f"<{etiqueta}>" + "".join(f"<li>{enlazar(v)}</li>" for v in valores) + f"</{etiqueta}>"


def fuentes_html(fuentes: list[str]) -> str:
    items = []
    for f in fuentes:
        m = RE_URL.match(f)
        if not m:
            items.append(f"<li>{esc(f)}</li>")
            continue
        url, cola = _partir_url(m.group(0))
        nota = (cola + f[m.end():]).strip()
        nota_html = f" <span>{esc(nota)}</span>" if nota else ""
        items.append(f'<li><a href="{esc(url)}">{esc(url_corta(url))}</a>{nota_html}</li>')
    return '<ol class="fuentes">' + "".join(items) + "</ol>"


def insignia(dificultad: str) -> str:
    emoji, clase = DIFICULTAD[dificultad]
    return (f'<span class="insignia dif-{clase}"><span aria-hidden="true">{emoji}</span> '
            f'<span class="sr-only">Dificultad: </span>{esc(dificultad)}</span>')


def ficha(p: dict, d: dict) -> str:
    pid = p["id"]
    buscar = " ".join([p["nombre"], p["nombre_completo"], pid, *p["alias"]])
    veredicto = d["veredicto_corto"]
    api = p["api"]
    mig = p["migracion"]

    api_html = (
        "<dl>"
        f"<dt>¿Existe?</dt><dd>{esc(API_ETIQUETA.get(api['existe'], api['existe']))}</dd>"
        f"<dt>Estilo</dt><dd>{enlazar(api['estilo'])}</dd>"
        f"<dt>Autenticación</dt><dd>{enlazar(api['auth'])}</dd>"
        f"<dt>Requisitos</dt><dd>{enlazar(api['requisitos'])}</dd>"
        f"<dt>Documentación</dt><dd>{enlazar(api['docs_url'])}</dd>"
        "</dl>"
    )
    mig_partes = [f"<dt>Veredicto</dt><dd>{esc(mig['veredicto'])}</dd>"]
    if mig.get("cuando_migrar"):
        mig_partes.append(f"<dt>Cuándo migrar</dt><dd>{enlazar(mig['cuando_migrar'])}</dd>")
    if mig.get("alternativas"):
        mig_partes.append("<dt>Alternativas</dt><dd>" + lista(mig["alternativas"]) + "</dd>")
    if mig.get("coste_esfuerzo_migracion"):
        mig_partes.append(f"<dt>Coste y esfuerzo</dt><dd>{enlazar(mig['coste_esfuerzo_migracion'])}</dd>")

    id_pedir = f"pedir-{pid}"
    columna_a = [
        bloque("API", api_html),
        bloque(f"MCP · {MCP_ETIQUETA.get(p['mcp']['estado'], p['mcp']['estado'])}", parrafo(p["mcp"]["detalle"])),
        bloque("Otras vías", lista(p["otras_vias"]) if p["otras_vias"] else "<p>No hay.</p>"),
        bloque("RPA", parrafo(p["rpa"])),
        bloque("Permisos acotados", parrafo(p["permisos_acotados"])),
    ]
    columna_b = [
        bloque(
            "Qué pedir al informático",
            f'<p class="pedir" id="{esc(id_pedir)}">{enlazar(p["pedir_al_informatico"])}</p>'
            f'<button type="button" class="boton boton-peq" data-copiar="{esc(id_pedir)}" data-requiere-js hidden>Copiar texto</button>',
        ),
        bloque("Demo gratis", objeto_o_texto(p["demo_gratis"])),
        bloque("Coste", objeto_o_texto(p["coste_demo"])),
        bloque("Migración", "<dl>" + "".join(mig_partes) + "</dl>"),
    ]
    if p.get("verifactu"):
        columna_b.append(bloque("Verifactu", parrafo(p["verifactu"])))
    columna_b.append(bloque("Fuentes", fuentes_html(p["fuentes"])))

    tercero = ('<span class="marca-tercero">Pide informático o distribuidor</span>'
               if d["pide_informatico"] else "")

    return f"""<li><article class="ficha" id="p-{esc(pid)}" data-id="{esc(pid)}" data-buscar="{esc(buscar)}" aria-labelledby="t-{esc(pid)}">
  <div class="ficha-cab">
    <div><h4 class="ficha-nombre" id="t-{esc(pid)}">{esc(p['nombre'])}</h4><p class="ficha-tipo">{esc(p['tipo'])}</p></div>
    {insignia(p['dificultad'])}
  </div>
  {tercero}
  <dl class="claves">
    <dt>Vía principal</dt><dd>{esc(d['via_principal'])}</dd>
    <dt>MCP</dt><dd>{esc(MCP_ETIQUETA.get(p['mcp']['estado'], p['mcp']['estado']))}</dd>
    <dt>Demo</dt><dd>{esc(p['demo_resumen'])}</dd>
    <dt>Coste</dt><dd>{esc(p['coste_resumen'])}</dd>
    <dt>Veredicto</dt><dd><span class="v-{veredicto}">{esc(VEREDICTO_ETIQUETA[veredicto])}</span></dd>
  </dl>
  <div class="acciones-ficha" data-requiere-js hidden>
    <button type="button" class="boton boton-peq boton-mia">Añadir a mis herramientas</button>
  </div>
  <details class="detalle-ficha">
    <summary>Ver detalle<span class="sr-only"> de {esc(p['nombre'])}</span></summary>
    <div class="detalle">
      <div>{''.join(columna_a)}</div>
      <div>{''.join(columna_b)}</div>
      <p class="meta">{esc(p['nombre_completo'])} · Confianza de la información: <strong>{esc(p['confianza'])}</strong> · Verificado el <time datetime="{esc(p['verificado_el'])}">{esc(fecha_larga(p['verificado_el']))}</time></p>
    </div>
  </details>
</article></li>"""


def seccion_categoria(cat: dict, plataformas: list[dict], deriv: dict) -> str:
    partes = [f"<h4>Hallazgos</h4>{lista(cat['hallazgos'])}"]
    if cat.get("normativa"):
        partes.append(f'<h4>Normativa</h4><p class="normativa">{enlazar(cat["normativa"])}</p>')
    if cat.get("asistentes_ia"):
        partes.append(f"<h4>Asistentes de IA</h4>{lista(cat['asistentes_ia'])}")
    extra = " y normativa" if cat.get("normativa") else ""
    fichas = "\n".join(ficha(p, deriv[p["id"]]) for p in plataformas)
    n = len(plataformas)
    return f"""<section class="categoria" id="cat-{esc(cat['id'])}" aria-labelledby="ct-{esc(cat['id'])}">
  <h3 class="categoria-titulo" id="ct-{esc(cat['id'])}"><span>{esc(cat['nombre'])}</span> <span class="cat-recuento">{n} herramientas</span></h3>
  <details class="hallazgos">
    <summary>Lo que hemos aprendido en esta categoría: hallazgos{extra}</summary>
    {''.join(partes)}
    <p class="meta">Verificado el <time datetime="{esc(cat['verificado_el'])}">{esc(fecha_larga(cat['verificado_el']))}</time></p>
  </details>
  <ul class="rejilla">
{fichas}
  </ul>
</section>"""


# --------------------------------------------------------------------------
# Páginas
# --------------------------------------------------------------------------

def construir_index(plataformas: list[dict], categorias: list[dict], deriv: dict,
                    guias: list[dict], base_url: str) -> str:
    por_cat: dict[str, list[dict]] = {}
    for p in plataformas:
        por_cat.setdefault(p["categoria"], []).append(p)
    clave_nombre = lambda p: sin_acentos(p["nombre"]).casefold()  # noqa: E731
    for lista_cat in por_cat.values():
        lista_cat.sort(key=clave_nombre)

    orden = [c for c in ORDEN_CATEGORIAS if any(cat["id"] == c for cat in categorias)]
    orden += sorted(cat["id"] for cat in categorias if cat["id"] not in orden)
    cats = {c["id"]: c for c in categorias}

    ultima = max(p["verificado_el"] for p in plataformas)
    total = len(plataformas)

    guias_html = "".join(
        f'<li><a class="guia-enlace" href="guias/{esc(g["slug"])}.html"><strong>{esc(g["titulo"])}</strong>'
        f'<span>{esc(g["descripcion"])}</span></a></li>'
        for g in guias
    )
    opciones_cat = "".join(
        f'<option value="{esc(c)}">{esc(cats[c]["nombre"])} ({len(por_cat.get(c, []))})</option>' for c in orden
    )
    opciones_dif = "".join(
        f'<option value="{esc(k)}">{esc(k)}</option>' for k in DIFICULTAD
    )
    opciones_ver = "".join(
        f'<option value="{esc(k)}">{esc(v)}</option>' for k, v in VEREDICTO_ETIQUETA.items()
    )
    datalist = "".join(
        f'<option value="{esc(p["nombre"])}">{esc(", ".join(p["alias"]))}</option>'
        for p in sorted(plataformas, key=clave_nombre)
    )
    secciones = "\n".join(seccion_categoria(cats[c], por_cat.get(c, []), deriv) for c in orden)

    indice = [
        {
            "id": p["id"],
            "nombre": p["nombre"],
            "nombre_completo": p["nombre_completo"],
            "alias": p["alias"],
            "categoria": p["categoria"],
            "dificultad": p["dificultad"],
            "veredicto": deriv[p["id"]]["veredicto_corto"],
            "via": deriv[p["id"]]["via_principal"],
            "tercero": deriv[p["id"]]["pide_informatico"],
            "demo": deriv[p["id"]]["hay_demo_gratis"],
        }
        for p in plataformas
    ]
    indice_json = json.dumps(indice, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    cuerpo = f"""<a class="saltar" href="#catalogo">Saltar al catálogo</a>
<div class="franja" aria-hidden="true"></div>
<div class="barra"><div class="envoltura">
  <a class="marca" href="./">Executive Lab</a>
  <span class="barra-nota">Catálogo vivo · {total} herramientas · revisión semanal</span>
</div></div>
<header class="cabecera"><div class="envoltura">
  <p class="kicker">Conectar antes que copiar y pegar</p>
  <h1>Conectores para pymes</h1>
  <p class="entradilla">Cómo conectar las herramientas de tu pyme a un arnés de IA: qué vía usar (MCP, API, puente o RPA), con qué permisos, qué pedir al informático y cuándo compensa migrar.</p>
  <p class="para-quien">Para dueños de pymes y alumnos de Executive Lab. Cada ficha resume lo que hemos verificado en fuentes primarias, con enlaces para comprobarlo. Empieza por las guías si es la primera vez.</p>
  <h2 class="guias-titulo">Guías</h2>
  <ul class="guias">{guias_html}</ul>
</div></header>
<main>
<section class="seccion" id="mis-herramientas" aria-labelledby="mh-titulo" data-requiere-js hidden><div class="envoltura">
  <h2 class="seccion-titulo" id="mh-titulo"><span class="num">01</span> Mis herramientas</h2>
  <p class="intro">Elige las herramientas que usa tu empresa y verás de un vistazo cuáles son fáciles de conectar, cuáles necesitan a tu informático o distribuidor y cuáles conviene valorar cambiar. La selección se guarda en la dirección de la página: puedes copiar el enlace y compartirlo.</p>
  <form class="mh-form" id="mh-form" autocomplete="off">
    <div class="campo">
      <label for="mh-buscar">Añadir una herramienta</label>
      <input type="text" id="mh-buscar" list="mh-lista" placeholder="Ej.: Holded, Outlook, Sage 50…" aria-describedby="mh-ayuda">
      <datalist id="mh-lista">{datalist}</datalist>
    </div>
    <button type="submit" class="boton boton-primario">Añadir</button>
  </form>
  <p class="sr-only" id="mh-ayuda">Escribe el nombre o un alias y pulsa Intro. También puedes usar el botón «Añadir a mis herramientas» de cada ficha.</p>
  <p class="mensaje" id="mh-mensaje" role="status" aria-live="polite"></p>
  <ul class="chips" id="mh-chips" aria-label="Herramientas elegidas"></ul>
  <div class="mh-acciones">
    <button type="button" class="boton boton-peq" id="mh-copiar">Copiar enlace para compartir</button>
    <button type="button" class="boton boton-peq" id="mh-solo" aria-pressed="false">Ver solo mis herramientas en el catálogo</button>
    <button type="button" class="boton boton-peq" id="mh-vaciar">Vaciar selección</button>
  </div>
  <div id="mh-resumen"></div>
</div></section>
<section class="seccion" id="catalogo" aria-labelledby="cat-titulo" tabindex="-1"><div class="envoltura">
  <h2 class="seccion-titulo" id="cat-titulo"><span class="num">02</span> Catálogo</h2>
  <p class="intro">{total} herramientas en {len(orden)} categorías. Despliega una ficha para ver la API, el MCP, los permisos, la demo, el coste, la migración y las fuentes.</p>
  <noscript><p class="intro">Sin JavaScript no funcionan el buscador, los filtros ni «Mis herramientas», pero puedes consultar todas las fichas.</p></noscript>
  <form class="filtros" id="filtros" role="search" aria-label="Filtrar el catálogo" data-requiere-js hidden>
    <div class="campo">
      <label for="f-q">Buscar por nombre o alias</label>
      <input type="search" id="f-q" placeholder="Ej.: ContaPlus, Murano, Gmail…">
    </div>
    <div class="campo">
      <label for="f-cat">Categoría</label>
      <select id="f-cat"><option value="">Todas</option>{opciones_cat}</select>
    </div>
    <div class="campo">
      <label for="f-dif">Dificultad</label>
      <select id="f-dif"><option value="">Todas</option>{opciones_dif}</select>
    </div>
    <div class="campo">
      <label for="f-ver">Veredicto</label>
      <select id="f-ver"><option value="">Todos</option>{opciones_ver}</select>
    </div>
    <div class="filtros-fila">
      <label class="check" for="f-demo"><input type="checkbox" id="f-demo"> Solo con demo gratis</label>
      <button type="button" class="boton boton-peq" id="f-limpiar">Limpiar filtros</button>
    </div>
  </form>
  <p class="recuento" id="recuento" role="status" aria-live="polite">Mostrando las {total} herramientas.</p>
  <details class="leyenda">
    <summary>Cómo leer las fichas</summary>
    <dl>
      <dt>Dificultad</dt><dd><span aria-hidden="true">🟢</span> Fácil, <span aria-hidden="true">🟡</span> Media, <span aria-hidden="true">🟠</span> Difícil y <span aria-hidden="true">🔴</span> Muy difícil: lo que cuesta hoy conectarla con permisos acotados, según la investigación de cada ficha.</dd>
      <dt>Vía principal</dt><dd>«RPA» si es muy difícil; si no, «MCP oficial» si el fabricante lo publica; «API» si tiene API (con «+ MCP comunitario» si existe uno); «API limitada / puente» si la API es parcial; «Puente (export / BD)» si basta una exportación o una base de datos de solo lectura; y si no, «RPA o export».</dd>
      <dt>MCP</dt><dd>Oficial (del fabricante), comunitario (de terceros: úsalo solo en lectura) o no hay.</dd>
      <dt>Demo</dt><dd>Cómo probarla sin pagar: gratis permanente, prueba de N días, sandbox o cuenta de desarrollador, evaluación bajo petición o no hay.</dd>
      <dt>Veredicto</dt><dd>Conectar tal cual; conectar con puente (exportación, base de datos o partner); o valorar migración (conectarla cuesta tanto que puede compensar cambiar). Lee la guía <a href="guias/conectar-o-migrar.html">¿Conectar o migrar?</a>.</dd>
      <dt>Pide a otra persona</dt><dd>Programa instalado (escritorio u on-premise), dificultad «Difícil», el acceso lo da un distribuidor, partner, gestoría, comercial, franquicia, banco o proveedor, o hace falta el administrador de Microsoft 365 o Google Workspace (consentimiento de la app).</dd>
      <dt>Confianza</dt><dd>Alta, media o baja según la calidad de las fuentes. Lo que no se pudo confirmar aparece como «no verificado».</dd>
    </dl>
  </details>
{secciones}
  <p class="sin-resultados" id="sin-resultados" hidden>No hay herramientas con esos filtros. Prueba con otro nombre o pulsa «Limpiar filtros».</p>
</div></section>
</main>
{pie(ultima, "")}"""

    script = (f'<script type="application/json" id="indice">{indice_json}</script>\n'
              f"<script>{JS}</script>")
    descripcion = ("Catálogo vivo para conectar las herramientas de una pyme a un arnés de IA: "
                   "MCP, API, permisos, demo, coste y cuándo migrar. Por Executive Lab.")
    return pagina("Conectores para pymes · Executive Lab", descripcion, base_url, cuerpo, script)


def cargar_guias(dir_guias: Path) -> list[dict]:
    guias = []
    orden = list(GUIAS)
    for ruta in sorted(dir_guias.glob("*.md"), key=lambda r: (orden.index(r.stem) if r.stem in orden else 99, r.stem)):
        texto = quitar_frontmatter(ruta.read_text(encoding="utf-8"))
        m = re.search(r"^#\s+(.+)$", texto, re.M)
        titulo = m.group(1).strip() if m else ruta.stem.replace("-", " ").capitalize()
        descripcion = GUIAS.get(ruta.stem)
        if not descripcion:
            parrafo_1 = next((b.strip() for b in texto.split("\n\n") if b.strip() and not b.lstrip().startswith(("#", ">"))), "")
            descripcion = re.sub(r"[*_`\[\]]", "", parrafo_1)[:180]
        guias.append({"slug": ruta.stem, "titulo": titulo, "descripcion": descripcion, "texto": texto})
    return guias


def construir_guia(guia: dict, guias: list[dict], ultima: str, base_url: str) -> str:
    def reescribir(url: str) -> str:
        if url.startswith(base_url):
            resto = url[len(base_url):]
            return "../" + (resto if resto else "index.html")
        m = re.match(r"^(?:\./)?([\w-]+)\.md(#.*)?$", url)
        if m:
            return f"{m.group(1)}.html{m.group(2) or ''}"
        return url

    contenido = Markdown(reescribir).convertir(guia["texto"])
    otras = "".join(
        f'<li><a href="{esc(g["slug"])}.html">{esc(g["titulo"])}</a></li>' for g in guias if g["slug"] != guia["slug"]
    )
    cuerpo = f"""<a class="saltar" href="#contenido">Saltar al contenido</a>
<div class="franja" aria-hidden="true"></div>
<div class="barra"><div class="envoltura">
  <a class="marca" href="../index.html">Executive Lab · Conectores para pymes</a>
  <span class="barra-nota">Guía</span>
</div></div>
<main class="envoltura guia" id="contenido">
  <a class="volver" href="../index.html">← Volver al catálogo</a>
  <article>
{contenido}
  </article>
  <nav class="otras-guias" aria-label="Otras guías">
    <h2 class="guias-titulo">Otras guías</h2>
    <ul>{otras}</ul>
  </nav>
</main>
{pie(ultima, "../")}"""
    return pagina(f"{guia['titulo']} · Conectores para pymes", guia["descripcion"],
                  f"{base_url}guias/{guia['slug']}.html", cuerpo)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Genera la web estática del catálogo Conectores para pymes.")
    parser.add_argument("--datos", type=Path, default=RAIZ / "datos", help="carpeta de datos (por defecto: datos/)")
    parser.add_argument("--guias", type=Path, default=RAIZ / "guias", help="carpeta de guías en markdown (por defecto: guias/)")
    parser.add_argument("--salida", type=Path, default=RAIZ / "sitio", help="carpeta de salida (por defecto: sitio/)")
    parser.add_argument("--base-url", default=BASE_URL, help=f"URL pública de la web (por defecto: {BASE_URL})")
    args = parser.parse_args(argv)
    base_url = args.base_url if args.base_url.endswith("/") else args.base_url + "/"

    errores, avisos, plataformas, categorias = validar.validar(args.datos)
    if errores:
        print(f"ERROR: los datos no son válidos ({len(errores)} problema(s)). Ejecuta scripts/validar.py.", file=sys.stderr)
        for e in errores[:20]:
            print(f"  - {e}", file=sys.stderr)
        return 1

    plataformas.sort(key=lambda p: p["id"])
    deriv = {p["id"]: derivados(p, base_url) for p in plataformas}
    guias = cargar_guias(args.guias)
    ultima = max(p["verificado_el"] for p in plataformas)

    salida = args.salida
    (salida / "guias").mkdir(parents=True, exist_ok=True)

    (salida / "index.html").write_text(
        construir_index(plataformas, categorias, deriv, guias, base_url), encoding="utf-8")

    vigentes = set()
    for g in guias:
        destino = salida / "guias" / f"{g['slug']}.html"
        destino.write_text(construir_guia(g, guias, ultima, base_url), encoding="utf-8")
        vigentes.add(destino.name)
    for viejo in (salida / "guias").glob("*.html"):
        if viejo.name not in vigentes:
            viejo.unlink()

    ids_por_cat: dict[str, list[str]] = {}
    for p in plataformas:
        ids_por_cat.setdefault(p["categoria"], []).append(p["id"])
    catalogo = {
        "nombre": "Conectores para pymes",
        "descripcion": "Cómo conectar las herramientas de una pyme a un arnés de IA.",
        "version_esquema": 1,
        "generado_el": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "ultima_verificacion": ultima,
        "verificacion_mas_antigua": min(p["verificado_el"] for p in plataformas),
        "url": base_url,
        "esquema": f"{base_url}esquema.json",
        "repositorio": REPO_URL,
        "licencia_datos": "CC BY 4.0 · https://creativecommons.org/licenses/by/4.0/deed.es",
        "aviso": AVISO,
        "total_plataformas": len(plataformas),
        "guias": [{"id": g["slug"], "titulo": g["titulo"], "url": f"{base_url}guias/{g['slug']}.html"} for g in guias],
        "categorias": [
            {**c, "plataformas": sorted(ids_por_cat.get(c["id"], []))}
            for c in sorted(categorias, key=lambda c: c["id"])
        ],
        "plataformas": [{**p, "derivados": deriv[p["id"]]} for p in plataformas],
    }
    (salida / "catalogo.json").write_text(json.dumps(catalogo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(args.datos / "esquema.json", salida / "esquema.json")

    for a in avisos:
        print(f"Aviso: {a}")
    print(f"OK: {len(plataformas)} fichas, {len(categorias)} categorías y {len(guias)} guías en {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
