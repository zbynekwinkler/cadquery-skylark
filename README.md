
# Wikihouse Skylark blocks in CadQuery

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)


## What and Why

The immediate goal is to remodel all available [Skylark](https://github.com/wikihouseproject/Skylark) blocks using [CadQuery](https://github.com/CadQuery/cadquery/). That will enable
regular git workflow for developing the system (think text based diff, code reviews etc.).

Also the tooling to work on the system will be free and portable. CadQuery is based on python
and OpenCascade and works on many systems.

CadQuery also captures the design intent directly and allows the creation of a fully
parametric designs, paving the way to easier creation of custom blocks.


## How

The first step is to reverse engineer the design of the existing blocks. A great tool for that
is [Freecad](https://www.freecad.org/). However, none of the available exports can be directly
opened in Freecad. [Onshape](https://www.onshape.com/en/) on the other hand can open simple
3dm files and export to STEP format which can be opened by Freecad. The account is free
and the browser based CAD works under various browsers and operating systems.

The model is still a mesh but the excelent parametric sketcher in Freecad can be used
to uncover the dimensions by _sketching over the mesh_ until it aligns perfectly.

Another usable input are the cutting DXF files. Don't try to open them in Freecad though.
They contain large number of elements (mostly discretized text) that will take Freecad forever
to load and even after it loads it is not workable (over 30k items in the object tree).

They can be opened in [LibreCAD](https://librecad.org/) quite easily. Delete the two
layers with the texts which brings the size of the file down from about 5MB to 200kB.
It opens in Freecad quite nicely then.

Use Freecad to compare the original data with the newly generated data until it
matches perfectly.

Prototype in `notebooks` to get a fast and easy visual feedback and as the code
works itself out, refactor the working pieces to `src` and leave behind only
sample calls to keep the visual feedback.

Rince & repeat for another block.

## Install

```
$ micromamba create -n cadquery-skylark
$ micromamba activate cadquery-skylark
$ micromamba install -c conda-forge -c cadquery python=3.10 cadquery=master
$ pip install jupyter-cadquery jupyter-console ocp-vscode
$ pip install -e .
$ code .
```

In VSCode install OCP CAD Viewer extension.
