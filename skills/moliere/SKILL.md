---
name: moliere
description: >-
  Écrire et réviser en français sans marqueurs de traduction ni tics de
  rédaction automatique. Profil par défaut : le post LinkedIn. Autres profils :
  note d'analyse, courriel, proposition commerciale. Use this skill for ANY
  substantial French text the user writes or asks to improve, such as a LinkedIn
  post, an article, a note d'analyse, a proposition commerciale, a courriel, a
  compte rendu, slide copy, or a report. Trigger also when the user says "ça
  fait trop américain", "on dirait une traduction", "c'est trop IA", "améliore
  le style", "relis-moi ça", "réécris en français correct", or when they reject
  a draft on style grounds. When a format skill also applies (post writer,
  proposal builder, deck builder), that skill governs structure and length while
  this one governs the language itself. Always consult before delivering French
  prose of more than three sentences.
license: CC-BY-4.0
---

# Molière

Un texte français réussi n'est pas un texte anglais traduit. La différence ne tient pas au vocabulaire mais à trois choses : la manière d'enchaîner les idées (connecteurs explicites contre juxtaposition), le rythme de la phrase (période contre staccato), et la retenue du ton (litote contre emphase).

Ce skill sert trois usages : rédiger, réviser, et épurer un texte marqué par une écriture automatique.

Le gras et les titres employés ci-dessous appartiennent à la consigne, jamais au texte livré. Ce que le skill s'autorise pour s'expliquer, il ne l'autorise pas dans ce qu'il produit.

## Choisir le profil

Le socle est commun : marqueurs de rédaction automatique, calques de l'anglais, verbes, rythme, typographie. Les profils n'assouplissent que ce qui les concerne. En l'absence d'indication, prendre `post`.

| Profil | Quand | Ce qui change |
|---|---|---|
| `post` (défaut) | LinkedIn, X, newsletter courte | « Je » autorisé, adresse au lecteur autorisée, staccato toléré une fois, paragraphes d'une à trois phrases, coupure du « voir plus » à surveiller. Lire `references/linkedin.md`. |
| `note` | Analyse, article, compte rendu | Distance, troisième personne, conditionnel journalistique, attribution des sources, litote. Lire `references/registre-presse.md`. |
| `courriel` | Message professionnel | Bref, registre tenu, une demande claire par message. Ni litote ni chute travaillée : on ne fait pas de style dans un courriel. |
| `proposition` | Offre, devis, réponse à appel d'offres | Verbe précis, chiffre opposable, engagement daté. Pas de litote : le client doit lire un engagement, pas une nuance. |

Si l'utilisateur ne dit pas quel texte il écrit, le déduire du contexte plutôt que de demander. Un texte de moins de trois cents mots destiné à être publié est un `post`.

## Procédure

### 1. Fixer le message essentiel

Avant d'écrire, formuler en une seule phrase ce que le lecteur doit retenir. Si la phrase n'arrive pas, le texte n'a pas d'angle et aucune qualité de style ne le sauvera.

L'angle consiste à ne traiter qu'un aspect d'une réalité forcément complexe. Un texte, une idée. Ce qui reste dehors est une réserve pour un autre texte.

### 2. Construire

Trois points portent le texte : l'attaque, la relance, la chute.

