import torch
import numpy as np
from trackastra.model import Trackastra
from trackastra.tracking import graph_to_ctc, graph_to_napari_tracks
from trackastra.data import example_data_bacteria
import tifffile as TIFF

device = "automatic" # explicit choices: [cuda, mps, cpu]

def load_ctc(from_folder, tp_range_from, tp_range_till):
    # load the first image to understand the shape
    fp = f"{from_folder}/t{tp_range_from:03}.tif"
    print("reading the first  raw file:",fp)
    i = TIFF.imread(fp)

    tp_range = tp_range_till - tp_range_from +1
    imgs = np.zeros([tp_range,*i.shape], dtype=i.dtype)
    masks = np.zeros([tp_range,*i.shape], dtype='uint16')
    print("allocated memory for twice the shapes: ",imgs.shape)

    fp = f"{from_folder}/SEG/mask{tp_range_from:03}.tif"
    print("reading the first mask file:",fp)
    masks[0] = TIFF.imread(fp)
    imgs[0] = i

    for tp in range(tp_range_from+1, tp_range_till+1):
        print("reading time point:",tp)
        imgs[tp-tp_range_from] = TIFF.imread(f"{from_folder}/t{tp_range_from:03}.tif")
        masks[tp-tp_range_from] = TIFF.imread(f"{from_folder}/SEG/mask{tp_range_from:03}.tif")

    print("done reading.")
    return imgs,masks


# load some test data images and masks
# imgs, masks = example_data_bacteria()

imgs, masks = load_ctc('/mnt/proj2/dd-24-22/Mastodon_paper/orig_as_CTC__own_SEG_TRA/',0,600)

# Load a pretrained model
#model = Trackastra.from_pretrained("general_2d", device=device)
#
# the 'ctc' model handles also 2d tracking
model = Trackastra.from_pretrained('ctc', device=device)

print("starting the tracking...")

# Track the cells
track_graph = model.track(imgs, masks, mode="greedy")  # or mode="ilp", or "greedy_nodiv"

print("done tracking.")

# Write to cell tracking challenge format
ctc_tracks, masks_tracked = graph_to_ctc(track_graph, masks, outdir=".")

print("done exporting (1st pass)")

# hmm, but it is written with "ZSTD compression".... a bit of problem
# soo, resave again:
for t in range(masks_tracked.shape[0]):
    print("re-saving time point:",t)
    TIFF.imwrite(f"man_track{t:04}.tif", masks_tracked[t])

print("done exporting (2nd pass)")

