# Correcteurs externes

`moliere_lint.py` mesure le style et les marqueurs de rédaction automatique. Il ne connaît ni l'orthographe, ni les accords, ni la conjugaison. Deux correcteurs libres couvrent exactement ce qu'il laisse de côté.

Aucun des deux n'est une dépendance de ce dépôt. Le linter et l'autofixeur tournent sans eux.

---

## LanguageTool

Correcteur multilingue, module français riche, licence LGPL. C'est le plus simple à mettre en place et le plus complet sur les accords.

### En local, sans envoyer le texte à un tiers

```bash
# Java 17 ou plus requis
curl -LO https://languagetool.org/download/LanguageTool-stable.zip
unzip LanguageTool-stable.zip && cd LanguageTool-*
java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081
```

Puis, depuis un autre terminal :

```bash
curl -s --data-urlencode "text@mon-texte.md" \
     --data "language=fr" \
     http://localhost:8081/v2/check | python3 -m json.tool
```

### Filtrer le bruit

LanguageTool signale par défaut des choses que ce skill assume : anglicismes de métier admis, phrases longues, absence d'espaces insécables dans du Markdown. Désactiver les règles concernées plutôt que d'ignorer la sortie entière :

```bash
curl -s --data-urlencode "text@mon-texte.md" \
     --data "language=fr" \
     --data "disabledRules=FRENCH_WHITESPACE,ANGLICISME,PHRASE_LONGUE" \
     http://localhost:8081/v2/check
```

L'API publique (`https://api.languagetool.org/v2/check`) évite l'installation, au prix d'un envoi du texte à un service tiers et d'une limite de débit. À éviter pour un texte confidentiel.

---

## Grammalecte

Correcteur spécifiquement français, licence GPL. Plus fin que LanguageTool sur la syntaxe française et les faux amis, moins bien maintenu.

```bash
pip install grammalecte-fr
echo "Les données a été traitée." | grammalecte-cli.py -f - -ctx
```

Sortie en JSON pour un enchaînement :

```bash
grammalecte-cli.py -f mon-texte.md -j > rapport.json
```

Grammalecte accepte un dictionnaire personnel, utile pour les termes de métier que ce skill autorise (token, prompt, benchmark). Voir sa documentation pour le format.

---

## Hunspell, pour l'orthographe seule

Le plus léger des trois, si l'on ne veut que l'orthographe :

```bash
sudo apt install hunspell hunspell-fr
hunspell -d fr_FR -l mon-texte.md | sort -u
```

`-l` ne liste que les mots inconnus, un par ligne. Pratique pour repérer les coquilles sans lire un rapport.

---

## Ordre d'emploi conseillé

1. **`typo_fix.py`** en premier : il corrige le mécanique et réduit le bruit des deux suivants.
2. **Hunspell ou Grammalecte** ensuite : orthographe et accords. Un texte fautif ne mérite pas qu'on discute son rythme.
3. **`moliere_lint.py`** en dernier : style, marqueurs, rythme, ancrage.

L'inverse fait perdre du temps. On ne travaille pas la chute d'un texte qui contient trois fautes d'accord.

---

## Ce qu'aucun de ces outils ne fait

Aucun ne sait si le texte dit quelque chose. Le contrôle le plus rentable reste celui que le skill décrit sous le nom de test de l'auteur substituable, et il n'existe aucun moyen de l'automatiser : lire le texte et se demander si quelqu'un d'autre aurait pu le signer.
