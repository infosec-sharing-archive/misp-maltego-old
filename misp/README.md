# README - Misp

This canari package brings six transforms to make Maltego interact with MISP. The current devel branch of the MISP is supported only 
(must have the search rest API). Canari and Malformity are prerequisites. 

To install: 

python setup.py install
canari install-package misp

The API key and MISP url is stored in ~/.canari/misp.conf. You might want to assign a special icon to a MISP event entity in
Maltego GUI (Manage Entities), otherwise you get the default pawn icon.
