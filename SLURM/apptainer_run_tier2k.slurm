#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cluster=genius
#SBATCH --partition=gpu_p100
#SBATCH --time=00:25:00
#SBATCH --job-name=Midori_kame
#SBATCH --output=tortuga_train3.out
#SBATCH --error=tortuga_train3.err
#SBATCH --cpus-per-task=4
#SBATCH --nodes=1
#SBATCH --gpus-per-node=1
#SBATCH --mem-per-cpu=1G
#SBATCH -A lp_hack_bio_im


APPTAINER_CACHEDIR=$VSC_SCRATCH/.apptainer/cache
APPTAINER_TMPDIR=$VSC_SCRATCH/.apptainer/tmp
apptainer run --nv -B $VSC_SCRATCH/EM_denoising/:/mnt careamics_gpu.sif python  /mnt/train_test_nalan_careamics_d.py
