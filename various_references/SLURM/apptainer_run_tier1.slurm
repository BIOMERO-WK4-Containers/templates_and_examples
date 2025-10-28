#!/bin/bash
#SBATCH -A 2024_300
#SBATCH --partition=cpu_milan
#SBATCH --nodes="1"
#SBATCH --ntasks-per-node="1"
#SBATCH --cpus-per-task=16
#SBATCH --gpus-per-task=1
#SBATCH --output=output_careamics_nalan.out
#SBATCH --error=error_careamics_nalan.err
#SBATCH --time=01:00:00

export APPTAINER_TMPDIR=$VSC_SCRATCH_PROJECTS_BASE/2024_300/twoller/containers/apptainer_tmp
export APPTAINER_CACHEDIR=$VSC_SCRATCH_PROJECTS_BASE/2024_300/twoller/containers/apptainer_cache
 
apptainer run careamics.sif python  $VSC_SCRATCH_PROJECTS_BASE/2024_300/twoller/containers/test_nalan_careamics.py
