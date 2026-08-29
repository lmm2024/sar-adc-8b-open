# External dependencies

The following are required but are not redistributed in this repository:

- IHP SG13G2 open PDK, including device models, PCells and layer definitions.
- IIC-OSIC-TOOLS Docker image `hpretl/iic-osic-tools:2026.07`.
- KLayout, Magic, netgen, ngspice, LibreLane/OpenROAD/Yosys and related tools supplied by the container.
- Standard-cell models and technology files supplied by the PDK/tool image.

The tested PDK revision is `84374023ee8b4b126bebbba67fcbada0a9c0ff0b`. License terms for these dependencies remain those of their respective projects. This repository contains only the design source, generated design views, compact verification evidence and scripts needed to reproduce the stated results.
