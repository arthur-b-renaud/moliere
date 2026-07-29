# Marqueurs de rédaction automatique

Sommaire : 1. Typographie. 2. Lexique. 3. Structures de phrase. 4. Structures de texte. 5. Test de densité.

Ce qui trahit un texte n'est pas la présence d'un marqueur isolé mais leur densité. Deux tirets cadratins suffisent pourtant à eux seuls.

Aucun élément de ce fichier n'est fautif en soi. Ce sont des marqueurs, c'est-à-dire des traits dont la fréquence est anormale dans les textes produits par une machine. On les évite parce qu'ils signent, pas parce qu'ils sont interdits.

Les anglicismes ne figurent pas ici. Ils relèvent du vocabulaire et non de la signature, et `STYLE.md` les traite en une règle : corriger les constructions fautives, garder les emprunts que la profession emploie.

---

## 1. Typographie

| Marqueur | Correction |
|---|---|
| Tiret cadratin (U+2014) et demi-cadratin (U+2013) en incise | virgules, deux-points, parenthèses, ou couper la phrase. Motif et exceptions dans `typographie.md` |
| Gras dans le corps du texte | supprimer ; l'emphase se construit syntaxiquement |
| Puces avec emoji en tête | supprimer |
| Guillemets anglais dans un texte français | guillemets français |
| Points de suspension | point |
| Points d'exclamation | point, sauf un par texte en profil `post` |
| Titres avec une capitale à chaque mot | capitale au premier mot seulement |
| Gras ou italique fabriqués en caractères mathématiques Unicode | supprimer ; ils cassent les lecteurs d'écran |

## 2. Lexique

**Adjectifs surreprésentés.** crucial, essentiel, fondamental, incontournable, majeur, véritable, robuste, puissant, captivant, unique, clé (en apposition : « un enjeu clé »), stratégique employé sans objet.

**Verbes surreprésentés.** permettre, garantir, assurer, offrir, favoriser, optimiser, transformer, révolutionner, accompagner, s'inscrire dans, se positionner comme, venir compléter, répondre aux besoins.

**Substantifs creux.** solution, dispositif, démarche, écosystème, levier, synergie, brique, verticale, valeur ajoutée, expertise, enjeu, défi, opportunité employé au sens de « occasion ».

**Locutions.** il est important de noter que, il convient de souligner, force est de constater, dans un monde où, à l'ère de, plus que jamais, à l'heure où, loin d'être anecdotique, ce n'est pas un détail, l'enjeu est double, en somme, en conclusion, pour aller plus loin, vous l'aurez compris, la vraie question n'est pas X mais Y.

**Adverbes de liaison en excès.** par ailleurs, de plus, en outre, ainsi, néanmoins, notamment. Un par texte, pas davantage.

Aucun de ces mots n'est fautif en soi. Le problème tient à leur fréquence : ils apparaissent quand le rédacteur n'a rien de précis à dire et remplit avec du connecteur.

**Réserve importante.** Chacun de ces mots redevient légitime dès qu'il est le terme exact du domaine. Le dispositif d'un jugement, une solution aqueuse, l'écosystème d'un lac, le levier d'une commande hydraulique, une charge robuste au sens mécanique : ce sont des emplois précis, pas du remplissage. Le test tient en une question : le mot désigne-t-il cette chose et rien d'autre, ou pourrait-il désigner n'importe quoi ? Un correcteur qui bannit « solution » d'un article de chimie n'a pas compris la règle.

## 3. Structures de phrase

- **Participe présent en queue** : « ..., permettant ainsi de », « ..., offrant une meilleure lisibilité ». Le marqueur le plus fiable après le tiret cadratin.
- **Énumération ternaire d'adjectifs** : « rapide, fiable et évolutif ».
- **Antithèse binaire répétée** : « Ce n'est pas A. C'est B. » Une fois par texte, c'est une figure. Deux fois, c'est une signature.
- **Double adjectif systématique** : « une approche cohérente et personnalisée », « des besoins spécifiques et évolutifs ».
- **Phrase d'un seul mot** en guise d'emphase.
- **Uniformité métrique** : toutes les phrases entre quinze et vingt mots.
- **Chapeau annonciateur** : « Voici pourquoi : », « Ce que ça change concrètement : », « Trois raisons à cela : ».
- **Symétrie parfaite des paragraphes** : quatre paragraphes de trois phrases chacun.

## 4. Structures de texte

- Le paragraphe de synthèse final qui répète ce que le texte vient de dire.
- L'introduction qui annonce le plan.
- La question rhétorique en ouverture.
- La liste à puces là où deux phrases suffiraient.
- L'exemple générique, sans nom propre, sans date, sans chiffre : « une entreprise du secteur bancaire a récemment constaté que... ». Un texte humain cite Schneider, le 12 mars, 4,2 millions.
- La neutralité totale : aucune phrase ne prend de risque, aucune n'est réfutable.

## 5. Test de densité

Compter sur un texte de trois cents mots :

- Plus de deux items de la section 2 : le texte sonne artificiel.
- Un seul item de la section 1 ou 3 : le texte est identifié comme généré.
- Zéro nom propre, zéro chiffre, zéro date : le texte n'a rien dit.

Correctif le plus efficace, à appliquer en premier : remplacer un exemple générique par un exemple daté et nommé. Un fait vérifiable annule dix marqueurs.

**Ces trois seuils sont empiriques.** Ils viennent d'une lecture attentive de beaucoup de textes générés, pas d'un corpus annoté ni d'une mesure de fréquence. Les écrire en chiffres leur donne une précision qu'ils n'ont pas. Ils servent à ordonner les priorités de révision, pas à trancher si un texte est généré.
