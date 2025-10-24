# Single-Purpose Image Processing Scripts, and Containers

This repository holds several single-purpose segmentation and
tracking scripts (in the root folder). Possibly a pre- or post-processing
scripts to prepare or polish, respectively, are available too
in the folder `aux_processing`.

Some scripts were adopted for "workflows", that is, to accept
inputs (and parameters, and outputs) in a "standard way" given
a certain "workflow concept such as Nextflow or BIOMERO. This
requires to embed the scripts into Docker and Apptainer (singularity)
containers, which is exemplified in the folder `containers`.
The adopting layers are, nevertheless, missing currently.

Some scripts were converted into embarrassingly parallel regime,
and married with SLURM (and HPC). Examples are provided in the
`SLURM` folder. From the HPC point of view, this parallelisation
happens at the level of using multiple nodes, but not within each
node itself. Towards multiprocessing/multithreading (on a node)
an initial investigations are thus exemplified in
the `util/parallelism_paradigms.py`.

# Image processing operations

## Demonstrators available

- Segmentation
  - Cellpose v3, CPU-friendly
  - Cellpose v4, CPU-killer -> GPU-demanding

- Tracking
  - TrackAstra (2D, 3D)

- Segmentation and Tracking in one go
  - N/A

## Demonstrators wanted

- Segmentation
  - Cellpose v4 training pipeline
  - InstanSeg
  - EmbedSeg

- Tracking
  - CellTrackingChallenge.NUDT-CN, transformer-based tracker?
  - U-LSTM as CellTrackingChallenge.BHU-IL
  - [CELLECT](https://www.nature.com/articles/s41592-025-02886-x) (3D!)

- Segmentation and Tracking in one go
  - TGMM, old-school but still very performant, CPU-only
  - Ultrack (3D)
  - Cell-TRACTR (2D)
  - EmbedTrack

## Presentations on containers and HPC

- presentation on [Docker and workflow management primer] (https://docs.google.com/presentation/d/1euJewnbw5fT2awcPtaiSgiDLyvMTZB8w/edit?slide=id.p1#slide=id.p1)
- presentation on [HPC infrastructure](https://docs.google.com/presentation/d/1jR8FzRQyQRIMw1s-pEHv8qsU52RKztICLCHleTT2Xo8/edit?usp=sharing)

## Containers repositories
- https://hub.docker.com/
- https://seqera.io/containers/
- https://git.embl.org/grp-cbbcs/container-recipes/-/tree/master
- https://github.com/BIOP/BIOP-desktop/tree/main/docker
