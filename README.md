# Residency + Law School Match Optimizer

Completely Computerized Hypothetical Match List Solely Based on Factors Below

- Law school rank  
- Orthopedic surgery residency rank  
- Geographic proximity

## To-Do
- Add culture fit
- Add weather 

## Project Files

- `top_law_schools.csv`: List of law schools with ranks and addresses  
- `top_ortho_programs.csv`: List of orthopedic residency programs  
- `match_optimizer.ipynb`: Python script that calculates top matches  
- `top_law_ortho_matches.csv`: Output CSV of optimal matches  

## How to Run

1. Install dependencies:

   ```
   pip install pandas geopy
   ```

2. Run the script:

   ```
   python match_optimizer.ipynb
   ```

3. Open `top_law_ortho_matches.csv` to see the results.

## Custom Weights

Adjust how important each factor is in `match_optimizer.py`: bigger number = more importance (more penalty for lower ranking / farther distance) 

```python
law_weight = 2.0
ortho_weight = 1.0
distance_weight = 2.0
```

## Sample Output

| Law School | Ortho Program | Law Rank | Ortho Rank | Distance (mi) | Score |
|------------|---------------|----------|-------------|----------------|--------|
| NYU        | HSS           | 8        | 1           | 1.3            | 11.6   |
| Penn       | Jefferson     | 5        | 9           | 2.1            | 16.2   |

---

Contact: [github.com/franceskoback](https://github.com/franceskoback)

