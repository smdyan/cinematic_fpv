## About
Description and Setup of the Long range drone for Cinematic followed by some engineering calculations.


## Run Marimo Notebook in isolated Venv using UV
uv init project_name
cd project_name
uv venv .venv

uv add numpy                    # add dependencies
uv add "marimo[recommended]"

uv run marimo edit my_notebook.py
uv run marimo edit --watch      # work in your IDE

uv run marimo run notebook.py           # Run marimo notebooks as app


