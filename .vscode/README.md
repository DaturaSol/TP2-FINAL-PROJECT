<!-- ./.vscode/README.md  -->

# `./.vscode/` Folder

Here live the VS Code settings, launch options, and other configurations.

These apply to everyone who opens the project, so the whole team gets the same
formatting, linting, and type-checking behavior automatically. The Python
settings here assume you are working **inside the dev container** (see
`../.devcontainer/`).

- **Formatting & linting** is handled by Ruff (format on save is on).
- **Type checking** is handled by Pylance + mypy.

If you want a personal tweak that shouldn't affect the team, change it in your
own VS Code user settings instead of this file.