<!-- ./docker/README.md -->

# `./docker/` Folder

This is where the configuration for our shared machine lives. Changing anything
here affects everyone, think of this folder as how we orchestrate the project.

## The files

- **`Dockerfile.dev`** - the recipe for the developer machine. It starts from
  Python 3.12 and adds Git, curl, `uv` (Python package manager), and Node.js +
  pnpm (for JavaScript). This is the environment you and everyone else uses.
- **`docker-compose.yml`** - the orchestrator. It defines the `dev` service (one
  virtual machine) and wires up the code folder, the saved dependencies, and
  port 8080 for debugging. For this project, the single `dev` service runs
  everything.

You normally don't run anything here by hand, the Dev Containers extension
(see `../.devcontainer/`) reads these files for you.

## Ports

The backend is exposed on **port 8080**. The frontend reaches it at
`http://localhost:8080`.

## Changing these files

If you edit anything in this folder, **everyone must rebuild their container** to
get the change:

- `F1` -> `Dev Containers: Rebuild Container`

Tell the team in chat when you push a change here, so nobody is left on a stale
machine.