# match_pipeline.py
import pandas as pd
from geopy.distance import geodesic

# ---------- INPUTS ----------
ortho_df = pd.read_csv("../data/geo/ortho_lat_long.csv")
law_df   = pd.read_csv("../data/geo/law_lat_long.csv")

# ---------- WEIGHTS ----------
law_rank_importance   = 5
ortho_rank_importance = 1
dist_rank_importance  = 5
culture_weight        = 10

# ---------- CULTURE BOOSTS ----------
ortho_culture = {
    "5. Mass General Brigham/Massachusetts General Hospital/Brigham and Women's Hospital/Harvard Medical School (Boston)": 3,
    "20. New York Presbyterian Hospital (Columbia Campus)": -3,
    "3. NYU Grossman School of Medicine/NYU Langone Orthopedic Hospital": -1,
    "1. Hospital for Special Surgery/Cornell Medical Center": -1,
    "72. University of North Carolina Hospitals Orthopaedic Surgery Residency": 5,
    "7. Duke Orthopaedic Surgery Residency": 2,
    "16. Carolinas Medical Center": 3,
    "71. Dell Medical School at UT Austin Orthopaedic Surgery Residency": 5,
    "65. Prisma Health/University of South Carolina SOM Greenville Orthopaedic Surgery Residency": 5,
    "18. University of Pennsylvania Health System": -2,
    "11. Sidney Kimmel Medical College at Thomas Jefferson University/TJUH": -2
}

law_culture = {
    "7. Harvard Law School": 3,
    "15. University of Texas School of Law": 1
}

# ---------- ATTACH CULTURE COLUMNS (0 if not present) ----------
ortho_df["CultureScore"] = ortho_df["Name"].map(ortho_culture).fillna(0.0).astype(float)
law_df["CultureScore"]   = law_df["Name"].map(law_culture).fillna(0.0).astype(float)

# ---------- SCORING ----------
def pair_score(law_row, ortho_row, distance_miles: float) -> float:
    law_rank   = int(str(law_row["Name"]).split(".")[0])
    ortho_rank = int(str(ortho_row["Name"]).split(".")[0])
    return (
        law_rank_importance   * law_rank +
        ortho_rank_importance * ortho_rank +
        dist_rank_importance  * distance_miles
        - culture_weight * (float(law_row.get("CultureScore", 0)) + float(ortho_row.get("CultureScore", 0)))
    )

# ---------- BUILD ALL PAIRS ----------
matches = []
for _, law in law_df.iterrows():
    if pd.isna(law["Lat"]) or pd.isna(law["Lon"]):
        continue
    for _, ortho in ortho_df.iterrows():
        if pd.isna(ortho["Lat"]) or pd.isna(ortho["Lon"]):
            continue
        dist_miles = geodesic((law["Lat"], law["Lon"]), (ortho["Lat"], ortho["Lon"])).miles
        score = pair_score(law, ortho, dist_miles)
        matches.append({
            "Law School": law["Name"],
            "Ortho Program": ortho["Name"],
            "Distance (miles)": round(dist_miles, 2),
            "Score": round(score, 3)
        })

# ---------- RESULTS TABLE ----------
results_df = pd.DataFrame(matches).sort_values("Score").reset_index(drop=True)
results_df.to_csv("../results/top_law_ortho_matches.csv", index=False)

# ---------- TOP UNIQUE PICKS ----------
ortho_signals = 30
law_signals   = 25

# Ortho
top_ortho_programs, seen_ortho = [], set()
for _, row in results_df.iterrows():
    o = row["Ortho Program"]
    if o not in seen_ortho:
        top_ortho_programs.append(o)
        seen_ortho.add(o)
    if len(top_ortho_programs) == ortho_signals:
        break

# Law
top_law_schools, seen_law = [], set()
for _, row in results_df.iterrows():
    l = row["Law School"]
    if l not in seen_law:
        top_law_schools.append(l)
        seen_law.add(l)
    if len(top_law_schools) == law_signals:
        break

# ---------- SAVE SIMPLE SIGNAL LISTS ----------
pd.DataFrame(top_ortho_programs, columns=["Ortho Program"]).to_csv("../results/ortho_signals.csv", index=False)
pd.DataFrame(top_law_schools,   columns=["Law School"]).to_csv("../results/law_signals.csv",   index=False)

