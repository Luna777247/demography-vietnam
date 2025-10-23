Vietnam Population Explorer

This repository contains analysis and visualizations for Vietnamese population data (1955-2025).

Contents
- `Dự báo dân số Việt Nam.ipynb`: main Jupyter notebook with ETL, modeling, and visualizations.
- `raw/`: raw CSV datasets (Vietnam and other supporting files).
- `populations/`: generated PNG visualizations.
- `analysis/`: exported analysis results and HTML.

How to push to GitHub
1. Create a repository on GitHub (via the website or using `gh`).
2. Add the remote and push:

   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git branch -M main
   git push -u origin main

Notes
- Large data files are included under `raw/`. If you'd prefer to exclude them, remove or add them to `.gitignore` before pushing.
