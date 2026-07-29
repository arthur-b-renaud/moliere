#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
courbe_rythme - trace la longueur des phrases d'un texte, en SVG.

L'uniformite metrique est le marqueur le plus difficile a faire voir : il ne
se lit pas dans une phrase, il se lit dans la courbe. Ce script la trace.

Sans dependance. La sortie est un SVG lisible par GitHub et par tout
navigateur, avec des couleurs qui tiennent en theme clair comme en sombre.

    python3 scripts/courbe_rythme.py exemples/post-avant.md exemples/post-apres.md \\
        -o assets/rythme.svg --titres "avant" "apres"

Licence MIT. Voir LICENSE.
"""

from __future__ import annotations

import argparse
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moliere_lint import mots, phrases, prepare  # noqa: E402

# Palette lisible sur fond clair et sur fond sombre.
TEINTES = ["#d1495b", "#2a9d8f", "#e9a13b", "#5b6dc8"]
AXE = "#8b8b8b"


def longueurs(chemin):
    with open(chemin, encoding="utf-8") as f:
        prose, _ = prepare(f.read())
    return [len(mots(p)) for p in phrases(prose) if mots(p)]


def polyline(serie, x0, y0, largeur, hauteur, maxi, n_max):
    pas = largeur / max(n_max - 1, 1)
    pts = []
    for i, v in enumerate(serie):
        x = x0 + i * pas
        y = y0 + hauteur - (v / maxi) * hauteur
        pts.append(f"{x:.1f},{y:.1f}")
    return " ".join(pts)


def svg(series, titres, largeur=760, hauteur=300):
    marge_g, marge_d, marge_h, marge_b = 46, 16, 46, 62
    lg = largeur - marge_g - marge_d
    ht = hauteur - marge_h - marge_b
    maxi = max(max(s) for s in series if s) or 1
    maxi = int(maxi * 1.15) + 1
    n_max = max(len(s) for s in series)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" '
        f'width="{largeur}" height="{hauteur}" font-family="ui-sans-serif,system-ui,sans-serif">',
        '<style>'
        '.t{fill:#8b8b8b;font-size:11px}'
        '.l{fill:#8b8b8b;font-size:12px}'
        '.g{stroke:#8b8b8b;stroke-opacity:.22}'
        '</style>',
        f'<text x="{marge_g}" y="20" class="l" font-size="13" font-weight="600">'
        f'Longueur des phrases, mot par mot</text>',
        f'<text x="{marge_g}" y="36" class="t">'
        f'un texte marqué tient sur un plateau, un texte écrit respire</text>',
    ]

    # Grille horizontale
    for k in range(5):
        v = maxi * k / 4
        y = marge_h + ht - (v / maxi) * ht
        out.append(f'<line x1="{marge_g}" y1="{y:.1f}" x2="{marge_g + lg}" '
                   f'y2="{y:.1f}" class="g"/>')
        out.append(f'<text x="{marge_g - 8}" y="{y + 4:.1f}" class="t" '
                   f'text-anchor="end">{int(v)}</text>')

    # Series
    for i, (serie, titre) in enumerate(zip(series, titres)):
        if not serie:
            continue
        teinte = TEINTES[i % len(TEINTES)]
        pts = polyline(serie, marge_g, marge_h, lg, ht, maxi, n_max)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{teinte}" '
                   f'stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
        pas = lg / max(n_max - 1, 1)
        for j, v in enumerate(serie):
            x = marge_g + j * pas
            y = marge_h + ht - (v / maxi) * ht
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.8" fill="{teinte}"/>')

        moy = statistics.mean(serie)
        ec = statistics.pstdev(serie)
        ly = hauteur - 34 + i * 18
        out.append(f'<line x1="{marge_g}" y1="{ly - 4}" x2="{marge_g + 22}" '
                   f'y2="{ly - 4}" stroke="{teinte}" stroke-width="2.4"/>')
        out.append(f'<text x="{marge_g + 30}" y="{ly}" class="l">'
                   f'{titre} · moyenne {moy:.1f} mots · écart type {ec:.1f}</text>')

    out.append(f'<line x1="{marge_g}" y1="{marge_h + ht}" x2="{marge_g + lg}" '
               f'y2="{marge_h + ht}" stroke="{AXE}" stroke-opacity=".5"/>')
    out.append(f'<text x="{marge_g + lg}" y="{marge_h + ht + 18}" class="t" '
               f'text-anchor="end">rang de la phrase</text>')
    out.append("</svg>")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="courbe_rythme",
        description="Trace la longueur des phrases de un a quatre textes, en SVG.")
    p.add_argument("fichiers", nargs="+")
    p.add_argument("-o", "--sortie", default="-", help="fichier SVG, ou - pour stdout")
    p.add_argument("--titres", nargs="*", default=None, help="legende de chaque courbe")
    a = p.parse_args(argv)

    if len(a.fichiers) > 4:
        print("quatre textes au maximum", file=sys.stderr)
        return 2

    series = [longueurs(f) for f in a.fichiers]
    titres = a.titres or [os.path.basename(f) for f in a.fichiers]
    if len(titres) != len(series):
        titres = (titres + [os.path.basename(f) for f in a.fichiers])[:len(series)]

    image = svg(series, titres)
    if a.sortie == "-":
        print(image)
    else:
        os.makedirs(os.path.dirname(a.sortie) or ".", exist_ok=True)
        with open(a.sortie, "w", encoding="utf-8") as f:
            f.write(image + "\n")
        for f_, s in zip(a.fichiers, series):
            print(f"{f_} : {len(s)} phrases, moyenne {statistics.mean(s):.1f}, "
                  f"ecart type {statistics.pstdev(s):.1f}")
        print(f"ecrit : {a.sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
