## Why is this a new ref file?
It's not. But we only realized this after we had already created this repo. This
repo was used to generate an image on which we ran a find program to discover
the stars that we hadn't tracked before. Then we add these stars to our newer
version of `ref_revised_71` file that keeps a list of stars positions.

## How and what
Raw images numbered 271-280 from July 28, 2022 were used to generate aligned
combined using darks from the night and masterflat from 2022-06-19. The program
[create_align_combined.py](./create_align_combined.py) was used to create the
aligned combined. The result is
[m23_7.0_2022-06-19_0028.fit](./m23_7.0_2022-06-19_0028.fit). Running the [DAO
finder](https://photutils.readthedocs.io/en/stable/api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder)
algorithm on this aligned combined image using the program in
[main.py](./main.py) we found 3127 stars that are kept in
[m23_7.0_2022-06-19_0028_dao.txt](./m23_7.0_2022-06-19_0028_dao.txt).

Note that we also tried using IRFA algorithm from the photutils library, but the
DAOFind worked better for us results for DAOFind were similar to the result in
our current reference file.
