# Kazakhstan Internal Migration Dashboard

An interactive data visualization of internal migration flows across Kazakhstan's regions from 2010 to 2025, built with Python and Plotly.

## Overview

This project analyses origin-destination migration flow data from Kazakhstan's Bureau of National Statistics, covering 3,039 migration corridors across 20 regions over 8 years. The dashboard reveals the dominant urban pull of Astana, Almaty, and Shymkent — and the persistent population loss in northern and eastern oblasts.


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
│   └── Internal_migration.csv   # Raw data
├── dashboard.py                  # Main Python script
├── requirements.txt              # Python dependencies
└── README.md
```

## Setup & usage

**1. Clone the repository**
```bash
git clone https://github.com/diar299/kz-migration.git
cd kz-migration
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the dashboard**
```bash
python dashboard.py
```

This generates `kazakhstan_migration_dashboard.html` — open it in any browser.

## Requirements

```
pandas>=1.5.0
plotly>=5.15.0
```

## Dashboard panels

1. **Net migration by region (2023)** — horizontal bar chart showing which regions gain and lose population
2. **Top 10 migration corridors (2023)** — the busiest origin-destination pairs
3. **Geographic bubble map (2023)** — spatial view of net flows, bubble size = migration intensity
4. **City trend lines (2010–2025)** — net inflow to Astana, Almaty city, and Shymkent over time
5. **Total migration volume by year** — overall internal mobility trend
6. **Top origin regions (all years)** — cumulative outflow by region

## Author

**Diar Islambekov** — Public policy researcher specialising in governance and Central Asia.

- Portfolio: [diar299.github.io](https://diar299.github.io)
- GitHub: [@diar299](https://github.com/diar299)
- Email: diar.islambekov@gmail.com

## License

Data is sourced from Kazakhstan's Bureau of National Statistics and is publicly available. Code is MIT licensed.
