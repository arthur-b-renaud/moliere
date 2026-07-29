#!/usr/bin/env python3
"""Detourage du Moliere de Mignard.

Le fond est un noir verdatre presque uniforme, et les feuilles les plus sombres
de la couronne de laurier partagent sa valeur a cinq niveaux pres. Un simple
seuil fuit donc a travers la couronne et la mite.

La parade tient en trois temps :
  1. propagation depuis les bords, qui ne retire que le fond *relie* au bord ;
  2. rebouchage des trous enclaves, ce qui reconstitue la couronne ;
  3. mais filtre par la taille : les interstices entre feuilles font quelques
     pixels et se rebouchent, la poche de fond que le rameau enclave a droite
     de la tete en fait cent et reste transparente.

Le bord bas n'est jamais seme : le buste y est coupe par le cadre.
"""
import sys

import numpy as np
from PIL import Image, ImageFilter

SRC = "assets/entete.webp"
X0, X1, Y0, Y1 = 11, 765, 1, 931           # bornes du tableau de gauche
FOND = np.array([2.0, 17.0, 13.0])         # couleur de fond, echantillonnee
COLMATE = 3                                # colmatage des interstices
ZONE = (500, 320)                          # x min, y max du rameau de droite


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

    # Colmatage : les interstices entre feuilles communiquent avec l'exterieur.
    # On dilate, on rebouche tout ce qui devient enclave, on revient a la taille.
    # C'est ce qui reconstitue la couronne au lieu de la miter.
    sujet = dilate(sujet, COLMATE)
    sujet |= ~propager(~sujet, graines)
    sujet = erode(sujet, COLMATE)

    # Reste une poche de vrai fond, enclavee par le rameau a droite de la tete,
    # que le rebouchage a rendue opaque. On la retire par sa taille : elle
    # survit a une erosion que les interstices ne passent pas.
    #
    # Le filtre est borne a cette zone. Applique partout, il emporterait aussi
    # le baton noir et les ombres du drape, qui sont sombres et etendus : le
    # critere de taille ne distingue pas un fond d'un objet noir.
    zone = np.zeros((h, w), bool)
    zone[:ZONE[1], ZONE[0]:] = True
    residu = sujet & candidat & zone
    sujet &= ~dilate(erode(residu, taille_trou), taille_trou)

    alpha = np.asarray(Image.fromarray((sujet * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(plume))).astype(float) / 255.0
    alpha = np.clip((alpha - 0.42) / 0.30, 0, 1)

    # Decontamination : le fond a bave sur les pixels de bordure, on le retire
    # au prorata de l'opacite, sans quoi le detourage porte un lisere noir.
    bord = (alpha > 0.02) & (alpha < 0.98)
    net = rgb.copy()
    a3 = alpha[..., None]
    net[bord] = np.clip((rgb[bord] - FOND * (1 - a3[bord])) / np.maximum(a3[bord], .25), 0, 255)

    Image.fromarray(np.dstack([net, alpha * 255]).astype(np.uint8), "RGBA").save(sortie)
    print(f"{sortie}  {w}x{h}  opaque a {100 * (alpha > .5).mean():.1f} %")


if __name__ == "__main__":
    main(float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
