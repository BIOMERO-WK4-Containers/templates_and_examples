#!/usr/bin/env bash

#SBATCH -A FTA-25-62
#SBATCH -o /mnt/proj2/dd-24-22/Mastodon_paper/code/seg_and_tra_pipeline/logs/job-%x-%A_%a-%N.out.txt
#SBATCH -e /mnt/proj2/dd-24-22/Mastodon_paper/code/seg_and_tra_pipeline/logs/job-%x-%A_%a-%N.err.txt

#SBATCH -J "cellpose v4 3D"
#SBATCH -p qgpu
#SBATCH --gpus 1

# ${-n} tasks created in total, each wanting ${-c} CPUs,
# the tasks are spread evenly over ${-N} nodes

#SBATCH -n 1
#SBATCH -t 5:00:0

# HOW TO RUN, example:
# sbatch --array=1-6 0_slurmFacade_startHere.sh


cd /mnt/proj2/dd-24-22/Mastodon_paper/code/seg_and_tra_pipeline/
pixi run --frozen python /mnt/proj2/dd-24-22/Mastodon_paper/code/seg_and_tra_pipeline/SLURM/cp4_3d_for_jobArrays.py
