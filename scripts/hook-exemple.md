# Hook Claude Code, à activer soi-même

Ce dépôt ne livre aucun hook actif. Un hook s'exécute à chaque appel d'outil correspondant, chez celui qui l'installe, et personne n'a envie de découvrir ça après coup. La procédure est ici, la décision reste à vous.

## Ce que fait ce hook

À chaque fois que Claude écrit ou modifie un fichier `.md` ou `.txt`, le linter tourne et lui renvoie ses constats. Claude corrige avant de vous rendre la main, sans que vous ayez à demander la relecture.

C'est le seul moyen de rendre les règles de comptage réellement contraignantes : sans hook, le modèle estime au lieu de compter.

## Installation

Dans `~/.claude/settings.json` (portée globale) ou `.claude/settings.json` (portée projet) :

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/scripts/hook-moliere.sh"
          }
        ]
      }
    ]
  }
}
```

Puis créer `scripts/hook-moliere.sh`, exécutable :

```bash
#!/usr/bin/env bash
# Lance moliere_lint sur le fichier que Claude vient d'ecrire.
# Ne bloque jamais : il informe.
set -euo pipefail

fichier=$(jq -r '.tool_input.file_path // empty')
[[ -z "$fichier" ]] && exit 0
[[ "$fichier" != *.md && "$fichier" != *.txt ]] && exit 0
[[ ! -f "$fichier" ]] && exit 0

rapport=$(python3 "$CLAUDE_PROJECT_DIR/scripts/moliere_lint.py" \
            "$fichier" --profil post --json 2>/dev/null) || exit 0

echo "$rapport" | jq -r '
  .[0] as $r
  | ($r.constats | map(select(.severite == "bloquant" or .severite == "defaut"))) as $graves
  | if ($graves | length) == 0 then empty
    else "moliere_lint (score \($r.score)/100) : "
         + ($graves | map("\(.severite) · \(.message)") | join(" ; "))
    end'
```

```bash
chmod +x scripts/hook-moliere.sh
```

Le hook a besoin de `jq`. Il sort en code 0 dans tous les cas : il informe, il ne bloque pas.

## Le régler

- **Changer de profil.** Remplacer `--profil post` par `note`, `courriel` ou `proposition` selon ce que le dépôt contient.
- **Le rendre bloquant.** Ajouter `--strict` et sortir en code 2 quand le linter échoue. Claude reçoit alors le message comme une erreur et reprend son texte. À réserver aux dépôts dont tous les fichiers Markdown sont de la prose publiable : sur une documentation technique, il gênera plus qu'il n'aidera.
- **Le restreindre à un dossier.** Ajouter un test sur le chemin, par exemple `[[ "$fichier" != *"/contenu/"* ]] && exit 0`.

## Ce qu'il ne faut pas en faire

Ne pas l'activer globalement dans `~/.claude/settings.json` si vous écrivez du Markdown technique. Le linter est calibré pour de la prose française destinée à être lue par un humain, pas pour un fichier de configuration commenté ni pour un journal de modifications. Il produira du bruit, et le bruit fait qu'on cesse de lire.

La portée projet est presque toujours le bon choix.
