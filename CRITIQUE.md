# Critique du skill

Ce fichier réunit les points que l'auteur juge discutables et qu'il n'a pas tranchés. Il n'existe pas par scrupule : un guide de style qui ne publie pas ses propres faiblesses invite le lecteur à croire qu'il n'en a pas.

Chaque entrée donne le défaut, la position actuelle, et la réécriture proposée. Ouvrir une issue pour en contester une.

---

## 1. La voix passive est interdite trop largement

**Position actuelle.** `STYLE.md` §4 privilégie l'actif et `exemples-phrases.md` n° 13 traite le passif comme un défaut. `references/fautes.md` §8 le réhabilite en partie, ce qui laisse le dépôt à deux voix.

**Objection.** Le passif est parfois le seul choix correct. Quand l'agent est inconnu (« le corps a été retrouvé mardi »), quand il est indifférent (« la loi a été votée en 2019 »), quand la thématisation impose l'objet en tête, l'actif force à inventer un sujet ou à alourdir la phrase. Le français administratif abuse du passif, ce qui n'en fait pas une faute.

**Réécriture proposée.** Remplacer « pas de voix passive systématique » par un test : le passif est justifié quand l'agent est inconnu, indifférent, ou déjà connu du lecteur. Dans tous les autres cas, il masque une paresse.

---

## 2. Les points de suspension restent interdits sans nuance

**Position actuelle.** `typographie.md` §2 réserve l'exclamation à la citation et déconseille les points de suspension. Le profil `post` autorise une exclamation par texte.

**Ce qui a été fait.** L'exclamation est devenue un défaut de support et non de langue, réglé par les profils.

**Ce qui reste ouvert.** Les points de suspension sortent toujours en alerte quel que soit le support. Sur une publication, ils marquent une hésitation qui peut être exactement l'effet cherché. Le contrôle devrait suivre le profil, comme l'exclamation.

---

## 3. Le poids du skill s'est déplacé, il n'a pas disparu

**Position actuelle.** 541 mots de corps et 109 mots de description, contre 2 308 dans la version d'origine.

**Ce qui a été fait.** `SKILL.md` est devenu une porte d'entrée : ce que fait le skill, où aller, quels outils. Les règles sont descendues dans `STYLE.md`, qui n'est lu qu'au moment d'écrire.

**Ce qui reste ouvert.** Le poids total n'a pas diminué, il s'est déplacé. Un agent qui rédige lit `SKILL.md` puis `STYLE.md`, soit environ 2 400 mots, contre 2 308 auparavant. Le gain est réel pour les sessions où le skill se déclenche sans qu'on écrive, et nul pour les autres. Personne n'a mesuré la proportion.

---

## 4. Le registre décrit reste celui d'une élite éditoriale

**Ce qui a été fait.** Le fichier `registre-presse.md`, qui s'appuyait sur *Les Echos* et *Le Monde*, a été supprimé. Sa déontologie est passée dans `STYLE.md` §5 et sa distance dans `supports.md`, sans invoquer d'autorité.

**Ce qui reste ouvert.** Le registre décrit reste celui du français professionnel parisien. Un texte destiné à une revue technique, à une collectivité territoriale ou à un lectorat associatif n'en relève pas, et le dépôt ne le dit nulle part.

---

## 5. Aucune variante régionale

**Position actuelle.** Le skill ne connaît que le français de France.

**Objection.** Les usages québécois, belges et suisses diffèrent sur des points que le skill traite comme absolus : la francisation des anglicismes (le Québec traduit là où la France emprunte), les nombres (septante, nonante), certaines tournures administratives. Un utilisateur québécois recevra des corrections qui vont contre l'usage de son lectorat, ce que le skill lui-même identifie comme la pire faute possible.

**Ce qu'il faudrait.** Un fichier `variantes.md` et un réglage de profil. Personne dans ce dépôt n'a la compétence pour l'écrire. Contribution recherchée.

---

## 6. Les listes de marqueurs ne sont pas mesurées

**Position actuelle.** `marqueurs.md` donne des seuils chiffrés : « plus de deux items pour trois cents mots, le texte sonne artificiel ».

**Objection.** Ces seuils n'ont aucune base statistique. Ils viennent d'une lecture attentive, pas d'un corpus annoté. Les publier sous forme de nombres leur donne une autorité qu'ils n'ont pas.

**Ce qui a été fait.** Le fichier le dit désormais lui-même, en clair, à la fin de sa section 5.

**Ce qui reste ouvert.** Le dire ne le corrige pas. Il faudrait constituer un corpus annoté et mesurer les fréquences réelles. C'est la contribution la plus utile que ce dépôt puisse recevoir.

