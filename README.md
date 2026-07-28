<p align="center">
  <img src="assets/entete.webp" alt="Molière et Shakespeare" width="100%">
</p>

<h1 align="center">Molière</h1>

<p align="center">
  <em>Un skill Claude Code pour écrire un français qui n'a pas l'air traduit,<br>
  ni écrit par une machine.</em>
</p>

<p align="center">
  <a href="#licence"><img alt="Licence MIT et CC BY 4.0" src="https://img.shields.io/badge/licence-MIT%20%2B%20CC%20BY%204.0-blue"></a>
  <img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8%2B-blue">
  <img alt="Sans dépendance" src="https://img.shields.io/badge/d%C3%A9pendances-aucune-green">
  <img alt="Langue française" src="https://img.shields.io/badge/langue-fran%C3%A7ais-lightgrey">
</p>

---

> **In English, briefly.** `moliere` is a Claude Code skill that writes and edits French prose without the tells of machine writing or literal translation from English. It bundles a style guide (rhythm, connectives, verbs, French typography), a blacklist of LLM markers, and a zero-dependency Python linter that measures what a language model cannot reliably count: sentence-length variance, opening-line length, marker density, factual anchoring. Four profiles: LinkedIn post (default), analysis note, email, commercial proposal. Everything below is in French, because the subject is.

---

## Sommaire

