## About
Marimo notebook on Python.
Description and Setup of the Long range drone for Cinematic followed by some engineering calculations.


## Run and Edit Marimo Notebook in isolated Venv using UV
uv run marimo edit notebook.py          # Run in web
uv run marimo edit --watch              # Work in your IDE
uv run marimo run notebook.py           # Run marimo notebooks as app


## Initial setup (not required)
uv init project_name
cd project_name
uv venv .venv

uv add numpy                    # add dependencies
uv add "marimo[recommended]"