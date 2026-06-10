<!-- ./.devcontainer/README.md  -->

# `./.devcontainer/` Folder

The **Dev Containers** VS Code extension lets everyone work inside the exact same
environment — same Python, same Node.js, same tools, no matter what laptop they
have. No more "it works on my machine."

## First time setup

1. Install Docker Desktop and the "Dev Containers" extension in VS Code.
2. Open this project folder in VS Code.
3. When prompted, click **"Reopen in Container"** (or open the command palette
   with `F1` and run `Dev Containers: Reopen in Container`).
4. Wait — the first build takes a few minutes. After that it's fast.

When it finishes, your terminal and editor are running *inside* the container.
Dependencies install automatically.

## When something breaks

If the container won't start, or tools seem missing or out of date, rebuild it:

- `F1` -> **`Dev Containers: Rebuild Container`**
- Still broken? `F1` -> **`Dev Containers: Rebuild Without Cache`** (slower, but
  fixes most problems).

## Adding tools

You can add VS Code extensions for everyone in `devcontainer.json`, or just
install them locally for yourself. Editor settings live in
`../.vscode/settings.json`.