- [Le problème](#le-problème)
- [Installation](#installation)
- [Tutoriel en cinq minutes](#tutoriel-en-cinq-minutes)
- [Les quatre profils](#les-quatre-profils)
- [Les trois modes](#les-trois-modes)
- [Ce que le skill corrige](#ce-que-le-skill-corrige)
- [Le linter](#le-linter)
- [Le personnaliser](#le-personnaliser)
- [Pourquoi Molière](#pourquoi-molière)
- [Ce que le skill ne fait pas](#ce-que-le-skill-ne-fait-pas)
- [Sources](#sources)
- [Contribuer](#contribuer)
- [Licence](#licence)

---

## Le problème

> « Ce que l'on conçoit bien s'énonce clairement, et les mots pour le dire arrivent aisément. »
> Nicolas Boileau, *L'Art poétique*, 1674

Un modèle de langue écrit un français grammaticalement correct et immédiatement reconnaissable. Ce n'est pas une question de vocabulaire. C'est le tiret cadratin en incise, le participe présent en fin de phrase, l'énumération à trois adjectifs, l'exemple sans nom propre ni date, et douze phrases de dix-huit mots à la file.

Le voici, appliqué à un post que tout le monde a déjà lu :

<table>
<tr><th width="50%">Avant</th><th width="50%">Après</th></tr>
<tr valign="top">
<td>

Et si le véritable enjeu du recrutement n'était pas le sourcing, mais l'expérience candidat&nbsp;?

Dans un monde où la guerre des talents s'intensifie, les entreprises doivent adresser cette problématique de manière stratégique. Notre écosystème RH se transforme en profondeur — et cela n'est pas un détail.

Une entreprise du secteur industriel a récemment constaté que la mise en place d'un dispositif de suivi permettait d'améliorer ses indicateurs, offrant ainsi une meilleure visibilité sur son pipeline.

Vous l'aurez compris, l'expérience candidat n'est plus une option.

</td>
<td>

Sur nos douze derniers recrutements de techniciens de maintenance, onze candidats ont abandonné avant l'entretien. Pas après. Avant.

Le processus durait vingt-trois jours entre la candidature et la première réponse. Un technicien qualifié, en Isère, reçoit trois propositions par semaine. Il ne nous attendait pas.

Nous avons changé une seule chose&nbsp;: la réponse part désormais sous quarante-huit heures, y compris quand elle est négative, et elle est signée par le responsable d'atelier, pas par un service.

Ce qui coûtait, ce n'était pas l'absence d'outil. C'était le silence.

</td>
</tr>
<tr>
<td align="center"><strong>34</strong>&nbsp;/100</td>
<td align="center"><strong>100</strong>&nbsp;/100</td>
</tr>
</table>

Les deux textes sont dans [`exemples/`](exemples/), avec les versions complètes et le relevé des interventions dans [`avant-apres.md`](skills/moliere/references/avant-apres.md). Les scores sortent du linter fourni, que vous pouvez relancer vous-même.

### Le marqueur qu'on ne voit pas en lisant

Les tics lexicaux se repèrent à l'œil. Le rythme, non : il faut le tracer. Voici la longueur de chaque phrase, dans l'ordre, pour une note d'analyse avant et après révision.

<p align="center">
  <img src="assets/rythme.svg" alt="Longueur des phrases : le texte marqué tient sur un plateau, le texte révisé alterne" width="100%">
</p>

Le texte généré tient sur un plateau : onze phrases de quatorze à dix-huit mots, écart type 1,0. Le texte révisé alterne des phrases de cinq et de vingt-neuf mots, écart type 7,6, pour une moyenne quasi identique. C'est la même longueur moyenne et ce n'est pas la même langue.

La courbe se génère sur vos propres textes :

```bash
python3 scripts/courbe_rythme.py avant.md apres.md -o rythme.svg
```

---

## Installation

Trois voies. La première suffit dans la plupart des cas.

### 1. Copier le skill

```bash
git clone https://github.com/arthur-b-renaud/skill-moliere.git
cp -r skill-moliere/skills/moliere ~/.claude/skills/
```

Le skill est disponible dans toutes vos sessions Claude Code. Vérifier :

```
/skills
```

`moliere` doit apparaître dans la liste.

### 2. Sur un seul projet

```bash
mkdir -p .claude/skills
cp -r /chemin/vers/skill-moliere/skills/moliere .claude/skills/
```

Utile quand un dépôt contient de la prose française (documentation, site, contenu) et pas les autres.

### 3. Avec les outils

Les scripts sont indépendants du skill. Pour que Claude puisse les lancer, garder le dépôt entier et travailler dedans :

```bash
git clone https://github.com/arthur-b-renaud/skill-moliere.git
cd skill-moliere
python3 scripts/moliere_lint.py exemples/post-avant.md --profil post
```

Aucune dépendance à installer. Python 3.8 suffit.

---

## Tutoriel en cinq minutes

> « Je n'ai fait celle-ci plus longue que parce que je n'ai pas eu le loisir de la faire plus courte. »
> Blaise Pascal, *Les Provinciales*, lettre XVI, 1657

### Étape 1. Écrire un post

Dans Claude Code, demandez simplement :

```
Écris-moi un post LinkedIn sur le fait qu'on a divisé par trois
notre délai de recrutement en répondant sous 48 h.
```

Le skill se déclenche seul. Il prend le profil `post`, lit `linkedin.md`, et applique le socle commun. Vous n'avez rien à invoquer.

Ce qu'il fait sans qu'on le lui demande : il vous réclamera un chiffre si vous n'en donnez pas. C'est voulu. Un post sans fait opposable est un post que personne ne discutera.

### Étape 2. Faire réviser un texte reçu

```
Relis-moi ça, c'est trop IA :
[collez votre texte]
```

Il rend le texte corrigé, puis une liste courte des interventions par nature de défaut. Jamais un texte annoté : vous voulez publier, pas corriger une copie.

Autres formulations qui déclenchent le skill : « ça fait trop américain », « on dirait une traduction », « réécris en français correct ».

### Étape 3. Épurer sans réécrire

Quand le fond est bon et que seuls les marqueurs gênent :

```
Épure ce texte, garde ma structure et mes mots, enlève juste
ce qui fait écriture automatique.
```

Le mode épuration touche au plus une phrase sur trois. C'est la différence avec la révision, qui refait le texte.

### Étape 4. Mesurer

Le skill énonce dix règles « mécaniques, vérifiables en comptant ». Or compter est exactement ce qu'un modèle de langue fait mal. D'où le linter :

```bash
python3 scripts/moliere_lint.py mon-post.md --profil post
```

```
MOLIÈRE · contrôle   mon-post.md
profil post · 180 mots · 12 phrases   score 34/100

  [bloquant] 19 marqueur(s) lexicaux, soit 31.7 pour 300 mots (seuil 2)
             dans un monde ou, demarche, dispositif, ecosysteme, en conclusion,
             enjeu, force est de constater, il est important de noter, levier
  [bloquant] 1 participe(s) present(s) en queue de phrase
             « , offrant » · couper la phrase ou coordonner avec « et »
  [defaut]   2 tiret(s) cadratin ou demi-cadratin
             lignes 3, 15 · remplacer par virgule, deux-points, parenthese ou point
  [defaut]   enumeration a trois adjectifs
             « rapide, fluide et transparent »
  [defaut]   question rhetorique en ouverture
  [alerte]   5 hashtags (maximum 3)
  [info]     attaque : 93 caracteres
  [info]     rythme
             moyenne 15.0 mots · ecart type 11.5
```

Et pour corriger la typographie sans toucher au style :

```bash
python3 scripts/typo_fix.py mon-post.md            # montre le diff
python3 scripts/typo_fix.py mon-post.md --ecrire   # applique
```

### Étape 5, facultative. Lui donner votre voix

Ouvrez [`skills/moliere/references/corpus-voix.md`](skills/moliere/references/corpus-voix.md) et collez-y cinq à dix textes que vous avez publiés et que vous assumez. C'est le seul fichier que le propriétaire du skill remplit lui-même, et c'est celui qui change tout : sans lui, vous obtenez du bon français neutre ; avec lui, vous obtenez le vôtre.

---

## Les quatre profils

Le socle est commun. Les profils n'assouplissent que ce qui les concerne.

| Profil | Pour | Ce qui change |
|---|---|---|
| **`post`** *(défaut)* | LinkedIn, X, newsletter | Le « je » et l'adresse au lecteur sont autorisés, le staccato toléré une fois, l'attaque doit tenir avant la coupure du « voir plus » |
| **`note`** | Analyse, article, compte rendu | Distance, troisième personne, conditionnel journalistique, attribution des sources, litote |
| **`courriel`** | Message professionnel | Bref, registre tenu, une demande par message. On ne fait pas de style dans un courriel |
| **`proposition`** | Offre, devis, appel d'offres | Verbe précis, chiffre opposable, engagement daté. Pas de litote : le client doit lire un engagement |

C'est le repositionnement le plus utile de ce skill. La version d'origine était calibrée pour la presse écrite et proscrivait le « je », l'adresse au lecteur et l'exclamation. Un bon post LinkedIn vit de ces trois interdits.

---

## Les trois modes

| Mode | Quand | Ce qu'il rend |
|---|---|---|
| **Rédaction** | Vous partez de rien | Le texte, sans commentaire sur le processus |
| **Révision** | Le texte existe, il est faible | Le texte refait, puis les interventions par nature de défaut |
| **Épuration** | Le texte est bon, il sent la machine | Le même texte, une phrase sur trois retouchée au plus |

---

## Ce que le skill corrige

> « Il semble que la perfection soit atteinte non quand il n'y a plus rien à ajouter, mais quand il n'y a plus rien à retrancher. »
> Antoine de Saint-Exupéry, *Terre des hommes*, 1939

| Symptôme | Exemple | Correction |
|---|---|---|
| Participe présent en queue | « …, permettant ainsi de réduire les coûts » | « … et réduit donc les coûts » |
| Nominalisation en chaîne | « la mise en œuvre de l'accompagnement des équipes » | « former les équipes » |
| Énumération ternaire | « rapide, fiable et évolutive » | « qui tient la charge » |
| Calque de l'anglais | « adresser cette problématique » | « traiter cette question » |
| Exemple générique | « une entreprise du secteur bancaire » | un nom, une date, un montant |
| Attaque décorative | « Dans un monde où l'IA transforme… » | le fait le plus fort, en tête |
| Chute récapitulative | « En conclusion, on retiendra que… » | une phrase qui ouvre, nuance ou tranche |
| Emphase | « un changement absolument majeur » | « n'est pas sans conséquence » |
| Rythme uniforme | douze phrases de dix-huit mots | écart type supérieur à six |
| Tiret cadratin | « le harnais compte — et de loin » | « le harnais compte, et de loin » |

Vingt réécritures commentées dans [`clinique.md`](skills/moliere/references/clinique.md), deux textes entiers dans [`avant-apres.md`](skills/moliere/references/avant-apres.md).

### Le cas du tiret cadratin

Le skill le proscrit par défaut. Il dit aussi pourquoi, et ce n'est pas la raison qu'on donne d'habitude.

Le tiret cadratin n'est **pas** une faute en français. Le *Lexique des règles typographiques en usage à l'Imprimerie nationale* l'admet en incise et le prescrit pour le dialogue, et la littérature française en use depuis toujours. Prétendre le contraire, c'est se faire corriger par le premier lecteur compétent.

Le motif est statistique : depuis 2023, un texte professionnel français qui porte trois cadratins est lu comme généré, quel qu'en soit l'auteur. On l'évite comme on évite une coupe de cheveux datée, pas comme on évite une faute d'accord. D'où les exceptions nommées : dialogue de fiction, citation d'une œuvre, convention du support, demande explicite.

C'est la seule position tenable, et elle vaut pour toutes les règles de ce skill : une prescription dont on ne peut pas donner le motif est une superstition.

Cette page contient trois tirets cadratins. Deux sont dans des contre-exemples, le troisième est dans la réplique de Monsieur Jourdain citée plus bas, où le tiret marque le dialogue comme le *Lexique* le prescrit. Les attributions de citations, elles, n'en portent aucun : elles en portaient sept avant que le contrôle ne passe sur ce fichier.

---

## Le linter

Trois scripts, aucune dépendance, tous facultatifs. Le skill fonctionne sans eux ; il est simplement moins vérifiable.

| Script | Ce qu'il fait |
|---|---|
| [`moliere_lint.py`](scripts/moliere_lint.py) | Mesure. Ne corrige rien, ne juge pas le style |
| [`typo_fix.py`](scripts/typo_fix.py) | Corrige le mécanique et le réversible. Ne touche jamais au style |
| [`courbe_rythme.py`](scripts/courbe_rythme.py) | Trace la longueur des phrases en SVG |

La séparation entre les deux premiers est délibérée. Un outil qui corrige la typographie peut agir seul ; un outil qui corrigerait le style prendrait des décisions qui appartiennent à l'auteur.

`scripts/moliere_lint.py` fait ce qu'un modèle de langue rate : compter.

```bash
python3 scripts/moliere_lint.py FICHIER... [options]

  --profil post|note|courriel|proposition   défaut : post
  --controles tout|typo                     typo : typographie seule
  --seuil N                                 score minimal exigé
  --strict                                  code retour non nul si bloquant
  --json                                    sortie machine
```

Ce qu'il mesure :

- tirets cadratins, guillemets anglais, points décimaux, ordinaux fautifs, puces à emoji, caractères Unicode de substitution
- participes présents en queue de phrase, énumérations ternaires d'adjectifs, antithèses binaires répétées
- moyenne et écart type des longueurs de phrase, plateaux métriques, staccato
- longueur de l'attaque en caractères, chute plus longue que l'avant-dernière phrase
- ouvertures de paragraphe identiques, répétition d'un mot saillant sous quarante mots
- densité de marqueurs lexicaux pour trois cents mots, calques de l'anglais, abréviations de jargon
- ancrage : présence d'au moins un chiffre, un nom propre ou une date
- contraintes de plateforme : hashtags, hashtags génériques, longueur

Ce qu'il ne mesure pas : l'orthographe, les accords, la conjugaison. Voir [`scripts/correcteurs.md`](scripts/correcteurs.md) pour les ponts vers LanguageTool, Grammalecte et Hunspell, qui couvrent exactement ce qui manque.

Un fichier qui contient délibérément des contre-exemples se déclare, et tous ses constats passent à titre indicatif :

```markdown
<!-- moliere-lint: contre-exemples -->
```

### Ce dépôt s'applique ses propres règles

L'[intégration continue](.github/workflows/lint.yml) exige que `exemples/post-apres.md` et `exemples/note-apres.md` obtiennent au moins 90, que les versions marquées soient bien détectées sous 70, et que la typographie du skill lui-même soit propre. Si le linter échoue, c'est le linter ou l'exemple qui a tort, et il faut trancher avant de fusionner.

### Le hook, non livré

Un hook `PostToolUse` qui lance le linter à chaque écriture de fichier rendrait les règles réellement contraignantes. Il n'est pas activé dans ce dépôt, parce qu'un hook s'exécute chez celui qui l'installe et que personne n'aime le découvrir après coup. La procédure complète est dans [`scripts/hook-exemple.md`](scripts/hook-exemple.md).

---

## Le personnaliser

> « Le style est l'homme même. »
> Buffon, *Discours sur le style*, 1753

Un skill de style produit du français correct. Seul un corpus produit du français qui ressemble à quelqu'un.

1. Ouvrir `skills/moliere/references/corpus-voix.md`
2. Y coller cinq à dix textes publiés, avec pour chacun une ligne d'analyse portant sur la mécanique et jamais sur le fond : ce que fait l'attaque, comment la chute retombe, où se trouve la rupture de rythme
3. Retirer un texte dès qu'il ne représente plus la voix actuelle

Un exemple entièrement rempli figure dans le fichier. Un corpus périmé est pire qu'un corpus vide.

**Régler l'écriture inclusive.** Le défaut du skill : tournures épicènes et collectifs, point médian proscrit pour un motif d'accessibilité, doublets courts admis. Dites-le si vous voulez autre chose, il appliquera sans discuter.

---

## Pourquoi Molière

> MONSIEUR JOURDAIN. — Non, vous dis-je, je ne veux que ces seules paroles-là dans le billet ; mais tournées à la mode, bien arrangées comme il faut.
> Molière, *Le Bourgeois gentilhomme*, acte II, scène 4, 1670

Monsieur Jourdain veut écrire « Belle Marquise, vos beaux yeux me font mourir d'amour ». Son maître de philosophie lui propose la même phrase dans cinq ordres différents. Jourdain garde le premier.

La scène est une leçon de style entière : les mots étaient donnés, tout le travail portait sur leur ordre, et la meilleure version était celle qui ne se remarquait pas. C'est le programme de ce dépôt.

---

## Ce que le skill ne fait pas

Une page qui ne dit que ce qu'elle sait faire est une page qui ment par omission.

- **Il ne corrige pas l'orthographe.** Voir [`scripts/correcteurs.md`](scripts/correcteurs.md).
- **Il ne vérifie aucun fait.** Il vous pousse à en donner ; il ne sait pas s'ils sont vrais.
- **Il ne connaît qu'un français.** Celui de France, registre professionnel. Un lectorat belge, suisse ou québécois trouvera des frottements. Contributions bienvenues.
- **Ses listes de marqueurs ne sont pas mesurées.** Elles viennent d'une lecture attentive de beaucoup de textes générés, pas d'un corpus annoté. C'est utile et c'est discutable.
- **Il ne rend pas un texte intéressant.** Le correctif le plus rentable ne figure dans aucune liste noire : écrire une phrase qu'un lecteur compétent pourrait contester, puis la défendre.

Les points que l'auteur juge encore discutables sont réunis dans [`CRITIQUE.md`](CRITIQUE.md), avec les réécritures proposées. Ils attendent un arbitrage.

---

## Sources

> « Le secret d'ennuyer est celui de tout dire. »
> Voltaire, *Sept Discours en vers sur l'homme*, 1738

Ce skill n'invente pas ses règles, il les emprunte, et il dit à qui : le *Lexique des règles typographiques en usage à l'Imprimerie nationale*, les conseils d'écriture d'Umberto Eco dans la traduction de Sébastien Bailly, la clinique des phrases de L'Oreille tendue, les usages de la presse économique française.

Le détail, édition par édition, est dans [`SOURCES.md`](SOURCES.md). Une règle dont on ne peut pas remonter la source est une opinion déguisée en méthode.

> « Supprimez les adjectifs, les adverbes et tous les mots qui ne sont là que pour faire de l'effet. »
> Georges Simenon, entretien à *The Paris Review*, 1955, traduit de l'anglais

---

## Contribuer

Les contributions les plus utiles, par ordre :

1. **Un marqueur qui manque**, avec un exemple réel et sa correction. C'est ce qui fait vieillir le mieux : les tics des modèles changent tous les six mois.
2. **Un faux positif du linter**, avec le texte qui le déclenche. Un linter qui crie à tort est un linter qu'on désactive.
3. **Une variante régionale** : belge, suisse, québécoise. Le skill n'en connaît aucune.
4. **Une contestation argumentée** d'une règle. Voir `CRITIQUE.md` pour celles qui sont déjà ouvertes.

Voir [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Licence

- **Les scripts** (`scripts/`) : [MIT](LICENSE).
- **Le skill et sa prose** (`skills/`, `exemples/`, documentation) : [CC BY 4.0](LICENSE-CONTENT). Réutilisez, modifiez, redistribuez, y compris commercialement, en citant la source.

Les citations reproduites le sont à des fins de commentaire, avec attribution. Voir `SOURCES.md`.
