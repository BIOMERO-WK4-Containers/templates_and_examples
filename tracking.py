import torch
import numpy as np
from trackastra.model import Trackastra
from trackastra.tracking import graph_to_ctc, graph_to_napari_tracks
from trackastra.data import example_data_bacteria
import tifffile as TIFF
from skimage.transform import resize as img_resize
import util.parallelism_paradigms as P

device = "automatic" # explicit choices: [cuda, mps, cpu]


downscale_x = 3.0
downscale_y = 3.0
downscale_z = 1.0

orig_shape = None

# TODO: after down-scaling, check that
#         - no mask disappeared; if it did disappeared, place 1x1 px at least
#         - no mask has been split into multiple components (or(?), to different number of components than it was originally)

# TODO: instead of up-scaling back, relabel the original masks (reload them from the drive)
# TODO: after up-scaling/projecting back, check no label has been left untouched (consistency)

# TODO: towards automation:
#         - use ~1.0x number of CPUs for the multithreading
#         - put everything into functions, perhaps turn the whole thing into a class?
#         - consider using TQDM in util/parallelism_paradigms (and not print() in processing functions)
#         - for segmentation: use SLURM env variables (with defaults if no env var is found) for splitting the work

def downscaled_in_xyz(img, is_mask=False):
    global orig_shape
    sz_new = []
    sz_orig = img.shape
    orig_shape = [ sz for sz in sz_orig ] # backup (make a copy) the original size, assuming all input images are of the same size

    if len(sz_orig) > 2: sz_new.append( int(sz_orig[-3] // downscale_z) )
    sz_new.append( int(sz_orig[-2] // downscale_y) )
    sz_new.append( int(sz_orig[-1] // downscale_x) )
    return img_resize(img, sz_new, preserve_range=True, order=0) if is_mask else img_resize(img, sz_new, preserve_range=True)

def upscaled_in_xyz(img, is_mask=False):
    global orig_shape
    if orig_shape is None: return img
    return img_resize(img, orig_shape, preserve_range=True, order=0) if is_mask else img_resize(img, orig_shape, preserve_range=True)

def read_and_downscale(img_filepath, is_mask=False):
    return downscaled_in_xyz( TIFF.imread(img_filepath), is_mask=is_mask )

def write_upscaled(img_filepath, img, is_mask=False):
    TIFF.imwrite( img_filepath, upscaled_in_xyz(img, is_mask=is_mask) )


def load_ctc(from_folder, tp_range_from, tp_range_till):
    # load the first image to understand the shape
    fp = f"{from_folder}/t{tp_range_from:03}.tif"
    print("reading the first  raw file:",fp)
    i = read_and_downscale(fp, is_mask=False)

    tp_range = tp_range_till - tp_range_from +1
    imgs = np.zeros([tp_range,*i.shape], dtype=i.dtype)
    masks = np.zeros([tp_range,*i.shape], dtype='uint16')
    print("allocated memory for twice the shapes:",imgs.shape)
    print("...this is likely as much as",len(imgs.flat)*4.0 / float(1 << 30),"GB")

    fp = f"{from_folder}/SEG/mask{tp_range_from:03}.tif"
    print("reading the first mask file:",fp)
    masks[0] = read_and_downscale(fp, is_mask=True)
    imgs[0] = i

    for tp in range(tp_range_from+1, tp_range_till+1):
        print("reading time point:",tp)
        imgs[tp-tp_range_from] = read_and_downscale(f"{from_folder}/t{tp_range_from:03}.tif", is_mask=False)
        masks[tp-tp_range_from] = read_and_downscale(f"{from_folder}/SEG/mask{tp_range_from:03}.tif", is_mask=True)

    print("done reading.")
    return imgs,masks


## <  parallel version of load_ctc() >
def load_ctc_worker(input_tuple):
    imgs,idx,path,is_mask = input_tuple
    print("reading index :",idx)
    imgs[idx] = read_and_downscale(path, is_mask=is_mask)
    return "OK" # flag the job is done

NUM_PARALLEL_WORKERS = 50
def load_ctc_with_multiprocessing(from_folder, tp_range_from, tp_range_till):
    global NUM_PARALLEL_WORKERS

    # load the first image to understand the shape
    fp = f"{from_folder}/t{tp_range_from:03}.tif"
    print("reading the first raw file:",fp)
    i = read_and_downscale(fp, is_mask=False)

    tp_range = tp_range_till - tp_range_from +1
    imgs = np.zeros([tp_range,*i.shape], dtype=i.dtype)
    masks = np.zeros([tp_range,*i.shape], dtype='uint16')
    print("allocated memory for twice the shapes:",imgs.shape)
    print("...this is likely as much as",len(imgs.flat)*4.0 / float(1 << 30),"GB")
    imgs[0] = i

    tasks = [ (imgs,tp-tp_range_from,f"{from_folder}/t{tp:03}.tif",False) for tp in range(tp_range_from+1, tp_range_till+1) ]
    P.process_with_multithreading(tasks, load_ctc_worker, NUM_PARALLEL_WORKERS, "ctc_loader")

    print("reading the masks now")
    tasks = [ (masks,tp-tp_range_from,f"{from_folder}/SEG/mask{tp:03}.tif",True) for tp in range(tp_range_from, tp_range_till+1) ]
    P.process_with_multithreading(tasks, load_ctc_worker, NUM_PARALLEL_WORKERS, "ctc_loader")

    print("done reading.")
    return imgs,masks
## </ parallel version of load_ctc() >


# load some test data images and masks
# imgs, masks = example_data_bacteria()

#imgs, masks = load_ctc('/mnt/proj2/dd-24-22/Mastodon_paper/orig_as_CTC__own_SEG_TRA/',0,600)
imgs, masks = load_ctc_with_multiprocessing('/mnt/proj2/dd-24-22/Mastodon_paper/orig_as_CTC__own_SEG_TRA/',0,600)

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
print("will also re-shape to",orig_shape)
def rewriter(t):
    print("re-saving time point:",t)
    write_upscaled(f"man_track{t:04}.tif", masks_tracked[t], is_mask=True)
#
# serial
# for t in range(masks_tracked.shape[0]): rewriter(t)
#
# parallel
tasks = [ t for t in range(masks_tracked.shape[0]) ]
P.process_with_multithreading(tasks, rewriter, NUM_PARALLEL_WORKERS, "ctc_writer")

print("done exporting (2nd pass)")

