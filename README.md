<!-- moliere-lint: contre-exemples -->

<p align="center">
  <img src="assets/entete.webp" width="44%"
       alt="Molière en César, portrait peint par Nicolas Mignard en 1658">
</p>

<h1 align="center">Molière</h1>

<p align="center">
  <em>Écrire un français contemporain qui n'a pas l'air traduit,<br>
  ni écrit par une machine.</em>
</p>

<p align="center">
  <a href="https://github.com/arthur-b-renaud/moliere/actions/workflows/lint.yml"><img alt="Contrôle" src="https://github.com/arthur-b-renaud/moliere/actions/workflows/lint.yml/badge.svg"></a>
  <a href="#licence"><img alt="Licence MIT et CC BY 4.0" src="https://img.shields.io/badge/licence-MIT%20%2B%20CC%20BY%204.0-blue"></a>
  <img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8%2B-blue">
  <img alt="Sans dépendance" src="https://img.shields.io/badge/d%C3%A9pendances-aucune-green">
  <img alt="Langue française" src="https://img.shields.io/badge/langue-fran%C3%A7ais-lightgrey">
</p>

---

## Le problème, et ce que fait ce dépôt

Un modèle de langue écrit un français grammaticalement correct et immédiatement reconnaissable. Le
tiret cadratin en incise, le participe présent en fin de phrase, l'énumération à trois adjectifs,
l'exemple sans nom propre ni date, et douze phrases de dix-huit mots à la file.

Ce n'est pas une question de vocabulaire. C'est l'ordre des mots, l'enchaînement des propositions,
le choix du verbe et la variation du rythme.

**Le but : un français meilleur que celui qui sort d'un modèle par défaut**, pour les documents de
plusieurs pages, les publications courtes et les présentations. Rien à configurer, aucun fichier à
remplir, aucune personnalisation.

---

## Installer

### Avec Claude Code

```bash
git clone https://github.com/arthur-b-renaud/moliere.git
cp -r moliere/skills/moliere ~/.claude/skills/
```

C'est fini. Tapez `/skills` pour vérifier : `moliere` doit apparaître. Il se déclenche seul dès que
vous écrivez ou faites relire du français, sur tous vos projets. Pour le limiter à un dépôt, copiez
le dossier dans `.claude/skills/` plutôt que dans votre dossier personnel.

### Avec ChatGPT, Gemini ou n'importe quel autre assistant

Ces outils n'acceptent pas les skills, mais ils acceptent une consigne. Toutes les règles tiennent
dans un seul fichier prévu pour ça : **[`STYLE.md`](skills/moliere/STYLE.md)**, 1 900 mots,
autoportant, sans renvoi ni dépendance. Ouvrez, copiez tout, collez.

| Outil | Où coller |
|---|---|
| ChatGPT | Créer un GPT, puis *Configurer → Instructions*. Ou en tête d'une conversation |
| Gemini | Créer un Gem, puis le champ d'instructions |
| Claude, application ou site | Créer un projet, puis les instructions personnalisées |
| Le Chat, Copilot, et les autres | Le champ d'instructions système, quel que soit son nom |

---

## Tutoriel

**Écrire.** Demandez, sans rien invoquer.

```
Écris-moi une publication LinkedIn sur le fait qu'on a divisé
par trois notre délai de recrutement en répondant sous 48 h.
```

Il vous réclamera un chiffre si vous n'en donnez pas. C'est voulu : une publication sans fait
opposable est une publication que personne ne discutera.

**Faire réviser.** Il rend le texte corrigé, puis les interventions par nature de défaut. Jamais un
texte annoté.

```
Relis-moi ça, c'est trop IA :
[collez votre texte]
```

Déclenchent aussi le skill : « ça fait trop américain », « on dirait une traduction », « réécris en
français correct ».

**Épurer sans réécrire**, quand le fond est bon et que seuls les marqueurs gênent. Le mode épuration
touche au plus une phrase sur trois.

```
Épure ce texte, garde ma structure et mes mots, enlève juste
ce qui fait écriture automatique.
```

**Mesurer**, facultativement. Compter est ce qu'un modèle de langue fait le plus mal.

```bash
python3 skills/moliere/scripts/moliere_lint.py mon-texte.md --profil post
```

