#!/bin/bash
#SBATCH --job-name=build-apptainer_cellpose
#SBATCH --ntasks=1
#SBATCH --clusters=genius
#SBATCH --partition=gpu_p100
#SBATCH --cpus-per-task=4
#SBATCH --gpus-per-node=1
#SBATCH --time=1:00:00
#SBATCH --output=build1_cellpose.stdout
#SBATCH --error=build1_cellpose.stderr
#SBATCH --account="lp_hack_bio_im"
#SBATCH --chdir=/scratch/leuven/348/vsc34840/containers

echo Start Job
date
#cp $VSC_SCRATCH/containers/cellpose_bp.yml /tmp/cellpose_bp.yml

APPTAINER_CACHEDIR=$VSC_SCRATCH/.apptainer/cache
APPTAINER_TMPDIR=$VSC_SCRATCH/.apptainer/tmp
apptainer build --nv $VSC_SCRATCH/containers/cellpose.sif $VSC_SCRATCH/containers/cellpose_gpu.def


date
echo End Job