# ---------- ORTHO: REGION GROUPING ----------
def get_region(lat, lon):
    if lat is None or pd.isna(lat) or lon is None or pd.isna(lon):
        return "Unknown"
    # Pennsylvania (Philly, Pittsburgh, Hershey, Danville, Bethlehem, Erie)
    if 39.7 <= lat <= 42.3 and -80.6 <= lon <= -74.7:
        return "Pennsylvania"
    # Boston
    if 42.0 <= lat <= 42.6 and -71.3 <= lon <= -70.9:
        return "Boston"
    # NYC area (Manhattan/Brooklyn/Queens/Jersey City-ish)
    if 40.5 <= lat <= 41.1 and -74.3 <= lon <= -73.5:
        return "NYC area"
    # San Francisco (Bay Area)
    if 37.2 <= lat <= 37.9 and -122.5 <= lon <= -121.7:
        return "San Francisco"
    # LA
    if 33.7 <= lat <= 34.3 and -118.6 <= lon <= -118.1:
        return "LA"
    # Texas triangle (DFW/Houston/Austin/San Antonio)
    if 29.2 <= lat <= 33.2 and -99.0 <= lon <= -95.0:
        return "Texas"
    # North Carolina
    if 34.8 <= lat <= 36.3 and -79.5 <= lon <= -78.3:
        return "NC"
    # South (not NC): VA/SC/GA coastal-ish belt (rough)
    if 32.5 <= lat <= 38.5 and -81.0 <= lon <= -76.0:
        return "South (not NC)"
    # Chicago / Michigan
    if 41.5 <= lat <= 45.5 and -88.5 <= lon <= -82.5:
        return "Chicago / Michigan"
    # Midwest (catch MO/IN/IA/KS/NE etc., helps WashU St. Louis)
    if 37.0 <= lat <= 46.0 and -97.0 <= lon <= -82.0:
        return "Midwest"
    # West (PNW)
    if 45.0 <= lat <= 49.0 and -124.0 <= lon <= -120.0:
        return "West"
    return "Other"

# Build ranked ortho table with region + culture + weights
top_ortho_df = pd.DataFrame({
    "Ortho Program": top_ortho_programs,
    "Rank": range(1, len(top_ortho_programs) + 1)
})

# attach Lat/Lon from master ortho_df
ortho_lookup = ortho_df.set_index("Name")[["Lat", "Lon", "CultureScore"]].to_dict(orient="index")
top_ortho_df["Lat"]   = top_ortho_df["Ortho Program"].map(lambda n: ortho_lookup.get(n, {}).get("Lat"))
top_ortho_df["Lon"]   = top_ortho_df["Ortho Program"].map(lambda n: ortho_lookup.get(n, {}).get("Lon"))
top_ortho_df["Region"] = top_ortho_df.apply(lambda r: get_region(r["Lat"], r["Lon"]), axis=1)

region_order = [
    "Boston", "LA", "San Francisco", "NYC area",
    "Pennsylvania",
    "Texas", "South (not NC)", "NC", "Chicago / Michigan",
    "Midwest", "West", "Other", "Unknown"
]
top_ortho_df["Region"] = pd.Categorical(top_ortho_df["Region"], categories=region_order, ordered=True)

# add culture + weights for auditing (0 if not present)
top_ortho_df["OrthoCultureScoreUsed"] = top_ortho_df["Ortho Program"].map(ortho_culture).fillna(0).astype(float)
top_ortho_df["LawRankWeight"]   = law_rank_importance
top_ortho_df["OrthoRankWeight"] = ortho_rank_importance
top_ortho_df["DistWeight"]      = dist_rank_importance
top_ortho_df["CultureWeight"]   = culture_weight

top_ortho_df = top_ortho_df.sort_values(["Region", "Rank"])
cols_out = ["Ortho Program", "Rank", "Region",
            "OrthoCultureScoreUsed", "LawRankWeight", "OrthoRankWeight", "DistWeight", "CultureWeight"]
top_ortho_df[cols_out].to_csv("../results/ortho_signals_grouped.csv", index=False)

# ---------- LAW: SIGNALS WITH CULTURE USED ----------
top_law_df = pd.DataFrame({
    "Law School": top_law_schools,
    "Rank": range(1, len(top_law_schools) + 1)
})
# attach LawCultureScoreUsed + weights
top_law_df["LawCultureScoreUsed"] = top_law_df["Law School"].map(law_culture).fillna(0).astype(float)
top_law_df["LawRankWeight"]   = law_rank_importance
top_law_df["OrthoRankWeight"] = ortho_rank_importance
top_law_df["DistWeight"]      = dist_rank_importance
top_law_df["CultureWeight"]   = culture_weight
top_law_df.to_csv("../results/law_signals_detailed.csv", index=False)

# ---------- AUDIT FILES (non-zero culture only) ----------
pd.Series({k:v for k,v in ortho_culture.items() if v != 0},
          name="OrthoCultureScore").rename_axis("Ortho Program") \
  .reset_index().to_csv("../results/_audit_ortho_culture_nonzero.csv", index=False)

pd.Series({k:v for k,v in law_culture.items() if v != 0},
          name="LawCultureScore").rename_axis("Law School") \
  .reset_index().to_csv("../results/_audit_law_culture_nonzero.csv", index=False)

print("Done:")
print(" - ../results/top_law_ortho_matches.csv")
print(" - ../results/ortho_signals.csv")
print(" - ../results/law_signals.csv")
print(" - ../results/ortho_signals_grouped.csv")
print(" - ../results/law_signals_detailed.csv")
print(" - ../results/_audit_ortho_culture_nonzero.csv")
print(" - ../results/_audit_law_culture_nonzero.csv")