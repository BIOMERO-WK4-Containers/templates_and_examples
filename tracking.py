import torch
from trackastra.model import Trackastra
from trackastra.tracking import graph_to_ctc, graph_to_napari_tracks
from trackastra.data import example_data_bacteria
import tifffile as TIFF

device = "automatic" # explicit choices: [cuda, mps, cpu]

# load some test data images and masks
imgs, masks = example_data_bacteria()

# Load a pretrained model
#model = Trackastra.from_pretrained("general_2d", device=device)
#
# the 'ctc' model handles also 2d tracking
model = Trackastra.from_pretrained('ctc', device=device)

# Track the cells
track_graph = model.track(imgs, masks, mode="greedy")  # or mode="ilp", or "greedy_nodiv"

# Write to cell tracking challenge format
ctc_tracks, masks_tracked = graph_to_ctc(track_graph, masks, outdir=".")

# hmm, but it is written with "ZSTD compression".... a bit of problem
# soo, resave again:
for t in range(masks_tracked.shape[0]):
    TIFF.imwrite(f"man_track{t:04}.tif", masks_tracked[t])

