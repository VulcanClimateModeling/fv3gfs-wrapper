import os
from mpi4py import MPI
import fv3gfs
import fv3config

# May need to run 'ulimit -s unlimited' before running this example
# If you're running in our prepared docker container, you definitely need to do this
# sets the stack size to unlimited

# Run using mpirun -n 6 python3 basic_model.py
# mpirun flags that may be useful:
#     for docker:  --allow-run-as-root
#     for CircleCI: --oversubscribe
#     to silence a certain inconsequential MPI error: --mca btl_vader_single_copy_mechanism none

# All together:
# mpirun -n 6 --allow-run-as-root --oversubscribe --mca btl_vader_single_copy_mechanism none python3 basic_model.py

rundir_basename = 'rundir'

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    current_dir = os.getcwd()
    rundir_path = os.path.join(current_dir, rundir_basename)
    if rank == 0:  # Only create run directory from one rank
        # Can alter this config dictionary to configure the run
        config = fv3config.get_default_config()
        fv3config.write_run_directory(config, rundir_path)
    MPI.COMM_WORLD.barrier()  # wait for master rank to write run directory
    os.chdir(rundir_path)
    fv3gfs.initialize()
    for i in range(fv3gfs.get_step_count()):
        fv3gfs.step_dynamics()
        fv3gfs.step_physics()
        fv3gfs.save_intermediate_restart_if_enabled()
    fv3gfs.cleanup()