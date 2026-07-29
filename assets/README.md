# Images du dépôt

Ce dossier ne contient que ce qui ne peut pas être écrit en texte. Un tableau HTML vaut mieux qu'une capture d'écran : il se copie, il se cherche, il se lit au lecteur d'écran, et il ne se périme pas au premier changement de sortie du linter.

## Ce qui est là

| Fichier | Format | Où il sert | Comment le refaire |
|---|---|---|---|
| `social-preview.png` | 1280 × 640 | Vignette affichée quand le lien du dépôt est partagé | `gabarits/social.html`, rendu à 2× puis réduit |
| `carte-marqueurs.png` | 1080 × 1080 | Section « Ce que le skill corrige », et se partage seule | `gabarits/carte.html`, même procédé |
| `rythme.svg` | vectoriel | Section « Le marqueur qu'on ne voit pas en lisant » | commande ci-dessous |
| `entete.webp` | bannière | Haut du README | Montage de deux portraits du domaine public, voir `SOURCES.md` |
| `moliere-detoure.png` | 754 × 902, alpha | Illustration libre, fond transparent | `gabarits/detoure.py`, voir ci-dessous |

Les deux images matricielles se régénèrent à partir des gabarits HTML de `gabarits/`, sans autre dépendance qu'un navigateur :

```bash
google-chrome --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1280,640 \
  --screenshot=/tmp/social@2x.png "file://$PWD/assets/gabarits/social.html"
convert /tmp/social@2x.png -resize 1280x640 -strip assets/social-preview.png
```

Le rendu à 2× puis la réduction donnent un anticrénelage propre sur les petits corps de texte, ce qu'une capture à 1× ne produit pas. Pour la carte, remplacer les dimensions par 1080 × 1080.

```bash
python3 skills/moliere/scripts/courbe_rythme.py \
  exemples/document-avant.md exemples/document-apres.md \
  -o assets/rythme.svg --titres "texte marqué : plateau" "texte révisé : respiration"
```

`rythme.svg` est régénérable et versionné. Il ne demande aucune dépendance, il pèse trois kilo-octets, et il reste lisible en thème clair comme en thème sombre.

## Le portrait détouré

```bash
python3 assets/gabarits/detoure.py 22 6 1.3 assets/moliere-detoure.png
```

Les trois arguments sont la tolérance de couleur, le rayon du filtre de taille et la plume. Le script est commenté : le fond du tableau est un noir verdâtre dont les feuilles les plus sombres du laurier ne se distinguent qu'à cinq niveaux près, ce qui interdit un seuil simple. Il procède par propagation depuis les bords, colmatage des interstices, rebouchage des poches enclavées, puis retrait de la seule poche de fond que le rameau de droite enferme.

Le résultat tient sur fond clair sans liseré sombre, grâce à une décontamination des pixels de bordure au prorata de leur opacité.

## L'aperçu social se règle à la main

`social-preview.png` est versionné, mais **GitHub n'expose aucune API pour l'installer**. C'est la seule étape manuelle du dépôt :

> Settings → General → Social preview → Upload an image → `assets/social-preview.png`

Sans elle, GitHub affiche une vignette générique quand quelqu'un partage le lien sur LinkedIn ou sur X, et c'est de là que vient l'essentiel du trafic.

## Ce qui manque encore

**Une bannière recadrée.** `entete.webp` fait l'affaire mais n'est pas recadrée : les deux portraits en pied prennent trop de hauteur. Un recadrage sur les visages, avec le titre en surimpression, tiendrait mieux.

```bash
convert assets/entete.webp -resize 1280x -gravity north -crop 1280x400+0+40 assets/banniere.webp
```

**Un enregistrement de terminal.** Une révision réelle, de la demande au texte rendu. À faire avec [`vhs`](https://github.com/charmbracelet/vhs), qui produit un GIF à partir d'un script versionnable, plutôt qu'avec un enregistreur d'écran dont personne ne pourra refaire la prise. Garder sous quarante secondes : au-delà, personne ne regarde jusqu'au bout.

## Ce qu'il ne faut pas ajouter

- **Une capture de la sortie du linter.** Le README la donne en bloc de code : plus lisible, cherchable, et elle ne ment pas quand la sortie change.
- **Un badge qui ne mesure rien de réel.** Le dépôt en porte cinq, ce qui est la limite avant que personne ne les lise.
- **Des icônes décoratives dans les titres.** Le skill proscrit les puces à emoji ; le dépôt ne va pas s'en dispenser.
