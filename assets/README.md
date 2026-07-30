# Images du dépôt

Ce dossier ne contient que ce qui ne peut pas être écrit en texte. Un tableau HTML vaut mieux qu'une capture d'écran : il se copie, il se cherche, il se lit au lecteur d'écran, et il ne se périme pas au premier changement de sortie du linter.

## Ce qui est là

| Fichier | Format | Où il sert | Comment le refaire |
|---|---|---|---|
| `social-preview.png` | 1280 × 640 | Vignette affichée quand le lien du dépôt est partagé | `gabarits/social.html`, rendu à 2× puis réduit |
| `carte-marqueurs.png` | 1080 × 1080 | Section « Ce que le skill corrige », et se partage seule | `gabarits/carte.html`, même procédé |
| `rythme.svg` | vectoriel | Section « Le marqueur qu'on ne voit pas en lisant » | commande ci-dessous |
| `entete.webp` | 1920 × 2399 | Frontispice du README, et source du détourage | Numérisation Wikimedia du tableau de Mignard, voir `SOURCES.md` |
| `moliere-detoure.webp` | 1200 × 1440, alpha | Illustration libre, fond transparent | `gabarits/detoure.py`, voir ci-dessous |

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
python3 assets/gabarits/detoure.py 20 15 3 /tmp/moliere.png
convert /tmp/moliere.png -trim +repage -resize 1200x \
  -quality 92 -define webp:alpha-quality=100 assets/moliere-detoure.webp
```

Le script lit `entete.webp` : rien à télécharger, et le détourage se refait à l'identique depuis le seul contenu du dépôt. Les trois arguments sont la tolérance colorimétrique, le rayon du filtre de taille et la plume.

Il est commenté en tête de fichier, et il énonce sa propre limite. Mignard a peint la chevelure en fondu dans le fond : entre les deux, il n'existe aucune frontière, même pour un œil humain. Le détourage garde donc un peu de fond au pourtour des cheveux, ce qui se voit sur fond blanc et beaucoup moins sur un fond crème ou coloré. Ce n'est pas un défaut du script mais une propriété du tableau. Une rampe d'opacité douce a été essayée : elle délave tout, parce que les ombres du drapé et le bâton sont aussi proches du fond que la chevelure.

Le reste tient proprement, y compris sur fond clair, grâce à une décontamination des pixels de bordure au prorata de leur opacité.

## L'aperçu social se règle à la main

`social-preview.png` est versionné, mais **GitHub n'expose aucune API pour l'installer**. C'est la seule étape manuelle du dépôt :

> Settings → General → Social preview → Upload an image → `assets/social-preview.png`

Sans elle, GitHub affiche une vignette générique quand quelqu'un partage le lien sur LinkedIn ou sur X, et c'est de là que vient l'essentiel du trafic.

## Ce qui manque encore

**Une bannière large, si l'on en veut une.** Le frontispice actuel est le tableau entier, en portrait, affiché à 44 % de la largeur du README. C'est délibéré : un tableau de 1658 se regarde dans son cadre. Qui préfère une bannière peut recadrer sur le buste, en sachant que la composition de Mignard place la tête dans le tiers haut et qu'une coupe basse la décentre.

```bash
convert assets/entete.webp -resize 1920x -crop 1920x600+0+380 +repage \
  -resize 1280x -quality 84 assets/banniere.webp
```

**Un enregistrement de terminal.** Une révision réelle, de la demande au texte rendu. À faire avec [`vhs`](https://github.com/charmbracelet/vhs), qui produit un GIF à partir d'un script versionnable, plutôt qu'avec un enregistreur d'écran dont personne ne pourra refaire la prise. Garder sous quarante secondes : au-delà, personne ne regarde jusqu'au bout.

## Ce qu'il ne faut pas ajouter

- **Une capture de la sortie du linter.** Le README la donne en bloc de code : plus lisible, cherchable, et elle ne ment pas quand la sortie change.
- **Un badge qui ne mesure rien de réel.** Le dépôt en porte cinq, ce qui est la limite avant que personne ne les lise.
- **Des icônes décoratives dans les titres.** Le skill proscrit les puces à emoji ; le dépôt ne va pas s'en dispenser.