- **L'attaque** est la première phrase. Elle donne l'information la plus forte, une image concrète, un chiffre, une contradiction. Elle ne redit ni le titre ni le contexte, et ne commence jamais par une généralité (« Dans un monde où… », « À l'heure où… »).
- **La relance** est la phrase qui, au tiers du texte, remet de l'énergie quand l'attention retombe : une objection, un exemple précis, un changement d'échelle.
- **La chute** est la dernière phrase. Elle élargit, nuance ou tranche. Elle ne récapitule pas. Une chute qui commence par « En somme » ou « Retenez que » est une chute ratée.

Ordre par défaut : l'essentiel d'abord, le détail ensuite. Le lecteur qui s'arrête au tiers doit déjà savoir l'important.

### 3. Écrire

Six règles produisent l'essentiel de l'effet. Elles sont développées dans `references/phrase-francaise.md`, à lire avant de rédiger.

1. **Enchaîner par connecteurs logiques**, pas par juxtaposition. Le français articule (« or », « car », « donc », « d'où », « en revanche », « à ceci près que ») là où l'anglais aligne des phrases courtes et laisse le lecteur relier.
2. **Varier fortement la longueur des phrases.** Moyenne de quinze à vingt-cinq mots, écarts marqués. L'uniformité est le premier signe d'un texte automatique.
3. **Un verbe précis plutôt qu'une nominalisation.** « Procéder au déploiement de » devient « déployer ».
4. **Voix active**, sauf quand l'agent importe moins que l'objet.
5. **Un fait concret par paragraphe** : un chiffre, une date, un nom, un lieu. Le vague est le défaut le plus visible d'un texte généré.
6. **Litote plutôt qu'hyperbole**, sauf en profil `proposition`. « N'est pas sans conséquence » porte plus loin que « va tout changer ».

### 4. Réviser

Passer le texte à la grille ci-dessous. Sur un texte à enjeu, faire les passes séparément : chercher trois choses à la fois revient à n'en trouver aucune.

## Grille de contrôle

- [ ] Aucun marqueur de la liste noire (`references/marqueurs-llm.md`)
- [ ] Aucun participe présent en queue de phrase
- [ ] Aucune énumération à trois adjectifs
- [ ] Tirets cadratins traités (voir « Défauts forts » ci-dessous)
- [ ] Anglicismes et calques arbitrés (`references/marqueurs-llm.md`, section 6)
- [ ] Typographie conforme (`references/typographie.md`)
- [ ] Longueur des phrases variée, lue à voix haute sans reprendre son souffle
- [ ] Chaque phrase apporte une information que la précédente n'avait pas
- [ ] Attaque et chute travaillées séparément du reste
- [ ] Contraintes du profil respectées

## Règles de finition

Mécaniques, vérifiables en comptant. Elles s'appliquent en dernière passe.

Compter est précisément ce qu'un modèle de langue fait mal. Le dépôt fournit un contrôle déterministe : `python scripts/moliere_lint.py <fichier> --profil post`. Quand il est disponible, le lancer plutôt que d'estimer. Sinon, appliquer les règles à la main en sachant que le résultat sera approximatif.

1. **Attaque courte.** Sur un support qui tronque (LinkedIn, aperçu de courriel, résultat de recherche), la première phrase tient sous 150 caractères. Compter les caractères, pas les mots.
2. **La dernière phrase est plus courte que l'avant-dernière.** Règle purement rythmique, et le moyen le plus fiable de faire tomber une chute.
3. **Un fait opposable par argument.** Chaque paragraphe qui affirme porte un élément qu'un tiers pourrait vérifier ou contester. Un paragraphe sans prise est un paragraphe que personne ne discutera.
4. **Test de l'auteur substituable.** Si le texte pourrait être signé par n'importe quel professionnel du même secteur, il manque l'ancrage. Ajouter le détail que seul l'auteur peut écrire : ce qu'il a vu, mesuré, raté, facturé.
5. **Pas deux paragraphes ouverts de la même façon.** Alterner : sujet-verbe, connecteur, incise, groupe nominal.
6. **Un mot rare ne revient pas avant quarante mots.** La répétition rapprochée se remarque plus en français qu'en anglais, qui la tolère.
7. **Futur daté ou conditionné.** « Demain, X sera Y » n'engage personne. Écrire « d'ici 2027 » ou « si le prix continue de baisser ».
8. **Un seul concept nouveau par texte.** Deux formules à retenir s'annulent.
9. **Trois sigles non développés au maximum.**
10. **Aucun caractère Unicode de substitution.** Ni gras ni italique fabriqués avec des caractères mathématiques. Ils cassent les lecteurs d'écran.

## Deux règles absolues

Elles ne souffrent aucune exception, quel que soit le profil.

- **Jamais de participe présent en queue de phrase.** « Le dispositif réduit les coûts, permettant ainsi d'améliorer la marge » est un calque de l'anglais. Écrire : « Le dispositif réduit les coûts et améliore donc la marge. » C'est le marqueur le plus fiable d'une écriture assistée en français, et il n'a aucun emploi légitime.
- **Virgule décimale, jamais le point.** 1,3 milliard. Le point décimal est une faute de langue, pas une préférence.

## Défauts forts, avec leurs exceptions

Ces règles s'appliquent par défaut. Elles se lèvent pour un motif nommé, jamais par confort.

**Le tiret cadratin et le demi-cadratin.** À proscrire par défaut, pour une raison statistique et non typographique : depuis 2023, le cadratin en incise est devenu le marqueur qui trahit le plus vite une écriture assistée en français. Il ne s'agit pas d'une faute. Le *Lexique des règles typographiques en usage à l'Imprimerie nationale* prescrit d'ailleurs le tiret pour l'incise et pour le dialogue, et la littérature française en use depuis toujours. Mais un texte professionnel qui en porte trois sera lu comme généré, quel qu'en soit l'auteur. Remplacer par la virgule, les deux-points, la parenthèse ou le point.

Exceptions : le dialogue de fiction, la citation d'une œuvre existante, une convention typographique imposée par le support, et le cas où l'utilisateur demande explicitement de les garder.

**Le gras dans le corps du texte.** Sans objet sur LinkedIn, qui ne le rend pas. À proscrire dans un texte suivi, où l'emphase se construit par la syntaxe. Admis dans un rapport, une documentation ou un texte structuré en Markdown, où il sert au repérage et non à l'emphase.

**Les mots creux** : solution, dispositif, écosystème, accompagner, co-construire, levier, synergie, à 360°, robuste, incontournable. Proscrits comme remplissage. Admis quand ils sont le terme exact du domaine : le dispositif d'un jugement, une solution aqueuse, l'écosystème d'un lac. Le test est celui de la section 6 de `references/marqueurs-llm.md` : est-ce le mot que la profession emploie pour désigner cette chose précise, ou un mot qui pourrait désigner n'importe quoi ?

**Le staccato et la phrase d'un seul mot.** Proscrits en profil `note`, `courriel` et `proposition`. Tolérés une fois par texte en profil `post`, où le rythme court fait partie de la lecture au pouce. Deux fois, c'est un tic.

**Les abréviations de jargon** (éval, prop, config, spec, archi). Proscrites à l'écrit. Admises dans une citation d'oral rapportée telle quelle.

**Pas de français à tout prix.** Un terme technique que la profession emploie à l'oral se garde : token, prompt, roadmap, benchmark, framework, commit. Traduire contre l'usage produit un texte plus artificiel que l'anglicisme évité. Le test de décision et la liste indicative figurent dans `references/marqueurs-llm.md`, section 6.

## Écriture inclusive

Défaut du skill, réglable sur demande explicite de l'utilisateur.

- **Préférer les tournures épicènes et les collectifs** : « l'équipe de recherche » plutôt que « les chercheurs et les chercheuses », « le personnel soignant », « la clientèle », « les personnes candidates ».
- **Point médian proscrit par défaut.** Motif technique et non politique : les lecteurs d'écran le vocalisent mal, et il casse la recherche plein texte. Si l'utilisateur le demande, l'appliquer sans discuter.
- **Doublets complets admis quand ils sont courts** et qu'ils tombent naturellement : « celles et ceux », « toutes et tous ».
- **Accord de proximité** admis, sans le systématiser.
- Quand le genre d'une personne n'est pas connu, ne pas le supposer. Reformuler pour l'éviter.

## Fichiers de référence

Lire le fichier pertinent avant d'écrire, pas après.

| Fichier | Quand le lire |
|---|---|
| `references/phrase-francaise.md` | Toujours, avant de rédiger. Syntaxe, rythme, connecteurs, verbes, nominalisation, les conseils d'Eco. |
| `references/marqueurs-llm.md` | Toujours, avant de livrer. Liste noire lexicale, syntaxique et structurelle, calques et anglicismes autorisés. |
| `references/linkedin.md` | Profil `post`. Coupure du « voir plus », ce que la plateforme rend, longueur, hashtags, liens. |
| `references/typographie.md` | Dès qu'il y a des chiffres, des citations, des sigles, des titres ou des majuscules. |
| `references/registre-presse.md` | Profil `note`. Conditionnel journalistique, attribution des sources, distance, litote. |
| `references/clinique.md` | Pour réviser. Vingt réécritures commentées, du symptôme au remède. |
| `references/avant-apres.md` | Pour réviser un texte entier. Deux textes complets, avant et après, avec le relevé des interventions. |
| `references/corpus-voix.md` | Avant de rédiger au nom de quelqu'un. Textes validés par l'auteur, à imiter pour le rythme et la chute. |

## Trois modes

**Mode rédaction.** Fixer le message essentiel, écrire, réviser, livrer. Ne pas commenter le processus.

**Mode révision.** Livrer d'abord le texte corrigé, puis une liste courte des interventions, formulée par nature de défaut et non ligne par ligne (« nominalisations reprises », « trois calques de l'anglais », « rythme uniformisé cassé au deuxième paragraphe »). Ne jamais rendre un texte annoté : l'utilisateur veut un texte publiable, pas une copie corrigée.

**Mode épuration.** Quand un texte est correct sur le fond et seulement marqué par une écriture automatique, ne pas le réécrire. Retirer les marqueurs de `references/marqueurs-llm.md`, casser l'uniformité du rythme, remplacer un exemple générique par un fait daté. Toucher au plus une phrase sur trois, et conserver la structure et le vocabulaire de l'auteur partout ailleurs.

Si un choix est contestable, proposer deux variantes de la phrase concernée plutôt que d'imposer la sienne.

## Articulation avec un skill de format

Ce skill gouverne la langue. Un skill de format (rédacteur de posts, générateur de propositions, constructeur de présentations) gouverne la structure, la longueur et la voix. En cas de conflit, la règle de langue l'emporte, à une exception près.

**Exception : les signaux de voix.** Un auteur a souvent des formules de transition qui font partie de sa signature (« Ce que ça change concrètement : », « Ma conviction est la suivante : »). La liste noire les classe parmi les chapeaux annonciateurs, mais elles restent autorisées quand un skill de format les prescrit. Arbitrage retenu : **un seul signal par texte, jamais deux, jamais en ouverture de deux paragraphes consécutifs.** Employé une fois, il porte la voix. Employé deux fois, il la caricature. Et il n'a de valeur que si ce qui suit est effectivement concret : un acte, un coût, une décision. S'il introduit une généralité, le supprimer.

**Ordre de lecture** quand plusieurs skills se déclenchent : d'abord le skill de format, qui fixe la structure et la longueur ; ensuite celui-ci, qui écrit et révise ; jamais l'inverse.
