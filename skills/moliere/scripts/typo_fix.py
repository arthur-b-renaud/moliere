#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
typo_fix - correction typographique mecanique et reversible.

Ce script ne touche jamais au style. Il ne corrige que ce qui se corrige
sans jugement : guillemets, ordinaux, tirets en incise, espaces insecables.
Le style reste un choix humain, et c'est pourquoi il est separe du linter.

Par defaut le script n'ecrit rien : il montre le diff. Ajouter --ecrire.

    python3 scripts/typo_fix.py texte.md
    python3 scripts/typo_fix.py skills/ --insecables --ecrire

Les blocs de code, les commentaires HTML, le frontmatter et les fichiers
declares « contre-exemples » sont laisses intacts.

Licence MIT. Voir LICENSE.
"""

from __future__ import annotations

import argparse
import difflib
import os
import re
import sys

VERSION = "1.0.0"

NBSP = " "        # espace insecable
FINE = " "        # espace fine insecable

RE_PROTEGE = re.compile(
    r"(?P<bloc>^```.*?^```|^~~~.*?^~~~)"      # blocs de code clotures
    r"|(?P<yaml>\A---\n.*?\n---\n)"           # frontmatter
    r"|(?P<commentaire><!--.*?-->)"           # commentaires HTML
    r"|(?P<balise><[a-zA-Z/][^>\n]*>)"        # balises HTML et leurs attributs
    r"|(?P<inline>`[^`\n]*`)"                 # code en ligne
    r"|(?P<lien>https?://\S+)",               # URL
    re.S | re.M)


def segments(texte: str):
    """Decoupe le texte en (protege: bool, morceau)."""
    out, pos = [], 0
    for m in RE_PROTEGE.finditer(texte):
        if m.start() > pos:
            out.append((False, texte[pos:m.start()]))
        out.append((True, m.group(0)))
        pos = m.end()
    out.append((False, texte[pos:]))
    return out


# --------------------------------------------------------------------------
# Corrections
# --------------------------------------------------------------------------


def guillemets(t: str) -> str:
    """Guillemets anglais droits vers chevrons francais, avec insecables."""
    return re.sub(r'"([^"\n]{1,400}?)"',
                  lambda m: "«" + NBSP + m.group(1).strip() + NBSP + "»", t)


def ordinaux(t: str) -> str:
    t = re.sub(r"\b1(?:ere|ère)\b", "1re", t)
    t = re.sub(r"\b1(?:er)\b", "1er", t)
    return re.sub(r"\b(\d+)(?:eme|ème)\b", r"\1e", t)


def tirets(t: str) -> str:
    """Tiret cadratin ou demi-cadratin en incise vers la virgule.

    Uniquement quand le tiret est entoure d'espaces : le tiret colle
    (intervalle, mot compose) est laisse tel quel, faute de savoir.
    """
    t = re.sub(r"\s+[—–]\s+([^,\n]{0,200}?)\s+[—–]\s+", r", \1, ", t)
    t = re.sub(r"\s+[—–]\s+", ", ", t)
    return t


def insecables(t: str) -> str:
    """Espaces insecables devant la ponctuation double et dans les unites."""
    t = re.sub(r"(?<=\S)[ \t]+:(?=\s)", NBSP + ":", t)
    t = re.sub(r"(?<=\S)[ \t]*([;!?])(?=\s|$)", FINE + r"\1", t)
    t = re.sub(r"(?<=\d)[ \t]+(%|€|\$|km|kg|h|m²)\b", NBSP + r"\1", t)
    t = re.sub(r"\b(M|Mme|Mlle|Dr|Pr)\.[ \t]+(?=[A-ZÀ-Ý])", r"\1." + NBSP, t)
    return t


def espaces_parasites(t: str) -> str:
    """Espace avant le point ou la virgule, et double espace."""
    t = re.sub(r"[ \t]+([.,])(?=\s|$)", r"\1", t)
    t = re.sub(r"(?<=\S)[ \t]{2,}(?=\S)", " ", t)
    return t


CORRECTIONS = [
    ("guillemets", "guillemets francais", guillemets),
    ("ordinaux", "ordinaux (2eme vers 2e)", ordinaux),
    ("tirets", "tirets en incise vers virgule", tirets),
    ("espaces", "espaces parasites", espaces_parasites),
]

OPTIONNELLES = [
    ("insecables", "espaces insecables", insecables),
]


def corriger(source: str, actives) -> str:
    sortie = []
    for protege, morceau in segments(source):
        if protege:
            sortie.append(morceau)
            continue
        for _, _, fonction in actives:
            morceau = fonction(morceau)
        sortie.append(morceau)
    return "".join(sortie)


# --------------------------------------------------------------------------


def est_contre_exemple(source: str) -> bool:
    return bool(re.search(r"<!--\s*moliere-lint:\s*contre-exemples\s*-->",
                          source[:2000]))


def diff(avant: str, apres: str, chemin: str) -> str:
    return "".join(difflib.unified_diff(
        avant.splitlines(keepends=True), apres.splitlines(keepends=True),
        fromfile=chemin, tofile=chemin + " (corrige)", n=1))


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="typo_fix",
        description="Correction typographique mecanique. Ne touche jamais au style.")
    p.add_argument("fichiers", nargs="+")
    p.add_argument("--ecrire", action="store_true",
                   help="applique les corrections ; sans ce drapeau, montre le diff")
    p.add_argument("--insecables", action="store_true",
                   help="insere aussi les espaces insecables")
    p.add_argument("--sans", default="", metavar="LISTE",
                   help="corrections a desactiver, separees par des virgules")
    p.add_argument("--forcer", action="store_true",
                   help="traite aussi les fichiers declares contre-exemples")
    p.add_argument("--version", action="version", version=f"typo_fix {VERSION}")
    a = p.parse_args(argv)

    exclues = {s.strip() for s in a.sans.split(",") if s.strip()}
    actives = [c for c in CORRECTIONS if c[0] not in exclues]
    if a.insecables:
        actives += [c for c in OPTIONNELLES if c[0] not in exclues]

    chemins = []
    for f in a.fichiers:
        if os.path.isdir(f):
            for racine, _, noms in os.walk(f):
                chemins += [os.path.join(racine, n) for n in sorted(noms)
                            if n.endswith((".md", ".txt"))]
        else:
            chemins.append(f)

    modifies = 0
    for chemin in chemins:
        with open(chemin, encoding="utf-8") as fh:
            source = fh.read()
        if est_contre_exemple(source) and not a.forcer:
            print(f"  ignore (contre-exemples) : {chemin}")
            continue
        resultat = corriger(source, actives)
        if resultat == source:
            continue
        modifies += 1
        if a.ecrire:
            with open(chemin, "w", encoding="utf-8") as fh:
                fh.write(resultat)
            print(f"  corrige : {chemin}")
        else:
            sys.stdout.write(diff(source, resultat, chemin))

    if not a.ecrire and modifies:
        print(f"\n{modifies} fichier(s) a corriger. Relancer avec --ecrire.")
    elif not modifies:
        print("rien a corriger")
    return 0


if __name__ == "__main__":
    sys.exit(main())
