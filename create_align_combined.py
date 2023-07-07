import numpy as np

from pathlib import Path
from m23.file.raw_image_file import RawImageFile
from m23.utils import get_raw_images
from m23.calibrate import calibrateImages
from m23.align import image_alignment
from astropy.io.fits import getdata

FOLDER = Path("July 28, 2022")


def align_combine(output="m23_7.0_2022-06-19_0028.fit"):
    raw_images = get_raw_images(FOLDER / "m23")
    raw_images_data = [x.data() for x in raw_images]

    masterdark_data = getdata(FOLDER / "Calibration Frames/masterdark.fit")
    masterflat_data = getdata(FOLDER / "Calibration Frames/2022-06-19_masterflat.fit")
    calibrated = calibrateImages(masterdark_data, masterflat_data, raw_images_data)
    aligned_images = []
    for img in calibrated:
        aligned_images.append(
            image_alignment(img, "reference/m23_3.5_071.fit")[0]
        )  # noqa
    combined = np.sum(aligned_images, axis=0)
    RawImageFile(output).create_file(
        combined.astype("int32"), copy_header_from=raw_images[0]
    )


if __name__ == "__main__":
    align_combine()