#!/usr/bin/env python3
"""Detourage du Moliere en Cesar de Nicolas Mignard.

    python3 assets/gabarits/detoure.py 20 15 3 /tmp/moliere.png
                                       │  │  └─ plume, en pixels
                                       │  └──── rayon du filtre de taille
                                       └─────── tolerance colorimetrique

Le fond est un brun sombre presque uniforme. Deux difficultes, dans cet ordre
d'importance :

1. Mignard a peint la chevelure en fondu dans ce fond. Entre les deux il
   n'existe aucune frontiere, meme pour un oeil humain. Aucun seuil ne peut
   donc y tracer un contour juste : le detourage garde un peu de fond au
   pourtour des cheveux, ce qui se voit sur un fond clair. C'est une propriete
   du tableau, pas un defaut du script. Une rampe d'opacite douce a ete
   essayee : elle rend translucides les ombres du drape et du baton, qui sont
   aussi proches du fond, et delave tout. Le seuil dur reste le moindre mal.

2. Les feuilles les plus sombres du laurier partagent la valeur du fond a
   quelques niveaux pres. Un seuil simple fuit a travers la couronne et la
   mite. La parade tient en trois temps : propagation depuis les bords, qui ne
   retire que le fond *relie* au bord ; colmatage des interstices puis
   rebouchage des poches ainsi enclavees, ce qui reconstitue la couronne ;
   enfin retrait par filtre de taille de la poche de vrai fond que le rameau
   de droite enferme, filtre borne a cette zone car applique partout il
   emporterait le baton noir et les ombres du drape.

Le bord bas n'est jamais seme : le buste y est coupe par le cadre, et le semer
decoupe le vetement sombre en dentelle.
"""
import sys

import numpy as np
from PIL import Image, ImageFilter

# La source est l'image d'en-tete du depot, qui est le tableau entier. Rien a
# telecharger, et le detourage se refait a l'identique depuis le seul contenu
# du depot. L'original pleine resolution est sur Wikimedia, voir SOURCES.md.
SRC = "assets/entete.webp"                   # 1920 x 2399
X0, X1, Y0, Y1 = 3, 1917, 3, 2396            # marge de securite sur le cadre
FOND = np.array([35.0, 30.0, 27.0])          # brun sombre, echantillonne
COLMATE = 7                                  # colmatage des interstices
ZONE = (1270, 830)                           # x min, y max du rameau de droite


def dilate(m, n=1):
    for _ in range(n):
        d = m.copy()
        d[1:, :] |= m[:-1, :]
        d[:-1, :] |= m[1:, :]
        d[:, 1:] |= m[:, :-1]
        d[:, :-1] |= m[:, 1:]
        m = d
    return m


def erode(m, n=1):
    return ~dilate(~m, n)


def propager(candidat, graines):
    """Composantes de `candidat` reliees a `graines`."""
    m = graines & candidat
    while True:
        n = dilate(m) & candidat
        if n.sum() == m.sum():
            return m
        m = n


def main(tolerance, taille_trou, plume, sortie):
    rgb = np.asarray(Image.open(SRC).convert("RGB")).astype(float)[Y0:Y1, X0:X1]
    h, w, _ = rgb.shape

    candidat = np.linalg.norm(rgb - FOND, axis=2) < tolerance

    graines = np.zeros((h, w), bool)
    graines[:3, :] = True
    graines[:, :3] = graines[:, -3:] = True

    sujet = ~propager(candidat, graines)
    sujet = dilate(erode(sujet))                    # retire les pixels isoles

    sujet = dilate(sujet, COLMATE)                  # colmatage, voir l'en-tete
    sujet |= ~propager(~sujet, graines)
    sujet = erode(sujet, COLMATE)

    zone = np.zeros((h, w), bool)                   # poche du rameau de droite
    zone[:ZONE[1], ZONE[0]:] = True
    residu = sujet & candidat & zone
    sujet &= ~dilate(erode(residu, taille_trou), taille_trou)

    # Ne garder que la masse reliee au buste. Le seuil laisse sinon des ilots
    # de fond detaches autour de la chevelure, qui passent pour des taches.
    noyau = np.zeros((h, w), bool)
    noyau[int(h * .55):int(h * .90), int(w * .25):int(w * .75)] = True
    sujet = propager(sujet, noyau & sujet)

    alpha = np.asarray(Image.fromarray((sujet * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(plume))).astype(float) / 255.0
    alpha = np.clip((alpha - 0.42) / 0.30, 0, 1)

    # Decontamination : le fond teinte les pixels partiellement opaques. On le
    # retire au prorata, sans quoi le detourage porte un halo brun sur clair.
    a3 = alpha[..., None]
    net = np.clip((rgb - FOND * (1 - a3)) / np.maximum(a3, 0.30), 0, 255)
    net = np.where(a3 > 0.985, rgb, net)

    Image.fromarray(np.dstack([net, alpha * 255]).astype(np.uint8), "RGBA").save(sortie)
    print(f"{sortie}  {w}x{h}  opaque a {100 * (alpha > .5).mean():.1f} %")


if __name__ == "__main__":
    main(float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
