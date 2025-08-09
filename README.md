# Residency + Law School Match Optimizer

Completely Computerized Hypothetical Match List Solely Based on Factors Below

- **Law school rank**  
- **Orthopedic surgery residency rank**  
- **Geographic proximity**  
- **Culture/“fit” score**  

---

## To-Do
- Add weather as a factor  

---

## Project Files

- `top_law_schools.csv`: List of law schools with ranks and addresses  
- `top_ortho_programs.csv`: List of orthopedic residency programs with lat/long; region is inferred automatically  
- `match_pipeline.py`: Main pipeline — calculates scores, applies culture adjustments, assigns regions from lat/long, and generates ranked matches  
- `format_ortho_signals.py`: Cleans/formats orthopedic program signal data for use in the pipeline  
- `match_optimizer.ipynb`: (Optional) Notebook version for interactive tweaking and visualization  
- `ortho_signals_formatted.csv`: Processed list of orthopedic programs with culture scores, weights, and region  
- `top_law_ortho_matches.csv`: Ranked list of all law–ortho program combinations based on the minimization algorithm  

---

## How to Run

1. Install dependencies:  

   ```bash
   match_optimizer.ipynb
   ```

2. (First Run or to update list) Run relevant part of ipynb code to get latitude and longitide of the ortho or law programs you're interested in.

   ```bash
   python format_ortho_signals.py
   ```

4. Run the match pipeline:  will generate both:
   - `ortho_signals_formatted.csv` — formatted ortho program data with culture scores, weights, and regions
   - `top_law_ortho_matches.csv` — ranked list of all law–ortho combinations

   ```bash
   python match_pipeline.py
   ```

5. Format the ortho singals csv so you get a color-coded results excel sheet organized by region 
   ```bash
   python format_ortho_signals.py
   ```

---

## Custom Weights

Adjust how important each factor is in `match_pipeline.py`.  
Bigger number = more importance (more penalty for lower ranking / farther distance / lower culture fit).  

```python
law_weight = 2.0
ortho_weight = 1.0
distance_weight = 2.0
culture_weight = 1.5
```

---

## Culture Score Adjustments

- Culture scores can be edited in the CSV or directly in the script.  
- You can add or subtract from a program’s score based on personal impressions or new info.  
- Re-run the pipeline to see updated rankings instantly.  

---

## Sample Output

### Ortho Program Data (`ortho_signals_formatted.csv`)

| Ortho Program | Rank | Region | OrthoCultureScoreUsed | LawRankWeight | OrthoRankWeight | DistWeight | CultureWeight |
|---------------|------|--------|-----------------------|---------------|-----------------|------------|---------------|
| Mass General Brigham / MGH / Brigham & Women’s / Harvard Med | 1 | Boston | 3 | 5 | 1 | 5 | 10 |
| Boston University Medical Center Orthopaedic Surgery Residency | 12 | Boston | 0 |   |   |   |   |
| UCLA Medical Center Orthopaedic Surgery Residency | 21 | LA | 0 |   |   |   |   |

---

### Law–Ortho Matches (`top_law_ortho_matches.csv`)

| Law School | Ortho Program | Distance (mi) | Score |
|------------|---------------|---------------|-------|
| Harvard Law School | Mass General Brigham / MGH / Brigham & Women’s / Harvard Med | 2.88 | -5.621 |
| Duke University School of Law | Duke Orthopaedic Surgery Residency | 0.79 | 20.952 |
| Stanford Law School | Stanford Orthopedic Residency Program | 1.01 | 33.032 |
---

**Contact:** [github.com/franceskoback](https://github.com/franceskoback)
