<!-- ./src/front_end/README.md -->
# `./src/front_end/` Folder

This is where the JavaScript code for the frontend lives. Treat it as its own
mini-project, separate from the backend.

## You don't need to know Python

Nothing in here touches Python. You work only inside this folder. Ignore
`back_end/`, `.venv/`, and anything `.py`.

## First time? Do this

Open a terminal **inside the dev container** (VS Code does this automatically
when you "Reopen in Container"), then:

```bash
cd src/front_end
pnpm install      # downloads the packages listed in package.json
```

`pnpm` is already installed in the container — you don't install it yourself.

## Running things

```bash
pnpm dev          # starts the dev server (once the team sets one up)
```

Right now `pnpm dev` just prints a reminder, because the team hasn't picked a
framework yet. When you do (Vite, plain HTML, etc.), wire it into the `"dev"`
script in `package.json` and update this file.

## Talking to the backend

The backend runs on **port 8080** (see `docker/docker-compose.yml`). When you
fetch data, point your requests at `http://localhost:8080`.

## What NOT to do

- Don't edit files in `back_end/` or `data/` — those are the backend's.
- Don't commit the `node_modules/` folder (it's ignored automatically).