<!-- ./src/README.md -->

# `./src/` Folder

This is where all our code lives, split into two independent halves:

- **`back_end/`** - Python. The server, database logic, and business rules.
- **`front_end/`** - JavaScript. The user interface.

In a real-world project these would be two separate repositories and should be
treated as independent here too, the frontend talks to the backend over the
network (port 8080), not by importing its files. We keep them in one folder only
because this is a college project where simplicity and clarity matter most.

Each half has its own README with setup instructions for that team. 