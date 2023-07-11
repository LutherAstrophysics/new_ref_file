import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from photutils.aperture import CircularAperture
from astropy.stats import sigma_clipped_stats
from astropy.io.fits import getdata
from photutils.detection import IRAFStarFinder, DAOStarFinder
from pathlib import Path
from astroalign import find_transform
from ccdproc import cosmicray_lacosmic as lacosmic


def main(img, daofind=False):
    data = getdata(img)  # 2003-8-3

    # Remove hot pixels
    data, _ = lacosmic(data)
    data = np.array(data)

    mean, median, std = sigma_clipped_stats(data, sigma=3.0)

    print((mean, median, std))

    # Mask out extreme edges
    mask = np.zeros(data.shape, dtype=bool)
    mask[:, 0:12] = True
    mask[:, 1012:] = True
    mask[0:12, :] = True
    mask[1012:,] = True

    no_of_sigmas_above_bg = 5
    fwhm = 3.0
    if daofind:
        daofind = DAOStarFinder(fwhm=fwhm, threshold=no_of_sigmas_above_bg * std)
        sources = daofind(data - median, mask=mask)
    else:
        irafind = IRAFStarFinder(fwhm=fwhm, threshold=no_of_sigmas_above_bg * std)
        sources = irafind(data - median, mask=mask)

    for col in sources.colnames:
        if col not in ("id", "npix"):
            sources[col].info.format = "%.2f"  # for consistent table output

    sources.pprint(max_width=76)
    name = (
        ".".join(Path(img).name.split(".")[:-1])
        + ("_dao" if daofind else "_iraf")
        + ".txt"
    )
    sources.write(name, format="ascii", overwrite=True)

    positions = np.transpose((sources["xcentroid"], sources["ycentroid"]))
    xs, ys = sources["xcentroid"], sources["ycentroid"]
    print("Median X, Y", np.median(xs), np.median(ys))

    apertures = CircularAperture(positions, r=4.0)
    norm = ImageNormalize(stretch=SqrtStretch())
    plt.imshow(data, cmap="Greys", origin="lower", norm=norm, interpolation="nearest")

    # align the image to our reference
    t = find_transform(getdata("reference/m23_3.5_071.fit"), data, detection_sigma=10, min_area=10)[0]

    # stars = [(541.2, 475.65), (547.57, 493.95), (746.58, 459.64), (539.54, 426.1)]
    stars = t([(541.2, 475.65), (547.57, 493.95), (746.58, 459.64), (539.54, 426.1)])
    # breakpoint()

    stars_x, stars_y = zip(*stars)
    plt.plot(stars_x, stars_y, "r.", markersize=4)
    apertures.plot(color="blue", lw=1.5, alpha=0.5)
    plt.title(img)
    plt.show()


if __name__ == "__main__":
    main("m23_7.0_2022-06-19_0028.fit", daofind=True)