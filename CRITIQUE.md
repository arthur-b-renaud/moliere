# Critique du skill

Ce fichier réunit les points que l'auteur juge discutables et qu'il n'a pas tranchés. Il n'existe pas par scrupule : un guide de style qui ne publie pas ses propres faiblesses invite le lecteur à croire qu'il n'en a pas.

Chaque entrée donne le défaut, la position actuelle, et la réécriture proposée. Ouvrir une issue pour en contester une.

---

## 1. La voix passive est interdite trop largement

**Position actuelle.** `phrase-francaise.md` §6 proscrit la voix passive systématique et `clinique.md` n° 13 la traite comme un défaut.

**Objection.** Le passif est parfois le seul choix correct. Quand l'agent est inconnu (« le corps a été retrouvé mardi »), quand il est indifférent (« la loi a été votée en 2019 »), quand la thématisation impose l'objet en tête, l'actif force à inventer un sujet ou à alourdir la phrase. Le français administratif abuse du passif, ce qui n'en fait pas une faute.

**Réécriture proposée.** Remplacer « pas de voix passive systématique » par un test : le passif est justifié quand l'agent est inconnu, indifférent, ou déjà connu du lecteur. Dans tous les autres cas, il masque une paresse.

---

## 2. Les points de suspension et l'exclamation sont interdits sans nuance

**Position actuelle.** `typographie.md` §2 réserve l'exclamation à la citation et déconseille les points de suspension. Le profil `post` autorise une exclamation par texte, ce qui est un rattrapage tardif.

**Objection.** Sur un post, les points de suspension marquent une hésitation qui peut être exactement l'effet cherché. L'exclamation dans un remerciement ou une annonce n'est pas un tic, c'est du registre.

**Réécriture proposée.** Traiter les deux comme des défauts de profil et non de langue : proscrits en `note` et `proposition`, tolérés une fois en `post` et `courriel`.

---

## 3. `SKILL.md` reste long

**Position actuelle.** Environ 1 650 mots, chargés en contexte à chaque déclenchement.

**Objection.** Une partie du contenu ne sert qu'à la lecture humaine : les tableaux de profils pourraient tenir en cinq lignes, la section sur l'articulation avec un skill de format est rarement utile.

**Ce qui a été fait.** Les redondances entre `SKILL.md` et les fichiers de références ont été supprimées : l'interdiction du participe présent apparaissait quatre fois dans la version d'origine, celle du cadratin également.

**Ce qui reste ouvert.** Faut-il descendre sous les mille mots, au prix d'un skill moins lisible pour l'humain qui l'installe ? Il n'existe aucune mesure de l'effet réel sur la qualité produite, donc aucune raison objective de trancher.

---

## 4. Le registre de presse repose sur deux titres

**Position actuelle.** `registre-presse.md` s'appuie sur *Les Echos* et *Le Monde*.

**Objection.** Deux titres de la presse nationale de qualité ne font pas une norme du français professionnel. Le registre décrit est celui d'une élite éditoriale parisienne. Un texte destiné à une revue technique, à une collectivité territoriale ou à un lectorat associatif n'en relève pas.

**Réécriture proposée.** Renommer le fichier et son ambition : ce n'est pas « le registre de la presse française », c'est « un registre d'analyse tenue ». Le fichier gagnerait à décrire ce qu'il fait plutôt qu'à invoquer une autorité.

---

## 5. Aucune variante régionale

**Position actuelle.** Le skill ne connaît que le français de France.

**Objection.** Les usages québécois, belges et suisses diffèrent sur des points que le skill traite comme absolus : la francisation des anglicismes (le Québec traduit là où la France emprunte), les nombres (septante, nonante), certaines tournures administratives. Un utilisateur québécois recevra des corrections qui vont contre l'usage de son lectorat, ce que le skill lui-même identifie comme la pire faute possible.

**Ce qu'il faudrait.** Un fichier `variantes.md` et un réglage de profil. Personne dans ce dépôt n'a la compétence pour l'écrire. Contribution recherchée.

---

## 6. Les listes de marqueurs ne sont pas mesurées

**Position actuelle.** `marqueurs-llm.md` donne des seuils chiffrés : « plus de deux items pour trois cents mots, le texte sonne artificiel ».

**Objection.** Ces seuils n'ont aucune base statistique. Ils viennent d'une lecture attentive, pas d'un corpus annoté. Les publier sous forme de nombres leur donne une autorité qu'ils n'ont pas.

**Réécriture proposée.** Soit constituer un corpus et mesurer, soit dire explicitement que les seuils sont empiriques. La seconde option a été retenue dans le README ; le fichier lui-même n'a pas encore été corrigé.

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
