import tifffile as TIFF

cw = 170
for tp in range(0,601):
#for tp in range(245,601,5):
    print("doing tp:",tp)
    i = TIFF.imread(f"/home/ulman/papers/mastodonPaper/E1_cellposev4_trackatra/SEG_LZWed/mask{tp:03}.tif")

    i[:, 0:cw,        0:cw+10] = 0  # TL
    i[:, 0:cw,         -cw:-1] = 0  # TR
    i[:, -cw-10:-1,   0:cw+30] = 0  # BL
    i[:, -cw-10:-1, -cw-10:-1] = 0  # BR

    TIFF.imwrite(f"/home/ulman/papers/mastodonPaper/E1_cellposev4_trackatra/SEG_LZWed_cleanedCorners/mask{tp:03}.tif",i)

