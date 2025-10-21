# ----------------------------------------------
# WHOLE TASK PARAMETERS:

input_filepath  = '/mnt/proj2/dd-24-22/Mastodon_paper/orig_as_CTC__1px_markers'
output_filepath = '/mnt/proj2/dd-24-22/Mastodon_paper/orig_as_CTC__1px_markers/SEG'
last_tp = 600


# ----------------------------------------------
# JOBS SITUATION:

import os
worker_index = int(os.environ.get('SLURM_ARRAY_TASK_ID',1))
worker_total = int(os.environ.get('SLURM_ARRAY_TASK_COUNT',1))
#
# IMPORTANT: Run this worker script within SLURM's Job Arrays paradigm
# example: sbatch -J1-6 0_slurmFacade_startHere.sh
# (it's better here to index sub-jobs 1-based, not 0-based, then _ID = 1..6, _COUNT=6)
#
# However(!), by injecting the two above variables intol a local environment (OS),
# one can simulate the behaviour as if this script would be executed on a node, this is
# especially useful for testing the splitting of the full workload (into smaller batches)
#
# Also note, that due to the default values ",1", the script can be used outside SLURM
# and without any special preparations (like setting up the two variables), in which case
# this script will sequentially execute the whole workload...

def get_list_of_indices_for_this_worker(worker_id, number_of_all_workers_avaible, all_jobs_list):
    """ Assuming number_of_all_workers_avaible >= 1 and worker_id in [1, number_of_all_workers_avaible] """

    per_job_count = len(all_jobs_list) // number_of_all_workers_avaible

    this_job_indexes = all_jobs_list[(worker_id-1)*per_job_count:]
    if worker_id < number_of_all_workers_avaible:
        this_job_indexes = this_job_indexes[:per_job_count]  # the size of the last batch can vary...

    return this_job_indexes


# ----------------------------------------------
# THE WORKHORSE SCRIPT ITSELF:

import torch
import numpy as np
from cellpose import models
import tifffile as TIFF

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Will use: {device}")

model = models.CellposeModel(device=device)

all_jobs_indexes = [ tp for tp in range(0, last_tp+1) ]  # time points range from  0 till the last one inclusively (that's +1)
this_job_indexes = get_list_of_indices_for_this_worker(worker_index, worker_total, all_jobs_indexes)

for t in this_job_indexes:
    print(f"doing TP = {t}")

    img = TIFF.imread( f"{input_filepath}/t{t:03}.tif" )

    mask,_,_ = model.eval(np.reshape(img, (1,*img.shape)), channel_axis = 0, z_axis = 1, normalize=True, do_3D=True, niter=2000)

    TIFF.imwrite( f"{output_filepath}/mask{t:03}.tif", mask)