---

## 7. Le linter produit des faux positifs, par construction

**Position actuelle.** Trois contrôles reposent sur des heuristiques et se trompent :

- **Participe présent en queue.** La détection repose sur une liste de mots en `-ant` qui ne sont pas des participes. Elle est incomplète et le restera.
- **Énumération ternaire.** Un mot est jugé adjectif d'après son suffixe. « Nous concevons, industrialisons et maintenons » échappe à la détection, à raison ; d'autres cas passeront à tort.
- **Répétition rapprochée.** Le seuil de neuf lettres écarte les répétitions volontaires en parallélisme (« un projet qui échoue… qu'un projet qui réussit »), mais laisse passer des répétitions légitimes de termes techniques.

**Position assumée.** Un linter de style sans faux positif serait un linter qui ne trouve rien. Le compromis retenu : les heuristiques incertaines sortent en `alerte`, jamais en `bloquant`, et le message donne toujours le texte incriminé pour qu'un humain arbitre.

**Ce qui aiderait.** Signaler les faux positifs avec le texte qui les déclenche. C'est la contribution la plus utile au dépôt.

---

## 8. Le score sur 100 est une commodité, pas une mesure

**Position actuelle.** Le linter rend un score, calculé en retranchant un poids fixe par constat.

**Objection.** Rien ne justifie qu'un tiret cadratin vaille six points et une énumération ternaire six aussi. Le score est un raccourci de lecture, pas une grandeur. Deux textes à 80 ne sont pas comparables.

**Position assumée.** Le score sert à voir une progression sur un même texte et à poser un seuil en intégration continue. Ne pas en faire autre chose. Les constats individuels sont la vraie sortie du linter.

---

## 9. Le nom du skill n'indique pas sa fonction

**Position actuelle.** `moliere`.

**Objection.** Un skill se déclenche sur sa description, pas sur son nom, donc le coût fonctionnel est nul. Mais dans une liste de skills, `moliere` ne dit rien à qui ne connaît pas le dépôt.

**Position assumée.** Le nom est gardé. Un dépôt public a besoin d'un nom qui se retienne autant que d'un nom qui décrive, et la description du skill fait tout le travail de déclenchement.

---

## 10. Le mode épuration reste flou

**Position actuelle.** « Toucher au plus une phrase sur trois. »

**Objection.** Le chiffre a été ajouté pour remplacer un « avec le moins de modifications possible » qui n'engageait à rien. Il n'est pas plus fondé : une phrase sur trois sur un texte de six phrases n'a pas le même sens que sur un texte de soixante.

**Ce qu'il faudrait.** Un budget de modification exprimé en distance d'édition, mesuré par un script. Personne ne l'a écrit.

---

## 11. Le retrait du corpus rend l'imitation de voix volatile

**Ce qui a été fait.** Le fichier `corpus-voix.md`, livré vide et présenté comme le plus important du dépôt, a été supprimé. Un skill qui exige d'être édité avant de servir n'est pas distribuable : le clone devient sale et le premier `git pull` produit un conflit.

**Le prix.** La voix ne se calibre plus que sur ce que l'utilisateur colle dans la conversation, et rien ne survit d'une session à l'autre. Celui qui écrit tous les jours au nom de la même personne devra recoller ses exemples chaque fois.

**Ce qui n'a pas été fait.** Un mécanisme de persistance hors du dépôt, dans le fichier de mémoire personnel de l'utilisateur. Cela reste possible et ne demanderait qu'une ligne de documentation, mais cela réintroduirait une notion de configuration, que ce dépôt a choisi d'écarter.

---

## 12. Le renversement sur les anglicismes déplace une frontière que personne n'a mesurée

**Ce qui a été fait.** Le skill ne fait plus la chasse aux anglicismes. Il corrige les constructions fautives ou imprécises, garde les emprunts que la profession emploie, et tranche le reste par une question d'usage. Les entrées `digital` et `impacter` ont été retirées de la liste des calques du linter.

**L'objection.** Ce déplacement repose sur un jugement, pas sur une mesure. Un lectorat administratif, universitaire ou institutionnel jugera le résultat trop relâché, et il aura ses raisons. La règle « est-ce le mot que la profession emploie à l'oral » suppose en outre qu'on connaisse la profession du lecteur, ce qui n'est pas toujours le cas.

**Position assumée.** Une prescription de vocabulaire qui va contre l'usage d'un métier produit un texte plus artificiel que l'emprunt qu'elle évite. Mais la frontière bouge d'année en année, et ce fichier ne prétend pas la fixer.
