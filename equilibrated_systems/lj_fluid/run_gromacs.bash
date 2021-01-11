mkdir rundir;
cp lj.mdp rundir/system.mdp
cp frames/1.gro rundir/system.gro
cp frames/system.top rundir
(
    cd rundir
    gmx grompp -f system.mdp -c system.gro -p system.top -o system.tpr
    gmx mdrun -s system.tpr -nb cpu
)
