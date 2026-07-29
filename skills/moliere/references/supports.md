<!-- moliere-lint: contre-exemples -->

# Ce que le support change

Le style ne change pas d'un support à l'autre. La longueur, la distance au lecteur et la place de
l'information changent. Ce fichier ne traite que ces trois points ; tout le reste est dans
`STYLE.md` et s'applique partout.

Trois supports, qui correspondent aux trois profils du linter.

| Profil | Ce qu'il couvre |
|---|---|
| `document` | Devis, proposition commerciale, note d'analyse, rapport, compte rendu. Plusieurs pages. Un courriel est un document court : mêmes règles, en trois paragraphes |
| `post` | Publication sur un réseau professionnel, billet court, message de communauté |
| `presentation` | Slides, quel que soit l'outil |

En l'absence d'indication, prendre `document`. Un texte de moins de trois cents mots destiné à
être publié est un `post`.

---

## 1. Document

**Le plan est apparent.** Un lecteur qui ouvre une proposition de douze pages n'en lit d'abord que
les titres. Chaque titre annonce ce que la section démontre, non le thème qu'elle aborde : « Le
délai tient si la recette démarre en mars », pas « Planning ».

**L'essentiel d'abord, à chaque échelle.** Celui qui s'arrête au tiers d'une section doit déjà
savoir l'important. Cela vaut pour le document, pour la section, pour le paragraphe.

**Distance.** Troisième personne, tournures impersonnelles qui laissent le fait parler : reste que,
encore faut-il, on peine à voir. Le « je » est possible dans une note signée, mais il arrive tard,
une fois le fait posé, et jamais dans la première phrase. Pas d'apostrophe au lecteur, pas de
« nous » inclusif, pas d'impératif d'exhortation.

**Attribution systématique.** Chaque fait qui n'est pas de notoriété publique porte sa source dans
la phrase et non en note.

**Un devis ou une proposition engagent.** Verbe précis, chiffre opposable, date. Un livrable se
décrit par ce qu'il permettra de faire, jamais par la méthode employée pour le produire. Pas de
litote : le client doit lire un engagement, pas une nuance. Écrire « la recette est livrée le
14 mars » et non « nous nous efforcerons de livrer dans les meilleurs délais ».

**Le gras est admis dans un document structuré**, où il sert au repérage et non à l'emphase. Il ne
remplace jamais une phrase bien construite.

Longueur d'un paragraphe : trois à six phrases. Deux paragraphes d'une phrase à la suite signalent
un plan qui n'a pas été fait.

## 2. Publication

**La coupure.** Les réseaux tronquent le texte au bout de quelques lignes et affichent un lien
pour lire la suite. Sur mobile, la coupure tombe vers 140 caractères ; sur un écran large, vers
210. Écrire pour 140. Tout ce qui doit décider le lecteur à déplier tient avant.

Ces valeurs sont observées, elles ne sont documentées par aucune plateforme, et elles bougent.

**L'attaque porte un fait, pas une intention.** Pas de question rhétorique, pas de généralité sur
l'époque, aucune phrase commençant par « Dans un monde où » ou « À l'heure où ». Le fait le plus
fort, ou la contradiction, en tête.

**Le « je » qui raconte contre le « je » qui se félicite.** « Nous avons perdu onze candidats sur
douze avant l'entretien » est une information. « Je suis fier d'annoncer » n'en est pas une. Le
premier engage celui qui écrit, le second demande une félicitation.

**L'adresse au lecteur est autorisée quand elle informe**, jamais quand elle remplit. « Vérifiez le
délai entre la candidature et votre première réponse » donne une tâche. « Vous l'aurez compris » ne
donne rien.

**Ce que la plateforme ne rend pas** : ni gras, ni italique, ni titre, ni tableau, ni note de bas
de page. Le gras fabriqué en caractères mathématiques Unicode s'affiche, mais il casse les lecteurs
d'écran et se copie mal. Ne pas l'employer.

**Longueur.** La limite dure est de 3 000 caractères. La zone utile va de 600 à 1 500. Paragraphes
d'une à trois phrases, séparés par une ligne vide, parce que la lecture se fait au pouce.

**Une phrase d'un seul mot est tolérée une fois.** Deux fois, c'est un tic.

**Hashtags** : trois au maximum, précis, en fin de texte. Les hashtags génériques du type
`#innovation` ou `#motivation` n'apportent rien.

**Les liens.** La croyance selon laquelle un lien sortant réduit la portée est plausible mais n'a
jamais été démontrée publiquement. Mettre le lien où il sert le lecteur, et ne pas construire un
texte autour d'une superstition de plateforme.

## 3. Présentation

C'est le support le plus mal servi par les modèles, parce qu'ils y écrivent de la prose.

**Le titre porte le message, pas le sujet.** C'est la règle qui change tout. Un titre affirmatif
permet de lire le jeu de slides en ne lisant que les titres.

> Analyse des coûts de maintenance
> Les coûts de maintenance ont baissé de 12 % depuis mars

**Une idée par slide.** Si le titre porte deux verbes, il y a deux slides.

**Pas de phrase complète dans le corps.** Une puce n'est pas une phrase : ni verbe conjugué
superflu, ni point final. Groupes nominaux, ou propositions courtes.

> • Nous avons constaté que les délais de réponse étaient trop longs.
> • Délai de réponse : 23 jours

**Douze mots par puce au maximum**, quatre à six puces par slide. Au-delà, la slide est un document
et il faut la traiter comme tel.

**Les puces d'une même liste sont parallèles de construction.** Toutes des groupes nominaux, ou
toutes des verbes à l'infinitif. Mélanger les deux se voit immédiatement.

**La prose va dans les notes**, pas sur la slide. Ce qui se dit à l'oral n'a pas à être lu à
l'écran, et une slide que l'orateur lit à voix haute rend l'orateur inutile.

**Les chiffres sont rapportés.** « 12 % » ne dit rien. « 12 %, contre 4 % l'an dernier » dit
quelque chose. La règle du fait comparé vaut ici plus qu'ailleurs, faute de place pour nuancer.

Ce qui ne s'applique pas à une présentation : l'attaque, la chute, la variation du rythme, la
longueur de phrase. Une slide n'a pas de rythme. Le linter en tient compte et ne contrôle pas ces
points en profil `presentation`.
