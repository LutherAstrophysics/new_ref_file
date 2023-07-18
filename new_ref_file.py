import pandas as pd

df_new = pd.read_csv("m23_7.0_2022-06-19_0028_dao.txt", delim_whitespace=True)
df_og = pd.read_csv(
    "ref_no_na_w_2509_10.txt", skiprows=8, engine="python", delimiter="\s{2,}"
)


def is_star_already_present_at(x, y, threshold=2):
    return (
        len(
            df_og[
                (df_og["X"] > x - threshold)
                & (df_og["X"] < x + threshold)
                & (df_og["Y"] > y - threshold)
                & (df_og["Y"] < y + threshold)
            ]
        )
        > 0
    )


def main():
    stars_to_add_ids = []
    for i in range(len(df_new)):
        candidate = df_new.iloc[i]
        if not is_star_already_present_at(
            candidate["xcentroid"], candidate["ycentroid"], threshold=4
        ):
            stars_to_add_ids.append(candidate.id)
    new_stars = df_new[df_new.id.isin(stars_to_add_ids)]
    # We want to add new stars in order of their decreasing flux value
    # (Brightest first)
    new_stars = new_stars.sort_values(by="flux", ascending=False)
    new_stars_dict = {}
    for i in range(len(new_stars)):
        candidate = new_stars.iloc[i]
        # Only add this star if it's it's too close neighbor is not already there
        cx, cy = candidate["xcentroid"], candidate["ycentroid"]
        df_to_check = new_stars.iloc[:i]
        if (
            len(
                df_to_check[
                    (df_to_check["xcentroid"] > cx - 1)
                    & (df_to_check["xcentroid"] < cx + 1)
                    & (df_to_check["ycentroid"] > cy - 1)
                    & (df_to_check["ycentroid"] < cy + 1)
                ]
            )
            == 0
        ):
            new_stars_dict[candidate["id"]] = {
                "X": cx,
                "Y": cy,
                "Sigma": 0,
                "FWHM": 0,
                "Sky ADU": 0,
                "Star ADU": 0,
            }
    df_new_stars_only = pd.DataFrame.from_dict(new_stars_dict, orient="index")
    df_merged = pd.concat([df_og, df_new_stars_only], ignore_index=True)
    with open("ref_with_new_stars.txt", "w") as fd:
        fd.write(
            """Refer to https://github.com/lutherastrophysics/new_ref_file for more info
Star Data Extractor Tool
    Images: m23_3.5_071.fit (2003) and m23_7.0_2022-06-19_0028.fit
    Stars Found: 2508 (good stars) in 2003 img + 1246 in 2022
    Radius of star diaphragm:
    Sky annulus inner radius:
    Sky annulus outer radius:
    Threshold factor: High ="""
        )
        fd.write("\n")
        df_merged.columns = [
            column_header.rjust(10, " ") for column_header in df_merged.columns
        ]
        df_merged.to_csv(
            fd,
            index=False,
            sep="\t",
            float_format="%10.2f",
        )


if __name__ == "__main__":
    main()
