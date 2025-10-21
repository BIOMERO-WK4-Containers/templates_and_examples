import tifffile as TIFF

in_folder  = '/mnt/proj2/dd-24-22/Mastodon_paper/orig_as_CTC__1px_markers/SEG_LZWed'
out_folder = '/mnt/proj2/dd-24-22/Mastodon_paper/orig_as_CTC__own_SEG_TRA/SEG'

cw = 170
for tp in range(0,601):
#for tp in range(245,601,5):
    print("doing tp:",tp)
    i = TIFF.imread(f"{in_folder}/mask{tp:03}.tif")

    i[:, 0:cw,        0:cw+10] = 0  # TL
    i[:, 0:cw,         -cw:-1] = 0  # TR
    i[:, -cw-10:-1,   0:cw+30] = 0  # BL
    i[:, -cw-10:-1, -cw-10:-1] = 0  # BR

    TIFF.imwrite(f"{out_folder}/mask{tp:03}.tif",i)

