Setup a simulation modifying `app.py`

Equilibrate and run the simulation with:

```
python app.py -e 10 -n 1000

```

Generate `.gro` and `.top` files with (discard equilibration):

```
mmdemux --state_index 0 --start 10 --step 10 --split --extract_topology trj.nc trj.gro

```


