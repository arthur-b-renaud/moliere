# Le post LinkedIn

Profil `post`. Ce fichier ne traite que des contraintes de la plateforme. Tout ce qui touche à la langue reste régi par `phrase-francaise.md` et `marqueurs-llm.md`.

Sommaire : 1. La coupure. 2. Ce que la plateforme ne rend pas. 3. Le « je ». 4. Longueur et paragraphes. 5. Liens et hashtags. 6. Ce qui change par rapport au registre de presse. 7. Ce qui ne change pas.

Avertissement : les valeurs chiffrées de ce fichier sont observées, pas documentées par LinkedIn, et elles bougent. Les traiter comme des ordres de grandeur.

---

## 1. La coupure

Le feed tronque le texte et le remplace par « … voir plus ». La coupure tombe vers 140 caractères sur mobile et vers 210 sur ordinateur. Écrire pour 140.

Trois conséquences, dans l'ordre d'importance :

1. **La première phrase est le texte.** Le reste est un clic. Tout ce que le lecteur doit savoir pour décider de déplier tient avant la coupure.
2. **Le premier saut de ligne compte double.** Une première ligne courte suivie d'une ligne blanche laisse le regard tomber, et la coupure arrive plus loin dans le texte utile.
3. **Rien d'important après le troisième paragraphe.** Le taux de dépliement chute, et le taux de lecture jusqu'au bout encore plus.

Le contrôle mécanique de l'attaque figure dans `SKILL.md`, règle de finition 1, et se vérifie avec `scripts/moliere_lint.py --profil post`.

Ce que la coupure interdit en pratique : commencer par le contexte, par une définition, par une généralité sur l'époque, ou par une formule de politesse. Le lecteur ne dépliera pas pour aller chercher l'information.

## 2. Ce que la plateforme ne rend pas

LinkedIn n'interprète aucun balisage. Ni gras, ni italique, ni titre, ni liste à puces native, ni tableau, ni note de bas de page.

Conséquences pratiques :

- **Écrire `**mot**` produit `**mot**` à l'écran.** Le balisage Markdown reste visible et signe l'automatisme.
- **Ne jamais fabriquer du gras avec des caractères mathématiques Unicode.** Les lecteurs d'écran les vocalisent lettre par lettre ou les ignorent, et certains appareils affichent des carrés vides. C'est une règle d'accessibilité, pas de goût.
- **Les puces se font au caractère**, sobrement, en début de ligne. Une liste de plus de cinq items dans un post devient un tableau que personne ne lit.
- **Pas d'emoji en tête de puce.** C'est le marqueur visuel du post généré.
- **L'emphase se porte par la syntaxe**, par la position du mot dans la phrase et par la longueur de la phrase qui le contient. C'est plus difficile et c'est le sujet même de ce skill.

## 3. Le « je »

C'est la différence de fond avec le profil `note`. `registre-presse.md` proscrit le « je » en ouverture et l'adresse au lecteur. Sur LinkedIn, les deux sont autorisés, sous une condition.

**Le « je » qui raconte est autorisé. Le « je » qui se félicite ne l'est pas.**

- Autorisé : « J'ai facturé ce diagnostic 4 000 euros et je l'ai raté. » Un fait, daté, coûteux, vérifiable par celui qui l'a vécu.
- Autorisé : « Je ne comprends toujours pas pourquoi cette architecture tient. »
- Proscrit : « Je suis fier de vous annoncer », « Ravi d'avoir partagé », « Humblement, je crois que ».
- Proscrit : le récit d'humilité fabriqué, qui pose une réussite en la déguisant en leçon.

Même test pour l'adresse au lecteur. « Si vous avez déjà repris une base de code en 2005, vous savez ce qui suit » est une adresse qui informe. « Vous l'aurez compris » et « Posez-vous la question » sont des remplissages, proscrits partout, y compris ici.

## 4. Longueur et paragraphes

- **Limite dure : 3 000 caractères.** Longueur utile : entre 600 et 1 500. Au-delà, le texte appelle un article, pas un post.
- **Un paragraphe fait une à trois phrases.** Le mur de texte n'est pas lu au pouce.
- **Une ligne blanche entre chaque paragraphe.** C'est la seule mise en forme dont on dispose.
- **Le staccato est toléré une fois par texte**, en chute ou en relance. Une seule. Trois frappes courtes d'affilée produisent le post traduit de l'américain que ce skill sert précisément à éviter.

## 5. Liens et hashtags

**Les hashtags.** Trois au maximum, à la fin, en minuscules sauf pour les noms propres. Un hashtag placé au milieu d'une phrase la casse à la lecture. Les hashtags génériques (#innovation, #digital, #motivation) ne servent à rien et signent le post automatique.

**Les liens.** La croyance selon laquelle un lien sortant dans le corps du post ferait chuter la portée circule partout et n'est confirmée par aucune source officielle. Elle est plausible, jamais démontrée. Position retenue : mettre le lien où il sert le lecteur, et le mentionner explicitement s'il est en commentaire (« lien en commentaire » sans autre cérémonie). Ne pas construire un texte entier autour d'une superstition de portée.

**Les mentions.** Mentionner une personne ou une organisation qui n'a pas de rapport avec le texte est du démarchage. Elle le lira comme tel.

## 6. Ce qui change par rapport au registre de presse

| Point | `note` | `post` |
|---|---|---|
| Le « je » | Tard dans le texte, jamais en ouverture | Autorisé partout, s'il raconte |
| Adresse au lecteur | Proscrite | Autorisée si elle informe |
| Staccato | Proscrit | Une fois par texte |
| Phrase d'un seul mot | Proscrite | Une fois, en chute |
| Gras | Proscrit | Sans objet, la plateforme ne le rend pas |
| Litote | Recommandée | Recommandée, mais une seule suffit |
| Attribution des sources | Systématique | Sur les chiffres et les faits d'actualité |
| Conditionnel journalistique | Obligatoire | Obligatoire, c'est une règle déontologique |
| Point d'exclamation | Proscrit | Un par texte au maximum, jamais deux |
| Longueur des paragraphes | Libre | Une à trois phrases |

## 7. Ce qui ne change pas

Le profil `post` assouplit le registre, pas la langue. Restent applicables sans exception :

- Les deux règles absolues (participe présent en queue, virgule décimale).
- Toute la liste de `marqueurs-llm.md`, sections 1 à 5.
- Le conditionnel journalistique sur une information non confirmée. Un post qui annonce au présent une opération non signée engage son auteur, et LinkedIn ne protège personne.
- L'exigence de fait opposable : un chiffre, une date, un nom. C'est encore plus vrai ici qu'ailleurs, parce que le format récompense l'affirmation vague et que c'est précisément ce qui rend les posts interchangeables.
- La typographie française. La plateforme n'insère pas les espaces insécables, mais rien n'empêche de les écrire.

Une dernière chose que le format ne pardonne pas : le post qui pourrait être signé par n'importe qui. Sur un feed, c'est la seule faute qui se voit à un mètre.
