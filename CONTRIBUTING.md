# Contribuer

Le dépôt est petit et le restera. Les contributions utiles le sont beaucoup, les autres alourdissent un skill dont le coût se paie en contexte à chaque appel.

## Ce qui aide, par ordre d'utilité

### 1. Un marqueur qui manque

C'est ce qui fait vieillir le dépôt le mieux : les tics des modèles changent tous les six mois. Une bonne proposition contient :

- le marqueur, formulé comme les autres entrées de `references/marqueurs-llm.md`
- **un exemple réel**, pas une reconstitution
- la correction, écrite
- si possible, la fréquence observée

Une entrée sans exemple sera refusée. Une liste noire qui grossit sans preuve devient une superstition.

### 2. Un faux positif du linter

Un linter qui crie à tort est un linter qu'on désactive, et c'est le pire résultat possible. Ouvrir une issue avec :

- le texte exact qui déclenche le constat
- la commande lancée
- pourquoi le constat est faux

Les heuristiques connues comme faillibles sont recensées dans `CRITIQUE.md`, point 7. Ajouter un cas à cette liste est déjà une contribution.

### 3. Une variante régionale

Le skill ne connaît que le français de France, ce qui est un défaut assumé et documenté. Un fichier `references/variantes.md` couvrant les usages belges, suisses ou québécois serait la contribution la plus utile du dépôt. Personne ici n'a la compétence pour l'écrire.

Ce qu'il faudrait y traiter : la francisation des anglicismes, où le Québec traduit là où la France emprunte ; les nombres ; les tournures administratives ; ce que le profil `post` change selon le lectorat.

### 4. Une contestation argumentée

Les dix points ouverts sont dans `CRITIQUE.md`. Une contestation utile donne un contre-exemple, pas une préférence.

## Ce qui n'aide pas

- Allonger les listes sans exemple.
- Ajouter des citations. Le README en porte assez, et le skill n'en veut qu'une.
- Traduire le dépôt en anglais. L'objet est le français ; l'encart anglais du README suffit à situer.
- Ajouter une dépendance. Les scripts tournent sur une installation Python nue, et c'est une contrainte, pas un hasard.

## Le contrôle avant de proposer

```bash
python3 scripts/moliere_lint.py exemples/post-apres.md --profil post --seuil 90 --strict
python3 scripts/moliere_lint.py exemples/note-apres.md --profil note --seuil 90 --strict
python3 scripts/moliere_lint.py skills/ --controles typo --profil note --seuil 85 --strict
python3 scripts/typo_fix.py skills/ exemples/post-apres.md exemples/note-apres.md
python3 -m compileall -q scripts/
```

L'intégration continue lance exactement ces commandes. Si vous touchez au linter, vérifiez aussi que les versions marquées restent détectées sous 70 : un linter qui laisse passer `exemples/post-avant.md` ne sert plus à rien.

## Style des contributions

Le dépôt écrit en français et s'applique ses propres règles. Les fichiers de références qui contiennent des contre-exemples portent en tête :

```markdown
<!-- moliere-lint: contre-exemples -->
```

Les scripts sont en ASCII dans le code et les messages, pour éviter les surprises d'encodage sur les terminaux mal configurés. La prose, elle, est accentuée normalement.

## Licence des contributions

En proposant une contribution, vous acceptez qu'elle soit publiée sous les licences du dépôt : MIT pour `scripts/`, CC BY 4.0 pour la prose. Voir `LICENSE` et `LICENSE-CONTENT`.
