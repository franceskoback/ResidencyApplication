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
- `match_pipeline.py`: Main pipeline — calculates scores, applies culture adjustments, assigns regions from lat/long, and writes a color-coded, region-grouped output (shows Doximity next to program names)  
- `format_ortho_signals.py`: Cleans/formats orthopedic program signal data for use in the pipeline  
- `match_optimizer.ipynb`: (Optional) Notebook version for interactive tweaking and visualization  
- `top_law_ortho_matches.csv`: Output CSV of optimal matches (ranked, grouped by region, and color-coded)  

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

4. Run the match pipeline:  

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

| Region | Law School | Ortho Program (Doximity) | Law Rank | Distance (mi) | Culture Score | Rank Score |
|--------|------------|---------------------------|----------|---------------|---------------|------------|
| NE     | NYU        | HSS (1)                   | 8        | 1.3           | +0.5          | 11.6       |
| NE     | Penn       | Jefferson (9)             | 5        | 2.1           | −0.2          | 16.2       |

---

**Contact:** [github.com/franceskoback](https://github.com/franceskoback)
