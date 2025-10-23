# Vietnam Population Explorer — AI Coding Agent Instructions

## Project Overview
Comprehensive demographic analysis platform for Vietnamese population data (1955-2025): ETL pipeline → statistical modeling → interactive visualizations. Features ARIMA time series forecasting, Logistic/Gompertz growth models, and interactive HTML dashboards with Chart.js.

## Current Architecture & Data Flow

### Core Components
- **`Dự báo dân số Việt Nam.ipynb`** — Main analysis notebook (100+ cells) with ETL, ARIMA modeling, growth curve fitting, and systematic plot saving
- **`raw/vietnam.csv`** — Primary demographic dataset (1955-2025) with 13 indicators: Population, Median Age, Fertility Rate, Urban Pop %, etc.
- **`raw/Dân số/`** — 8 provincial population files (birth/death rates, fertility, urbanization by gender/region)
- **`populations/`** — Output directory for systematically saved matplotlib visualizations (PNG, 300 DPI)
- **`analysis/`** — Legacy output directory with demographic analysis results and JSON exports
- **HTML Dashboards**: `deepseek_html_20251022_8ad066.html`, `test.html` — Interactive Chart.js visualizations with Vietnamese localization

### Data Flow
1. **Input**: Raw CSVs with Vietnamese headers, wide format (years as columns), mixed encodings
2. **Processing**: Jupyter cells handle data cleaning, outlier removal, normalization, statistical modeling
3. **Analysis**: ARIMA forecasting, growth curve fitting (Logistic/Gompertz), correlation analysis, PCA
4. **Output**: PNG plots saved to `populations/` with descriptive filenames, JSON results to `analysis/`, interactive web dashboards

## Key Workflows

### Primary Analysis Workflow
```bash
# Launch Jupyter and open main notebook
jupyter notebook "Dự báo dân số Việt Nam.ipynb"

# Execute cells sequentially: data loading → preprocessing → modeling → visualization
# All plots auto-save to populations/ folder with plt.savefig() before plt.show()
```

### HTML Dashboard Development
```bash
# Serve locally for Chart.js CSV loading (browsers block file:// protocol)
python -m http.server 8000
# Access dashboards at http://localhost:8000/deepseek_html_20251022_8ad066.html
# Dashboards auto-load raw/vietnam.csv via fetch(), fallback to file upload
```

### Plot Saving Pattern (Critical)
```python
# Always add before plt.show() in analysis cells
plt.savefig('populations/descriptive_filename.png', dpi=300, bbox_inches='tight')
plt.show()
```
**Examples from codebase:**
- `plt.savefig('populations/correlation_matrix_analysis.png', dpi=300, bbox_inches='tight')`
- `plt.savefig('populations/seasonal_decomposition_analysis.png', dpi=300, bbox_inches='tight')`

## Code Patterns & Conventions

### Data Handling (Vietnamese Text Critical)
- **Encoding**: `pd.read_csv(path, encoding='utf-8')` for reading, `encoding='utf-8-sig'` for Excel compatibility
- **Vietnamese Paths**: Use raw strings for filenames with diacritics: `Path(r'raw/Dân số/file.csv')`
- **Type Conversion**: `pd.to_numeric(df['column'], errors='coerce')` for mixed numeric/text columns
- **Percentage Cleaning**: `df['col'].astype(str).str.replace('%', '').astype(float)` for percentage columns

### Analysis Patterns
- **Time Series**: Sort by year ascending, handle missing years with interpolation
- **Preprocessing**: Remove outliers using IQR method, normalize with StandardScaler/MinMaxScaler
- **Modeling**: ARIMA for forecasting, Logistic/Gompertz curves via `scipy.optimize.curve_fit`
- **Statistics**: `sm.OLS(y, sm.add_constant(X)).fit()` for regression, always check `model.summary()`

### Visualization Standards
- **Style**: `plt.style.use('seaborn-v0_8')` + `sns.set_palette("husl")` for consistent theming
- **Vietnamese Labels**: Handle diacritics in plot titles and axis labels
- **High Quality**: Always save with `dpi=300, bbox_inches='tight'` for publication quality
- **Systematic Naming**: `populations/{analysis_type}_{specific}_analysis.png`

### HTML Dashboard Patterns
- **CSV Loading**: PapaParse for client-side parsing, fetch relative paths when served over HTTP
- **Data Mapping**: Flexible column detection (e.g., 'Year' or 'Năm' for time axis)
- **Responsive Design**: CSS Grid/Flexbox with Vietnamese typography (`font-family: 'Segoe UI', sans-serif`)
- **Chart.js Config**: Custom color schemes, interactive tooltips with Vietnamese labels

## Dependencies & Environment
- **Core**: `pandas>=2.0.0`, `numpy>=1.24.0`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`
- **ML**: `scikit-learn` for preprocessing, PCA, and regression
- **Jupyter**: Notebook/Lab for interactive development and visualization
- **Web**: Chart.js (CDN), PapaParse (CDN) for dashboard functionality
- **Environment**: Python 3.9+, Windows/Unix compatible with Vietnamese encoding handling

## Developer Workflows

### Adding New Analysis
1. Load and preprocess data using existing patterns in early notebook cells
2. Apply statistical methods (correlation, regression, time series analysis)
3. Create visualizations with Vietnamese labels and proper styling
4. **Critical**: Add `plt.savefig('populations/{descriptive_name}.png', dpi=300, bbox_inches='tight')` before `plt.show()`
5. Export results as JSON to `analysis/` folder for dashboard consumption

### Common Implementation Patterns
- **Data Loading**: `df = pd.read_csv(Path('raw/vietnam.csv'), encoding='utf-8')`
- **Regression**: `model = sm.OLS(y, sm.add_constant(X)).fit(); print(model.summary())`
- **Curve Fitting**: `popt, _ = curve_fit(logistic_func, t, y); y_pred = logistic_func(t, *popt)`
- **Plot Saving**: `plt.savefig(f'populations/{analysis_type}_{variable}.png', dpi=300, bbox_inches='tight')`

## Key Files to Reference
- `Dự báo dân số Việt Nam.ipynb` — Complete analysis implementation with all patterns
- `raw/vietnam.csv` — Primary data structure and Vietnamese column names
- `populations/*.png` — Current output format examples and naming conventions
- `analysis/demographic_transition_results.json` — JSON export format for dashboards
- `deepseek_html_20251022_8ad066.html` — Modern dashboard with Chart.js and Vietnamese UI
- `test.html` — Reveal.js presentation format with embedded visualizations

## Quality Gates
- **Data Integrity**: Validate 63 provinces + 5 cities, handle missing years gracefully
- **Vietnamese Support**: Ensure all text renders correctly (diacritics, fonts, encoding)
- **Plot Quality**: All matplotlib outputs saved at 300 DPI with proper aspect ratios
- **Statistical Rigor**: Report R² values, check model assumptions, validate forecasts
- **Cross-platform**: Test encoding handling on both Windows and Unix systems