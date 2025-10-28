import torch
from cellpose import models
import tifffile as TIFF

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Will use: {device}")

# ----------------------------------------------

input_filepath  = '/home/ulman/data/Kobe-Hackathon/official_test_dataset/nuclei_one_channel_one_TP.tif'
output_filepath = '/home/ulman/data/Kobe-Hackathon/official_test_dataset/nuclei_one_channel_one_TP__cp3_masks.tif'

# ----------------------------------------------

model = models.Cellpose(device=device)

img = TIFF.imread(input_filepath)

mask,_,_,_ = model.eval(img, normalize=True, do_3D=False, niter=2000)

TIFF.imwrite(output_filepath, mask)


