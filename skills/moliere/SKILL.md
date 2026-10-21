---
name: moliere
description: >-
  Écrire et réviser en français contemporain, sans marqueurs de traduction ni
  tics de rédaction automatique. Use this skill for ANY substantial French text
  the user writes or asks to improve: documents of several pages (devis,
  proposition commerciale, note, rapport), publications courtes, slides et
  présentations. Trigger also when the user says "ça fait trop américain", "on
  dirait une traduction", "c'est trop IA", "améliore le style", "relis-moi ça",
  "réécris en français correct", or when they reject a draft on style grounds.
  When a format skill also applies, that skill governs structure and length
  while this one governs the language itself. Always consult before delivering
  French prose of more than three sentences.
license: CC-BY-4.0
---

# Molière

Un texte français réussi n'est pas un texte anglais traduit. La différence ne tient pas au
vocabulaire mais à l'ordre des mots, à l'enchaînement des propositions, au choix du verbe et à la
variation du rythme.

Ce skill sert trois usages : rédiger, réviser, et épurer un texte marqué par une écriture
automatique. Il ne demande aucune configuration et aucun fichier à remplir.

## Comment l'utiliser

**Lire `STYLE.md` avant d'écrire.** C'est la seule instruction obligatoire. Ce fichier contient
toutes les règles et se suffit à lui-même.

Puis ouvrir la référence utile, jamais après coup :

| Fichier | Quand le lire |
|---|---|
| `STYLE.md` | Toujours, avant de rédiger comme avant de réviser |
| `references/supports.md` | Dès qu'on sait ce qu'on écrit : document, publication, présentation |
| `references/marqueurs.md` | Avant de livrer. La liste noire des tics de rédaction automatique |
| `references/fautes.md` | En révision. Les fautes de français que les modèles commettent |
| `references/typographie.md` | Dès qu'il y a des chiffres, des citations, des sigles ou des majuscules |
| `references/exemples-phrases.md` | Pour réviser une phrase. Réécritures commentées, du symptôme au remède |
| `references/exemples-textes.md` | Pour réviser un texte entier. Trois textes complets, avant et après |
| `references/paires-arthur.md` | Seulement pour un texte signé Arthur Renaud, et alors en premier. Quarante-six réécritures, avec leurs motifs |

Le gras et les titres employés dans ces fichiers appartiennent à la consigne, jamais au texte
livré. Ce que le skill s'autorise pour s'expliquer, il ne l'autorise pas dans ce qu'il produit.

## Trois modes

**Rédaction.** Fixer en une phrase ce que le lecteur doit retenir, écrire, réviser, livrer. Ne pas
commenter le processus.

**Révision.** Livrer d'abord le texte corrigé, puis une liste courte des interventions par nature
de défaut et non ligne par ligne : « nominalisations reprises », « trois calques de l'anglais »,
« rythme uniformisé cassé au deuxième paragraphe ». Ne jamais rendre un texte annoté.

**Épuration.** Quand le fond est bon et que seule l'écriture sent la machine, ne pas réécrire.
Retirer les marqueurs, casser l'uniformité du rythme, remplacer un exemple générique par un fait
daté. Toucher au plus une phrase sur trois, et conserver partout ailleurs la structure et le
vocabulaire de l'auteur.

Si un choix est contestable, proposer deux variantes de la phrase concernée plutôt que d'imposer
la sienne.

## Écrire au nom de quelqu'un

Si la conversation contient des textes de l'auteur, ou s'il en désigne, les lire pour la mécanique :
ce que fait l'attaque, comment la chute retombe, où se trouve la rupture de rythme. Jamais pour le
fond ni pour les idées.

Sinon, écrire en français neutre, et ne rien réclamer.

**Quand le texte est signé Arthur Renaud**, lire `references/paires-arthur.md` avant `STYLE.md` :
ce sont ses propres corrections de phrases de modèle, et elles priment en cas de conflit. Elles
tranchent notamment le ternaire, « impacter » et les expressions idiomatiques. Pour tout autre
auteur, ignorer ce fichier.

## Les outils

**Les scripts vérifient, ils ne sont jamais nécessaires.** Le skill fonctionne entièrement sans
Python. Ils servent à mesurer ce qu'un modèle de langue compte mal, et rien d'autre.

| Script | Ce qu'il fait |
|---|---|
| `scripts/moliere_lint.py` | Mesure. Ne corrige rien et ne juge pas le style |
| `scripts/typo_fix.py` | Corrige le mécanique et le réversible. Ne touche jamais au style |
| `scripts/courbe_rythme.py` | Trace la longueur des phrases en SVG |

```bash
python3 scripts/moliere_lint.py fichier.md --profil document|post|presentation
python3 scripts/typo_fix.py fichier.md --ecrire
```

Quand ils sont disponibles, les lancer plutôt que d'estimer. Sinon, appliquer les règles à la main
en sachant que le compte sera approximatif.
