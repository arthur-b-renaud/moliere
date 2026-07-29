# Images du dépôt

Ce dossier ne contient que ce qui ne peut pas être écrit en texte. Un tableau HTML vaut mieux qu'une capture d'écran : il se copie, il se cherche, il se lit au lecteur d'écran, et il ne se périme pas au premier changement de sortie du linter.

## Ce qui est là

| Fichier | Origine | Comment le refaire |
|---|---|---|
| `entete.webp` | Montage de deux portraits du domaine public, voir `SOURCES.md` | Recadrer en 1280 × 400 pour la bannière |
| `rythme.svg` | Généré | `python3 skills/moliere/scripts/courbe_rythme.py exemples/document-avant.md exemples/document-apres.md -o assets/rythme.svg --titres "texte marqué : plateau" "texte révisé : respiration"` |

`rythme.svg` est régénérable et versionné. Il ne demande aucune dépendance, il pèse trois kilo-octets, et il reste lisible en thème clair comme en thème sombre.

## Ce qui manque, par ordre de rendement

### 1. L'aperçu social, 1280 × 640

C'est l'image qui s'affiche quand quelqu'un partage le lien du dépôt sur LinkedIn ou sur X. Elle se règle dans **Settings → General → Social preview** et elle ne vit pas dans le dépôt.

C'est de loin l'image la plus rentable, et la seule dont l'absence coûte vraiment : sans elle, GitHub affiche une vignette générique qui ne dit rien.

Ce qu'elle doit porter, dans cet ordre : le mot **Molière**, une ligne de sous-titre qui dit ce que c'est, et le contraste avant-après réduit à deux phrases. Pas de capture d'écran de terminal : illisible à cette taille dans un fil.

### 2. La bannière d'en-tête, 1280 × 400

`entete.webp` fait l'affaire mais n'est pas recadrée : les deux portraits en pied prennent trop de hauteur. Un recadrage sur les visages, avec le titre en surimpression, tiendrait mieux.

```bash
convert assets/entete.webp -resize 1280x -gravity north -crop 1280x400+0+40 assets/banniere.webp
```

### 3. La carte des marqueurs, format carré

Les huit tics les plus fréquents et leur correction, sur une image carrée pensée pour être repartagée seule. C'est le contenu qui circule le mieux, parce qu'il est utile sans le dépôt.

Prendre les huit premières lignes du tableau « Ce que le skill corrige » du README.

### 4. L'enregistrement de terminal

Une révision réelle dans Claude Code, de la demande au texte rendu. À faire avec [`vhs`](https://github.com/charmbracelet/vhs), qui produit un GIF à partir d'un script versionnable, plutôt qu'avec un enregistreur d'écran dont personne ne pourra refaire la prise.

Garder sous quarante secondes. Au-delà, personne ne regarde jusqu'au bout.

## Ce qu'il ne faut pas ajouter

- **Une capture de la sortie du linter.** Le README la donne en bloc de code : plus lisible, cherchable, et elle ne ment pas quand la sortie change.
- **Un badge de couverture ou de qualité** qui ne mesure rien de réel. Le dépôt en porte déjà quatre, ce qui est la limite avant que personne ne les lise.
- **Des icônes décoratives dans les titres.** Le skill proscrit les puces à emoji ; le dépôt ne va pas s'en dispenser.
