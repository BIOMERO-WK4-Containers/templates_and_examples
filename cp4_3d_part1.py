import torch
import numpy as np
from cellpose import models
import tifffile as TIFF

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Will use: {device}")

# ----------------------------------------------

input_filepath  = '/mnt/proj2/dd-24-22/Mastodon_paper/orig_as_CTC__1px_markers'
output_filepath = '/mnt/proj2/dd-24-22/Mastodon_paper/orig_as_CTC__1px_markers/SEG'

last_tp = 600
group_size = 10
group_pos = 0

part = 1

# ----------------------------------------------

model = models.CellposeModel(device=device)

lastone = 1 if part == 5 else 0
part *= 100

for t in range(part, part+100+lastone):
    print(f"doing TP = {t}")

    img = TIFF.imread( f"{input_filepath}/t{t:03}.tif" )

    mask,_,_ = model.eval(np.reshape(img, (1,*img.shape)), channel_axis = 0, z_axis = 1, normalize=True, do_3D=True, niter=2000)

    TIFF.imwrite( f"{output_filepath}/mask{t:03}.tif", mask)


