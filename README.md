[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

Environment for development:

```
$ micromamba create -n cadquery-skylark
$ micromamba activate cadquery-skylark
$ micromamba install -c conda-forge -c cadquery python=3.10 cadquery=master
$ pip install jupyter-cadquery jupyter-console ocp-vscode
$ pip install -e .
$ code .
```

In VSCode install OCP CAD Viewer extension.
