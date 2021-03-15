Setup a simulation modifying `app.py`

Equilibrate and run the simulation with

```
python app.py -e 10 -n 1000

```

Generate `.gro` and `.top` files with (discard equilibration):

```
mmdemux -s 0 trj.nc trj.gro --split --extract_topology --start 10 --step 10

```


