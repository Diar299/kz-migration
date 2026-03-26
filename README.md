# Kazakhstan Internal Migration Dashboard

Interactive analysis of internal migration flows across Kazakhstan's regions from 2010 to 2025, built with Python and Plotly.

## View the dashboard

**[Open interactive notebook on nbviewer →](https://nbviewer.org/github/diar-islambekov/kz-migration/blob/main/migration_analysis.ipynb)**

## Overview

This project analyses origin-destination migration flow data from Kazakhstan's Bureau of National Statistics, covering 3,039 migration corridors across 20 regions over 8 years. The analysis reveals the dominant urban pull of Astana, Almaty, and Shymkent — and the persistent population loss in northern and eastern oblasts.

## Key findings

- Only **3 of 20 regions** consistently gain population from internal migration: Astana, Almaty city, and Shymkent
- The **Almaty → Almaty city** corridor is the single largest migration flow in 2025 (36,729 people)
- **Northern oblasts** (North Kazakhstan, East Kazakhstan, Kostanay) are the fastest-depopulating regions
- Internal migration volumes have **increased significantly since 2020**, with 2025 showing the highest recorded flows
- **Almaty region** emerged as a net gainer in 2024 — a new suburbanisation signal around Almaty city

## Data

| File | Description |
|------|-------------|
| `data/Internal_migration.csv` | Raw origin-destination flow data |

**Columns:**
- `Year` — year of migration record
- `region_emmigr` — origin region
- `region_immigr` — destination region
- `N` — number of people who moved

**Source:** Bureau of National Statistics of the Agency for Strategic Planning and Reforms of the Republic of Kazakhstan ([stat.gov.kz](https://stat.gov.kz))

## Project structure

```
kz-migration/
├── data/
│   └── Internal_migration.csv    # Raw data
├── migration_analysis.ipynb      # Jupyter notebook with charts
├── requirements.txt              # Python dependencies
└── README.md
```

## Setup & usage

**1. Clone the repository**
```bash
git clone https://github.com/diar-islambekov/kz-migration.git
cd kz-migration
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Open the notebook**
```bash
jupyter notebook migration_analysis.ipynb
```

## Requirements

```
pandas>=1.5.0
plotly>=5.15.0
```

## Charts

1. **Net migration by region (2023)** — which regions gain and lose population
2. **Top 10 migration corridors (2023)** — the busiest origin-destination pairs
3. **City trend lines (2010–2025)** — net inflow to Astana, Almaty city, and Shymkent over time
4. **Total migration volume by year** — overall internal mobility trend

## Author

**Diar Islambekov** — Public policy researcher specialising in governance and Central Asia.

- Portfolio: [diar-islambekov.github.io](https://diar-islambekov.github.io)
- GitHub: [@diar-islambekov](https://github.com/diar-islambekov)
- Email: diar.islambekov@gmail.com

## License

Data is sourced from Kazakhstan's Bureau of National Statistics and is publicly available. Code is MIT licensed.
