#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
moliere_lint - controle mecanique d'un texte francais.

Ce script fait ce qu'un modele de langue fait mal : compter.
Il ne juge pas le style, il mesure ce qui se mesure.

Aucune dependance. Python 3.8 et plus.

    python3 moliere_lint.py texte.md --profil document
    python3 moliere_lint.py texte.md --profil post
    python3 moliere_lint.py slides.md --profil presentation
    python3 moliere_lint.py exemples/*.md --json

Licence MIT. Voir LICENSE.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

VERSION = "1.0.0"

# --------------------------------------------------------------------------
# Severites et ponderations
# --------------------------------------------------------------------------

BLOQUANT, DEFAUT, ALERTE, INFO = "bloquant", "defaut", "alerte", "info"
POIDS = {BLOQUANT: 12, DEFAUT: 6, ALERTE: 3, INFO: 0}
ORDRE = {BLOQUANT: 0, DEFAUT: 1, ALERTE: 2, INFO: 3}

# --------------------------------------------------------------------------
# Profils
# --------------------------------------------------------------------------

# Trois supports, qui correspondent aux trois cas d'usage : un document de
# plusieurs pages, une publication courte, un jeu de slides.
#
# Une slide n'a ni attaque, ni chute, ni rythme : ces trois controles sont
# desactives en profil presentation, sans quoi tout le fichier sortirait en
# faute. En echange, elle porte deux contraintes que les autres n'ont pas,
# la longueur des puces et la ponctuation finale.

PROFILS = {
    "document": {
        "attaque_max": None,
        "coupure": None,
        "longueur_max": None,
        "staccato_permis": 0,
        "phrase_un_mot_permise": 0,
        "hashtags_max": 0,
        "exclamations_max": 0,
        "gras_interdit": False,
        "adresse_lecteur": False,
        "controle_attaque": False,
        "controle_chute": True,
        "controle_rythme": True,
        "puce_max_mots": None,
        "puce_sans_point_final": False,
    },
    "post": {
        "attaque_max": 150,
        "coupure": 140,
        "longueur_max": 3000,
        "staccato_permis": 1,
        "phrase_un_mot_permise": 1,
        "hashtags_max": 3,
        "exclamations_max": 1,
        "gras_interdit": True,
        "adresse_lecteur": True,
        "controle_attaque": True,
        "controle_chute": True,
        "controle_rythme": True,
        "puce_max_mots": None,
        "puce_sans_point_final": False,
    },
    "presentation": {
        "attaque_max": None,
        "coupure": None,
        "longueur_max": None,
        "staccato_permis": None,
        "phrase_un_mot_permise": None,
        "hashtags_max": 0,
        "exclamations_max": 0,
        "gras_interdit": False,
        "adresse_lecteur": False,
        "controle_attaque": False,
        "controle_chute": False,
        "controle_rythme": False,
        "puce_max_mots": 12,
        "puce_sans_point_final": True,
    },
}

# --------------------------------------------------------------------------
# Listes noires, tirees de references/marqueurs.md
# --------------------------------------------------------------------------

ADJECTIFS = """crucial cruciale cruciaux essentiel essentielle essentiels
fondamental fondamentale fondamentaux incontournable incontournables majeur
majeure majeurs veritable veritables robuste robustes puissant puissante
captivant captivante unique uniques strategique strategiques""".split()

VERBES = """permettre permet permettent permettant permis garantir garantit
garantissant assurer assure assurant offrir offre offrant favoriser favorise
optimiser optimise transformer transforme revolutionner accompagner accompagne
accompagnant""".split()

SUBSTANTIFS = """solution solutions dispositif dispositifs demarche demarches
ecosysteme ecosystemes levier leviers synergie synergies brique briques
verticale valeur-ajoutee expertise enjeu enjeux defi defis opportunite
opportunites""".split()

LOCUTIONS = [
    "il est important de noter",
    "il convient de souligner",
    "il convient de noter",
    "force est de constater",
    "dans un monde ou",
    "a l'ere de",
    "plus que jamais",
    "a l'heure ou",
    "loin d'etre anecdotique",
    "ce n'est pas un detail",
    "l'enjeu est double",
    "en somme",
    "en conclusion",
    "pour aller plus loin",
    "vous l'aurez compris",
    "n'est plus une option",
    "une longueur d'avance",
    "changer la donne",
    "au coeur de",
    "a n'en pas douter",
]

ADVERBES_LIAISON = ["par ailleurs", "de plus", "en outre", "neanmoins", "notamment"]

# Ne figurent ici que les constructions fautives ou imprecises en francais,
# jamais les emprunts de vocabulaire. « digital » et « impacter » en ont ete
# retires : les proscrire est une position de puriste que l'usage de 2026 ne
# soutient plus, et le skill ne fait pas la chasse aux anglicismes. Le critere
# d'entree dans cette liste : le mot francais existe, il est plus precis, et
# personne ne dit l'anglais faute de mieux.

CALQUES = {
    "adresser": "traiter, prendre en charge, s'attaquer a",
    "adressons": "traitons",
    "initier": "lancer, engager, ouvrir",
    "initie": "lance",
    "delivrer": "livrer, produire, tenir",
    "supporter un format": "prendre en charge, admettre",
    "supporte le format": "prend en charge le format",
    "investiguer": "enqueter sur, examiner",
    "basee": "fondee, appuyee",
    "basees": "fondees",
    "base sur": "fonde sur, a partir de",
    "en termes de": "en matiere de, sur le plan de",
    "au niveau de": "dans, pour, en matiere de",
    "faire sens": "avoir du sens",
    "sur base de": "sur la base de, d'apres",
    "en charge de": "charge de",
    "laissez-moi savoir": "dites-moi",
    "je suis excite": "je me rejouis de",
}

ABREVIATIONS_JARGON = ["eval", "evals", "prop", "props", "presen", "dispo",
                       "dispos", "config", "configs", "spec", "specs", "archi"]

# Mots en -ant qui ne sont pas des participes presents.
NON_PARTICIPES = set("""avant devant pendant cependant maintenant pourtant
autant tant quant partant instant restant important importante importants
interessant interessante courant courantes montant montants gant gants
diamant diamants elephant enfant enfants geant geants dirigeant dirigeants
commercant commercants habitant habitants participant participants
etudiant etudiants soignant soignants consultant consultants assistant
assistants occupant occupants representant representants fabricant
fabricants marchant vivant vivants savant savants puissant puissante
brillant brillante suivant suivante suivants dorenavant nonobstant
neanmoins pesant plaisant""".split())

# Mots frequents exclus du controle de repetition rapprochee.
MOTS_COURANTS = set("""lesquelles lesquels auxquelles auxquels desquelles
pourquoi comment lorsque puisque quelques plusieurs certaines certains
egalement seulement notamment toutefois cependant pourtant ensuite
d'abord aujourd'hui maintenant beaucoup souvent toujours jamais parfois
entreprise entreprises personnes personne quelqu'un""".split())

MOIS = """janvier fevrier mars avril mai juin juillet aout septembre octobre
novembre decembre""".split()

# « un » et « une » sont exclus : ce sont des articles avant d'etre des nombres.
NOMBRES_LETTRES = """deux trois quatre cinq six sept huit neuf dix onze
douze treize quatorze quinze seize vingt trente quarante cinquante soixante
cent cents mille million millions milliard milliards""".split()

# Suffixes qui font ressembler un mot a un adjectif.
SUFFIXES_ADJ = ("able", "ables", "ible", "ibles", "ive", "ives", "if", "ifs",
                "eux", "euse", "euses", "ique", "iques", "aire", "aires",
                "elle", "elles", "ant", "ante", "ants", "antes", "ent",
                "ente", "ents", "entes", "ide", "ides", "uste", "ustes",
                "ale", "ales", "aux", "iste", "istes", "ee", "ees", "e", "es")

# Caracteres Unicode de substitution (gras et italique fabriques).
RE_UNICODE_MATH = re.compile(r"[\U0001D400-\U0001D7FF]")
RE_EMOJI_PUCE = re.compile(
    r"^\s*[\U0001F300-\U0001FAFF←-➿⬀-⯿■-◿]", re.M)
RE_TIRET = re.compile(r"[—–]")
RE_ABREVIATION = re.compile(
    r"\b(?:M|MM|Mme|Mmes|Mlle|Dr|Pr|St|Ste|cf|etc|av|ap|ex|p|pp|fig|no|nos|art|vol|ed|J\.-C)\.",
    re.I)

# --------------------------------------------------------------------------
# Normalisation et decoupage
# --------------------------------------------------------------------------


def sans_accents(texte: str) -> str:
    decompose = unicodedata.normalize("NFD", texte)
    return "".join(c for c in decompose if unicodedata.category(c) != "Mn")


def prepare(source: str):
    """Retire ce qui n'est pas de la prose. Renvoie (prose, drapeaux)."""
    drapeaux = {"contre_exemples": False}
    if re.search(r"<!--\s*moliere-lint:\s*contre-exemples\s*-->", source[:2000]):
        drapeaux["contre_exemples"] = True

    texte = source
    # Frontmatter YAML
    texte = re.sub(r"\A---\n.*?\n---\n", "", texte, flags=re.S)
    # Blocs de code clotures
    texte = re.sub(r"^```.*?^```", "", texte, flags=re.S | re.M)
    texte = re.sub(r"^~~~.*?^~~~", "", texte, flags=re.S | re.M)
    # Commentaires HTML
    texte = re.sub(r"<!--.*?-->", "", texte, flags=re.S)
    # Tableaux Markdown
    texte = re.sub(r"^\|.*$", "", texte, flags=re.M)
    # Titres Markdown
    texte = re.sub(r"^#{1,6}\s+.*$", "", texte, flags=re.M)
    # Code en ligne et liens
    texte = re.sub(r"`[^`]*`", "", texte)
    texte = re.sub(r"https?://\S+", "", texte)
    return texte, drapeaux


def paragraphes(prose: str):
    return [p.strip() for p in re.split(r"\n\s*\n", prose) if p.strip()]


def phrases(prose: str):
    """Decoupe en phrases, en protegeant abreviations et decimales."""
    tampon = RE_ABREVIATION.sub(lambda m: m.group(0).replace(".", "\x00"), prose)
    tampon = re.sub(r"(\d)([.,])(\d)",
                    lambda m: m.group(1) + "\x01" + m.group(3), tampon)
    morceaux = re.split(r"(?<=[.!?…])[\s\n]+", tampon)
    resultat = []
    for m in morceaux:
        m = m.replace("\x00", ".").replace("\x01", ",").strip()
        m = re.sub(r"^[\s*\-•·>#]+", "", m).strip()
        if len(m.split()) >= 1 and re.search(r"[A-Za-zÀ-ÿ]", m):
            resultat.append(m)
    return resultat


def mots(texte: str):
    return re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'’\-]*", texte)


# --------------------------------------------------------------------------
# Constat
# --------------------------------------------------------------------------


class Constat:
    __slots__ = ("severite", "regle", "message", "detail", "ligne")

    def __init__(self, severite, regle, message, detail="", ligne=None):
        self.severite = severite
        self.regle = regle
        self.message = message
        self.detail = detail
        self.ligne = ligne

    def dict(self):
        return {"severite": self.severite, "regle": self.regle,
                "message": self.message, "detail": self.detail,
                "ligne": self.ligne}


def ligne_de(source: str, position: int) -> int:
    return source.count("\n", 0, position) + 1


# --------------------------------------------------------------------------
# Controles typographiques (toujours actifs)
# --------------------------------------------------------------------------


def controles_typo(source, prose, profil, cfg):
    c = []

    # Les tirets des blocs de code et des commentaires ont deja ete retires.
    tirets = list(RE_TIRET.finditer(prose))
    if tirets:
        lignes = sorted({ligne_de(prose, m.start()) for m in tirets})
        c.append(Constat(DEFAUT, "tiret-cadratin",
                         f"{len(tirets)} tiret(s) cadratin ou demi-cadratin",
                         "lignes " + ", ".join(map(str, lignes[:8])) +
                         " · remplacer par virgule, deux-points, parenthese ou point",
                         lignes[0]))

    for m in RE_UNICODE_MATH.finditer(prose):
        c.append(Constat(BLOQUANT, "unicode-substitution",
                         "gras ou italique fabrique en caracteres mathematiques Unicode",
                         "casse les lecteurs d'ecran", ligne_de(prose, m.start())))
        break

    # Un numero de version n'est pas un decimal : Apache 2.0, Python 3.8,
    # SWE-bench 1.5. On les reconnait a ce qui les precede, un nom propre ou
    # le mot « version ». Sans cette exemption, tout texte technique francais
    # sort en bloquant, ce qui est le plus mauvais des faux positifs.
    RE_VERSION = re.compile(
        r"(?:[A-ZÀ-Þ][\w.+-]*|\bversion|\bv)\s*\d+[.]\d+(?:[.]\d+)*\b")
    versions = {m.end() for m in RE_VERSION.finditer(prose)}

    for m in re.finditer(r"\b\d+[.]\d+(?:[.]\d+)*\b", prose):
        if m.group(0).count(".") == 1 and m.end() not in versions:
            c.append(Constat(BLOQUANT, "point-decimal",
                             f"point decimal dans « {m.group(0)} »",
                             "le francais ecrit la virgule decimale",
                             ligne_de(prose, m.start())))
            break

    for m in re.finditer(r"\b\d+(?:eme|ème)\b", prose):
        c.append(Constat(DEFAUT, "ordinal",
                         f"ordinal fautif « {m.group(0)} »",
                         "ecrire 2e, 3e, 1er, 1re", ligne_de(prose, m.start())))
        break

    guillemets = len(re.findall(r'"', prose))
    if guillemets >= 2:
        c.append(Constat(ALERTE, "guillemets",
                         f"{guillemets} guillemet(s) anglais",
                         "employer les chevrons francais « »"))

    if RE_EMOJI_PUCE.search(prose):
        n = len(RE_EMOJI_PUCE.findall(prose))
        c.append(Constat(DEFAUT, "puce-emoji", f"{n} puce(s) a emoji",
                         "marqueur visuel du texte genere"))

    if cfg["gras_interdit"]:
        gras = re.findall(r"\*\*[^*\n]+\*\*|__[^_\n]+__", prose)
        if gras:
            c.append(Constat(DEFAUT, "gras",
                             f"{len(gras)} passage(s) en gras",
                             "LinkedIn ne rend pas le balisage : le texte affichera les asterisques"))

    if re.search(r"…|\.\.\.", prose):
        c.append(Constat(ALERTE, "points-suspension",
                         "points de suspension",
                         "a eviter dans un texte professionnel"))

    exclam = len(re.findall(r"!", prose))
    if exclam > cfg["exclamations_max"]:
        c.append(Constat(ALERTE, "exclamation",
                         f"{exclam} point(s) d'exclamation (maximum {cfg['exclamations_max']})"))

    return c


# --------------------------------------------------------------------------
# Controles de langue
# --------------------------------------------------------------------------


def controles_langue(prose, plat, profil, cfg):
    c = []
    ps = phrases(prose)
    ws = mots(prose)
    nb_mots = len(ws)

    # 1. Participe present en queue
    trouves = []
    for m in re.finditer(r",\s+([A-Za-zÀ-ÿ']{4,}ant)\b", prose):
        brut = m.group(1)
        if sans_accents(brut.lower()) in NON_PARTICIPES:
            continue
        trouves.append((brut, ligne_de(prose, m.start())))
    if trouves:
        c.append(Constat(BLOQUANT, "participe-present",
                         f"{len(trouves)} participe(s) present(s) en queue de phrase",
                         " · ".join(f"« , {b} »" for b, _ in trouves[:4]) +
                         " · couper la phrase ou coordonner avec « et »",
                         trouves[0][1]))

    # 2. Enumeration ternaire d'adjectifs
    for m in re.finditer(
            r"\b([a-zà-ÿ]{4,})\s*,\s+([a-zà-ÿ]{4,})\s+et\s+([a-zà-ÿ]{4,})\b", prose):
        triplet = [m.group(1), m.group(2), m.group(3)]
        if all(w.endswith(SUFFIXES_ADJ) for w in triplet):
            c.append(Constat(DEFAUT, "enumeration-ternaire",
                             "enumeration a trois adjectifs",
                             f"« {m.group(0)} » · un adjectif choisi vaut mieux que trois generiques",
                             ligne_de(prose, m.start())))
            break

    # 3. Rythme
    longueurs = [len(mots(p)) for p in ps]
    longueurs = [n for n in longueurs if n > 0]
    if cfg["controle_rythme"] and len(longueurs) >= 4:
        moy = statistics.mean(longueurs)
        ec = statistics.pstdev(longueurs)
        detail = f"moyenne {moy:.1f} mots · ecart type {ec:.1f}"
        if ec < 5.0:
            c.append(Constat(DEFAUT, "rythme-uniforme",
                             "longueurs de phrase trop uniformes",
                             detail + " · viser un ecart type superieur a 6"))
        else:
            c.append(Constat(INFO, "rythme", "rythme", detail))
        # Plateau : quatre phrases consecutives dans une fourchette de 4 mots
        for i in range(len(longueurs) - 3):
            fenetre = longueurs[i:i + 4]
            if max(fenetre) - min(fenetre) <= 4:
                c.append(Constat(ALERTE, "plateau-metrique",
                                 f"plateau metrique, phrases {i + 1} a {i + 4}",
                                 "longueurs " + ", ".join(map(str, fenetre))))
                break
        if moy > 30:
            c.append(Constat(ALERTE, "phrases-longues",
                             f"moyenne de {moy:.1f} mots par phrase",
                             "au-dela de 25, le lecteur reprend son souffle"))

    # 4. Attaque
    if cfg["controle_attaque"] and ps:
        attaque = ps[0]
        n = len(attaque)
        if n > cfg["attaque_max"]:
            c.append(Constat(ALERTE, "attaque-longue",
                             f"attaque de {n} caracteres (maximum {cfg['attaque_max']})",
                             f"coupee vers {cfg['coupure']} caracteres sur mobile", 1))
        else:
            c.append(Constat(INFO, "attaque", f"attaque : {n} caracteres", ""))
        depart = sans_accents(attaque.lower())
        for amorce in ("dans un monde ou", "a l'heure ou", "a l'ere de",
                       "depuis toujours", "de nos jours", "aujourd'hui plus que"):
            if depart.startswith(amorce):
                c.append(Constat(DEFAUT, "attaque-generale",
                                 "l'attaque ouvre sur une generalite",
                                 f"« {attaque[:60]}… » · donner un fait, pas un decor", 1))
                break
        if attaque.rstrip().endswith("?"):
            c.append(Constat(DEFAUT, "question-rhetorique",
                             "question rhetorique en ouverture",
                             "elle demande au lecteur le travail que le texte devait faire", 1))

    # 5. Chute
    if cfg["controle_chute"] and len(ps) >= 2:
        derniere, avant = len(mots(ps[-1])), len(mots(ps[-2]))
        if derniere > avant:
            c.append(Constat(ALERTE, "chute-longue",
                             f"la derniere phrase ({derniere} mots) est plus longue "
                             f"que l'avant-derniere ({avant} mots)",
                             "couper : la chute tombe mieux courte"))
        fin = sans_accents(ps[-1].lower())
        for amorce in ("en conclusion", "en somme", "pour conclure",
                       "retenez que", "en resume", "vous l'aurez compris"):
            if fin.startswith(amorce):
                c.append(Constat(DEFAUT, "chute-recapitulative",
                                 f"la chute commence par « {amorce} »",
                                 "une chute qui resume est une chute perdue"))
                break

    # 6. Ouvertures de paragraphe
    paras = plat
    ouvertures = []
    for p in paras:
        w = mots(p)
        ouvertures.append(sans_accents(w[0].lower()) if w else "")
    for i in range(1, len(ouvertures)):
        if ouvertures[i] and ouvertures[i] == ouvertures[i - 1]:
            c.append(Constat(ALERTE, "ouvertures-identiques",
                             f"paragraphes {i} et {i + 1} ouvrent sur le meme mot",
                             f"« {ouvertures[i]} » · alterner sujet-verbe, connecteur, incise, groupe nominal"))
            break

    # 7. Repetition rapprochee d'un mot saillant
    positions = {}
    for i, w in enumerate(ws):
        cle = sans_accents(w.lower())
        if len(cle) < 9 or cle in MOTS_COURANTS:
            continue
        if cle in positions and i - positions[cle] < 40:
            c.append(Constat(ALERTE, "repetition-rapprochee",
                             f"« {w} » revient apres {i - positions[cle]} mots",
                             "un mot saillant ne revient pas avant quarante mots"))
            break
        positions[cle] = i

    # 8. Densite de marqueurs lexicaux
    plat_txt = " " + sans_accents(prose.lower()) + " "
    hits = []
    for liste, etiquette in ((ADJECTIFS, "adjectif"), (VERBES, "verbe"),
                             (SUBSTANTIFS, "substantif")):
        for w in liste:
            if re.search(r"\b" + re.escape(w) + r"\b", plat_txt):
                hits.append(w)
    for loc in LOCUTIONS:
        if loc in plat_txt:
            hits.append(loc)
    if hits:
        pour300 = len(hits) * 300 / max(nb_mots, 1)
        sev = BLOQUANT if pour300 > 6 else DEFAUT if pour300 > 2 else ALERTE
        c.append(Constat(sev, "marqueurs-lexicaux",
                         f"{len(hits)} marqueur(s) lexicaux, soit {pour300:.1f} pour 300 mots (seuil 2)",
                         ", ".join(sorted(set(hits))[:12])))

    # 9. Adverbes de liaison
    for adv in ADVERBES_LIAISON:
        n = len(re.findall(r"\b" + re.escape(adv) + r"\b", plat_txt))
        if n > 1:
            c.append(Constat(DEFAUT, "adverbe-liaison",
                             f"« {adv} » employe {n} fois",
                             "un par texte au maximum"))

    # 10. Calques de l'anglais
    calques = []
    for mot, remede in CALQUES.items():
        if re.search(r"\b" + re.escape(mot) + r"\b", plat_txt):
            calques.append(f"{mot} → {remede}")
    if calques:
        c.append(Constat(DEFAUT, "calques",
                         f"{len(calques)} calque(s) de l'anglais",
                         " · ".join(calques[:6])))

    # 11. Abreviations de jargon
    for ab in ABREVIATIONS_JARGON:
        if re.search(r"\b" + re.escape(ab) + r"\b", plat_txt):
            c.append(Constat(DEFAUT, "abreviation-jargon",
                             f"abreviation de jargon « {ab} »", "ecrire le mot entier"))
            break

    # 12. Ancrage : chiffre, nombre ecrit, nom propre ou date
    a_chiffre = bool(re.search(r"\d", prose))
    a_nombre = any(sans_accents(w.lower()) in NOMBRES_LETTRES for w in ws)
    a_date = bool(re.search(r"\b(?:19|20)\d{2}\b", prose)) or \
        any(sans_accents(w.lower()) in MOIS for w in ws)
    propres = []
    debut_phrase = {ps_i.split()[0] if ps_i.split() else "" for ps_i in ps}
    for w in ws:
        if w[0].isupper() and w not in debut_phrase and len(w) > 2:
            propres.append(w)
    if not (a_chiffre or a_nombre or a_date or propres):
        c.append(Constat(BLOQUANT, "aucun-ancrage",
                         "zero chiffre, zero nom propre, zero date",
                         "le texte n'a rien dit de verifiable"))
    else:
        c.append(Constat(INFO, "ancrage", "ancrage",
                         f"chiffres : {'oui' if a_chiffre or a_nombre else 'non'} · "
                         f"dates : {'oui' if a_date else 'non'} · "
                         f"noms propres : {len(set(propres))}"))

    # 13. Sigles non developpes
    sigles = set(re.findall(r"\b[A-Z]{2,6}\b", prose))
    sigles = {s for s in sigles if s not in {"OK", "PDF", "URL"}}
    if len(sigles) > 3:
        c.append(Constat(ALERTE, "sigles",
                         f"{len(sigles)} sigles ({', '.join(sorted(sigles)[:6])})",
                         "trois non developpes au maximum"))

    # 14. Staccato et phrases d'un seul mot
    courtes = [i for i, n in enumerate(longueurs) if n <= 4]
    series, precedent = 0, -10
    for i in courtes:
        if i == precedent + 1:
            continue
        if i + 1 in courtes:
            series += 1
        precedent = i
    # En profil presentation, les deux seuils sont a None : une slide est faite
    # de fragments, la phrase breve y est la norme et non un tic.
    if cfg["staccato_permis"] is not None and series > cfg["staccato_permis"]:
        c.append(Constat(DEFAUT, "staccato",
                         f"{series} serie(s) de phrases courtes "
                         f"(maximum {cfg['staccato_permis']})",
                         "signature du copywriting anglo-saxon : le francais articule"))
    un_mot = sum(1 for n in longueurs if n == 1)
    if cfg["phrase_un_mot_permise"] is not None and un_mot > cfg["phrase_un_mot_permise"]:
        c.append(Constat(DEFAUT, "phrase-un-mot",
                         f"{un_mot} phrase(s) d'un seul mot "
                         f"(maximum {cfg['phrase_un_mot_permise']})"))

    # 15. Antithese binaire repetee
    n_anti = len(re.findall(r"ce n'est pas .{0,60}?\bc'est\b", plat_txt))
    if n_anti > 1:
        c.append(Constat(DEFAUT, "antithese-binaire",
                         f"« Ce n'est pas A, c'est B » employe {n_anti} fois",
                         "une fois c'est une figure, deux fois c'est une signature"))

    # 16. Chapeau annonciateur
    for chapeau in ("voici pourquoi", "ce que ca change concretement",
                    "trois raisons a cela", "la vraie question n'est pas"):
        if chapeau in plat_txt:
            c.append(Constat(ALERTE, "chapeau-annonciateur",
                             f"chapeau annonciateur « {chapeau} »",
                             "un seul signal de voix par texte"))
            break

    # 17. Contraintes de plateforme
    if cfg["hashtags_max"] is not None:
        tags = re.findall(r"#\w+", prose)
        if len(tags) > cfg["hashtags_max"]:
            c.append(Constat(ALERTE, "hashtags",
                             f"{len(tags)} hashtags (maximum {cfg['hashtags_max']})",
                             " ".join(tags[:8])))
        generiques = {"#innovation", "#digital", "#motivation", "#business",
                      "#transformation", "#leadership", "#inspiration"}
        vus = [t for t in tags if t.lower() in generiques]
        if vus:
            c.append(Constat(ALERTE, "hashtags-generiques",
                             f"hashtag(s) generique(s) : {' '.join(vus)}",
                             "ils n'apportent rien et signent le post automatique"))
    if cfg["longueur_max"] and len(prose) > cfg["longueur_max"]:
        c.append(Constat(DEFAUT, "longueur",
                         f"{len(prose)} caracteres (limite {cfg['longueur_max']})"))

    # 18. Apostrophe creuse au lecteur
    for formule in ("vous l'aurez compris", "posez-vous la question",
                    "imaginez un instant", "et vous, qu'en pensez-vous"):
        if formule in plat_txt:
            c.append(Constat(DEFAUT, "apostrophe-creuse",
                             f"« {formule} »",
                             "n'apporte aucune information, quel que soit le profil"))
            break

    return c


# --------------------------------------------------------------------------
# Analyse d'un fichier
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Controles propres aux slides
# --------------------------------------------------------------------------

RE_PUCE = re.compile(r"^\s*(?:[-*+•]|\d+[.)])\s+(.*\S)\s*$", re.M)


def sans_code(source: str) -> str:
    """Blanchit les blocs de code et les commentaires, a longueur constante.

    Remplacer par du vide decalerait toutes les positions et fausserait les
    numeros de ligne. On substitue caractere pour caractere, sauf les sauts.
    """
    def blanchir(m):
        return "".join(ch if ch == "\n" else " " for ch in m.group(0))

    texte = re.sub(r"^```.*?^```", blanchir, source, flags=re.S | re.M)
    texte = re.sub(r"^~~~.*?^~~~", blanchir, texte, flags=re.S | re.M)
    return re.sub(r"<!--.*?-->", blanchir, texte, flags=re.S)


def controles_puces(source, cfg):
    """Longueur et ponctuation des puces. N'agit qu'en profil presentation.

    Une puce n'est pas une phrase : ni verbe conjugue superflu, ni point final.
    Le controle porte sur le balisage brut, avant que prepare() ne l'efface.
    """
    if cfg["puce_max_mots"] is None and not cfg["puce_sans_point_final"]:
        return []

    c = []
    longues, ponctuees = [], []
    for m in RE_PUCE.finditer(sans_code(source)):
        texte = re.sub(r"[`*_\[\]]", "", m.group(1)).strip()
        if not texte:
            continue
        if cfg["puce_max_mots"] and len(mots(texte)) > cfg["puce_max_mots"]:
            longues.append((texte, ligne_de(source, m.start())))
        if cfg["puce_sans_point_final"] and texte.endswith("."):
            ponctuees.append((texte, ligne_de(source, m.start())))

    if longues:
        c.append(Constat(DEFAUT, "puce-longue",
                         f"{len(longues)} puce(s) de plus de {cfg['puce_max_mots']} mots",
                         f"« {longues[0][0][:70]}… » · au-dela, la slide est un document",
                         longues[0][1]))
    if ponctuees:
        c.append(Constat(ALERTE, "puce-ponctuee",
                         f"{len(ponctuees)} puce(s) terminee(s) par un point",
                         "une puce n'est pas une phrase : pas de point final",
                         ponctuees[0][1]))
    return c


def analyser(chemin, profil, controles):
    with open(chemin, encoding="utf-8") as f:
        source = f.read()
    prose, drapeaux = prepare(source)
    cfg = PROFILS[profil]
    plat = paragraphes(prose)

    constats = controles_typo(source, prose, profil, cfg)
    if controles == "tout":
        constats += controles_langue(prose, plat, profil, cfg)
        constats += controles_puces(source, cfg)

    if drapeaux["contre_exemples"]:
        for c in constats:
            if c.severite in (BLOQUANT, DEFAUT):
                c.severite = INFO

    score = 100
    for c in constats:
        score -= POIDS[c.severite]
    score = max(0, min(100, score))

    constats.sort(key=lambda c: (ORDRE[c.severite], c.regle))
    return {
        "fichier": chemin,
        "profil": profil,
        "score": score,
        "mots": len(mots(prose)),
        "phrases": len(phrases(prose)),
        "contre_exemples": drapeaux["contre_exemples"],
        "constats": [c.dict() for c in constats],
    }


# --------------------------------------------------------------------------
# Sortie
# --------------------------------------------------------------------------

COULEURS = {BLOQUANT: "\033[31m", DEFAUT: "\033[33m", ALERTE: "\033[36m",
            INFO: "\033[90m"}
GRIS, RAZ, GRAS = "\033[90m", "\033[0m", "\033[1m"


def afficher(rapport, couleur):
    def c(code, texte):
        return f"{code}{texte}{RAZ}" if couleur else texte

    score = rapport["score"]
    teinte = "\033[32m" if score >= 80 else "\033[33m" if score >= 60 else "\033[31m"
    print()
    print(c(GRAS, "MOLIÈRE") + c(GRIS, " · contrôle") + "   " +
          c(GRIS, rapport["fichier"]))
    print(c(GRIS, f"profil {rapport['profil']} · {rapport['mots']} mots · "
                  f"{rapport['phrases']} phrases") + "   " +
          c(teinte, f"score {score}/100"))
    if rapport["contre_exemples"]:
        print(c(GRIS, "fichier declare « contre-exemples » : tout est ramene a titre indicatif"))
    print()

    if not rapport["constats"]:
        print(c("\033[32m", "  rien a signaler"))
        print()
        return

    for k in rapport["constats"]:
        etiquette = f"[{k['severite']}]".ljust(11)
        print("  " + c(COULEURS[k["severite"]], etiquette) + k["message"])
        if k["detail"]:
            print("             " + c(GRIS, k["detail"]))
    print()


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="moliere_lint",
        description="Controle mecanique d'un texte francais. "
                    "Compte ce qui se compte, ne juge pas ce qui se juge.")
    p.add_argument("fichiers", nargs="+", help="fichiers ou dossiers a controler")
    p.add_argument("--profil", default="document", choices=sorted(PROFILS),
                   help="support vise (defaut : document)")
    p.add_argument("--controles", default="tout", choices=("tout", "typo"),
                   help="tout, ou seulement les controles typographiques")
    p.add_argument("--seuil", type=int, default=0,
                   help="score minimal exige ; 0 desactive le seuil")
    p.add_argument("--strict", action="store_true",
                   help="code retour non nul des le premier constat bloquant")
    p.add_argument("--json", action="store_true", help="sortie JSON")
    p.add_argument("--version", action="version", version=f"moliere_lint {VERSION}")
    a = p.parse_args(argv)

    chemins = []
    for f in a.fichiers:
        if os.path.isdir(f):
            for racine, _, noms in os.walk(f):
                chemins += [os.path.join(racine, n) for n in sorted(noms)
                            if n.endswith((".md", ".txt"))]
        else:
            chemins.append(f)
    if not chemins:
        print("aucun fichier a controler", file=sys.stderr)
        return 2

    rapports = [analyser(ch, a.profil, a.controles) for ch in chemins]

    if a.json:
        print(json.dumps(rapports, ensure_ascii=False, indent=2))
    else:
        couleur = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
        for r in rapports:
            afficher(r, couleur)

    echec = False
    for r in rapports:
        if r["contre_exemples"]:
            continue
        if a.strict and any(k["severite"] == BLOQUANT for k in r["constats"]):
            echec = True
        if a.seuil and r["score"] < a.seuil:
            echec = True
    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())
