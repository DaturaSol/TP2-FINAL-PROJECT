<!-- ./src/front_end/README.md -->
# `./src/front_end/` Folder

This is where the JavaScript code for the frontend lives. Treat it as its own
mini-project, separate from the backend.

## Tech Stack Overview

This frontend uses a lightweight, modern web stack:

- **Vite:** Lightning-fast build tool and development server.
- **Vanilla JavaScript:** Native ES modules without the overhead of heavy UI frameworks.
- **PostCSS:** Used for CSS processing, allowing nested CSS (via `postcss-nesting`) and automatically adding vendor prefixes.
- **ESLint & Prettier:** Ensures consistent code style and catches syntax errors early.

## You don't need to know Python

Nothing in here touches Python. You work only inside this folder. Ignore
`back_end/`, `.venv/`, and anything `.py`.

## First time? Do this

Open a terminal **inside the dev container** (VS Code does this automatically
when you "Reopen in Container"), then:

```bash
cd src/front_end
npm install --legacy-peer-deps      # downloads the packages listed in package.json
```

## Running things

Start the development server with:

```bash
npm run dev
```

Vite will start a local server (typically at `http://localhost:5173`) and automatically open it in your browser. Any changes you make to HTML, CSS, or JS files will instantly reflect in the browser thanks to Hot Module Replacement (HMR).

## How to code in the project

- **HTML:** Edit `index.html` at the root for your main markup.
- **JavaScript:** Write your logic in `src/js/main.js` (or add new modules there and import them).
- **CSS:** Add styles to `src/styles/style.css`. You can use CSS nesting (e.g., standard `&` selector rules) thanks to PostCSS.
- **Static Assets:** Place images or other static files in `src/assets/images/` or the public `public/` directory depending on.

## Talking to the backend

The backend runs on **port 8080** (see `docker/docker-compose.yml`). When you
fetch data, point your requests at `http://localhost:8080`.

## What NOT to do

- Don't edit files in `back_end/` or `data/` — those are the backend's.
- Don't commit the `node_modules/` folder (it's ignored automatically).

## Scripts

Use the following scripts for your development workflow:

```bash
# Start the development server
npm run dev

# Checks your code for any linting errors
npm run lint

# Tries to automatically fix any linting errors present in your code
npm run lint:fix

# Formats your code in a consistent, predefined style using Prettier
npm run format

# Build for production
npm run build

# Preview the build
npm run preview

# Build and preview the project
npm run buildpreview
```

## Folder Structure

This is the structure of the project:

```plaintext
/
├── public                  # Public static assets (kept as-is during build)
├── src                     # Source code
│   ├── assets              # General assets for your project
│   │   ├── images          # Store your images here
│   ├── js                  # Javascript files of your project
│   └── styles              # CSS styles for your project
├── .editorconfig           # Configuration for the EditorConfig plugin
├── eslint.config.js        # Configuration for ESLint (Flat Config API)
├── .gitignore              # Files and folders to be ignored by Git
├── .prettierignore         # Files to be ignored by Prettier
├── .prettierrc             # Configuration for Prettier
├── index.html              # The root HTML file
├── package-lock.json       # Lockfile for your project's dependencies
├── package.json            # Defines your project and its dependencies
├── postcss.config.cjs      # Configuration for PostCSS
├── README.md               # This file
└── vite.config.js          # Configuration for Vite
```