```
MOLIÈRE · contrôle   mon-texte.md
profil post · 199 mots · 19 phrases   score 88/100

  [defaut]   enumeration a trois adjectifs
             « ameliore, teste et reutilise »
  [alerte]   chapeau annonciateur « ce que ca change concretement »
  [alerte]   1 marqueur(s) lexicaux : levier
  [info]     rythme
             moyenne 10.5 mots · ecart type 5.5
```

---

## L'essentiel

**Trois supports.** Le style ne change pas ; la longueur, la distance au lecteur et la place de
l'information changent.

| Profil | Pour |
|---|---|
| `document` *(défaut)* | Devis, proposition, note, rapport. Un courriel est un document court |
| `post` | Publication courte, billet |
| `presentation` | Diapositives |

**Trois modes.** Rédaction, révision, épuration.

**Deux règles absolues**, sans exception : jamais de participe présent en queue de phrase, jamais de
point décimal. Tout le reste se lève pour un motif nommé.

**Ce qu'il corrige**, pour les défauts les plus fréquents :

| Symptôme | Correction |
|---|---|
| « …, permettant ainsi de réduire les coûts » | « … et réduit donc les coûts » |
| « la mise en œuvre de l'accompagnement des équipes » | « former les équipes » |
| « rapide, fiable et évolutive » | « qui tient la charge » |
| « adresser cette problématique » | « traiter cette question » |
| « une entreprise du secteur bancaire » | un nom, une date, un montant |
| « Dans un monde où l'IA transforme… » | le fait le plus fort, en tête |
| « En conclusion, on retiendra que… » | une phrase qui ouvre, nuance ou tranche |
| douze phrases de dix-huit mots | écart type supérieur à six |

**Trois outils, tous facultatifs.** Le skill fonctionne entièrement sans Python : `moliere_lint.py`
mesure, `typo_fix.py` corrige la typographie, `courbe_rythme.py` trace le rythme.

Le détail est dans **[TECHNIQUE.md](TECHNIQUE.md)** : contrôles du linter, calcul du score, faux
positifs assumés, réglages, intégration continue, limites.

---

## Exemples

Voici le geste, sur une publication que tout le monde a déjà lue.

<table>
<tr><th width="50%">Avant · 34/100</th><th width="50%">Après · 100/100</th></tr>
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
</table>

| Où | Quoi |
|---|---|
| [`exemples/`](exemples/) | Six fichiers, trois paires avant et après, un par support |
| [`exemples-phrases.md`](skills/moliere/references/exemples-phrases.md) | Vingt réécritures commentées, du symptôme au remède |
| [`exemples-textes.md`](skills/moliere/references/exemples-textes.md) | Trois textes entiers avec le relevé des interventions |

<p align="center">
  <img src="assets/carte-marqueurs.png" alt="Huit tics qui trahissent un texte écrit par une machine, avec leur correction" width="72%">
</p>

---

## Pourquoi Molière

> MONSIEUR JOURDAIN. — Non, vous dis-je, je ne veux que ces seules paroles-là dans le billet ; mais tournées à la mode, bien arrangées comme il faut.
> Molière, *Le Bourgeois gentilhomme*, acte II, scène 4, 1670

Monsieur Jourdain veut écrire « Belle Marquise, vos beaux yeux me font mourir d'amour ». Son maître
de philosophie lui propose la même phrase dans cinq ordres différents. Jourdain garde le premier.

Les mots étaient donnés, tout le travail portait sur leur ordre, et la meilleure version était celle
qui ne se remarquait pas. C'est le programme de ce dépôt.

---

## Le reste

| Fichier | Ce qu'il contient |
|---|---|
| [TECHNIQUE.md](TECHNIQUE.md) | Documentation des outils, des profils et des réglages |
| [CRITIQUE.md](CRITIQUE.md) | Douze points que l'auteur juge discutables, avec les réécritures proposées |
| [SOURCES.md](SOURCES.md) | Les sources, édition par édition. Une règle sans source est une opinion déguisée en méthode |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Le marqueur qui manque et le faux positif du linter sont les contributions les plus utiles |

## Licence

Les fichiers `.py` sont sous [MIT](LICENSE). La prose du skill, les exemples et la documentation
sont sous [CC BY 4.0](LICENSE-CONTENT) : réutilisez, modifiez, redistribuez, y compris
commercialement, en citant la source.

Les citations reproduites le sont à des fins de commentaire, avec attribution. Voir
[`SOURCES.md`](SOURCES.md).
