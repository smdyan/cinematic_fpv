
## About

Marimo notebook on Python.
Guide and setup of the long range drone for Cinematic followed by some engineering calculations.


## Run and Edit Marimo Notebook in isolated Venv using UV

uv run marimo edit notebook.py          # Run in web <br>
uv run marimo edit --watch              # Work in your IDE <br>
uv run marimo run notebook.py           # Run marimo notebooks as app <br>


## Initial setup (not required)

uv init project_name <br>
cd project_name <br>
uv venv .venv <br>
uv add numpy                            # add dependencies <br>
uv add "marimo[recommended]" <br>