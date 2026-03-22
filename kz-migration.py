"""
Kazakhstan Internal Migration Dashboard
========================================
Interactive data visualization of internal migration flows
across Kazakhstan's regions from 2010 to 2025.

Data source: Bureau of National Statistics, Republic of Kazakhstan
             (stat.gov.kz) — origin-destination flow records

Author: Diar Islambekov
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ── Load & clean data ─────────────────────────────────────────────────────────

df = pd.read_csv("data/Internal_migration.csv")
df.columns = df.columns.str.strip()

# Clean region names for display
name_map = {
    "Almaty_city":   "Almaty city",
    "Astana_city":   "Astana",
    "Shymkent_city": "Shymkent",
    "North_Kaz":     "North Kazakhstan",
    "East_Kaz":      "East Kazakhstan",
    "West_Kaz":      "West Kazakhstan",
}
df["origin"]      = df["region_emmigr"].replace(name_map)
df["destination"] = df["region_immigr"].replace(name_map)
df["year"]        = df["Year"].astype(int)
df["flow"]        = df["N"].astype(int)

all_regions = sorted(set(df["origin"]) | set(df["destination"]))
all_years   = sorted(df["year"].unique())

# ── Net migration by region and year ─────────────────────────────────────────

def get_net_migration(year=None):
    d = df if year is None else df[df["year"] == year]
    arrivals   = d.groupby("destination")["flow"].sum().rename("arrivals")
    departures = d.groupby("origin")["flow"].sum().rename("departures")
    net = pd.DataFrame({"arrivals": arrivals, "departures": departures}).fillna(0)
    net["net"] = net["arrivals"] - net["departures"]
    return net.sort_values("net")

# ── Region coordinates for bubble map ────────────────────────────────────────

coords = {
    "Astana":          (51.18, 71.45),
    "Almaty city":     (43.25, 76.95),
    "Shymkent":        (42.32, 69.59),
    "Almaty":          (44.00, 77.50),
    "Zhetysu":         (44.80, 79.20),
    "Aktobe":          (50.28, 57.21),
    "Atyrau":          (47.11, 51.92),
    "West Kazakhstan": (51.23, 51.37),
    "Akmola":          (51.50, 70.00),
    "Kyzylorda":       (44.85, 65.51),
    "Pavlodar":        (52.29, 76.97),
    "Karaganda":       (49.80, 73.09),
    "Kostanay":        (53.21, 63.63),
    "Zhambyl":         (42.90, 71.38),
    "Mangystau":       (43.67, 51.15),
    "North Kazakhstan":(54.87, 69.15),
    "East Kazakhstan": (49.97, 82.61),
    "Turkestan":       (41.17, 68.25),
    "Abay":            (49.50, 80.00),
    "Ulytau":          (48.00, 67.00),
}

def net_color(v):
    if v > 20000:  return "#1D4ED8"
    if v > 5000:   return "#2563EB"
    if v > 0:      return "#93C5FD"
    if v > -5000:  return "#FCA5A5"
    if v > -10000: return "#EF4444"
    return "#B91C1C"

# ── Build dashboard ────────────────────────────────────────────────────────────

def build_dashboard():
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            "Net migration by region — 2023",
            "Top 10 migration corridors — 2023",
            "Geographic distribution of net flows — 2023",
            "Net migration trend — major cities (2010–2025)",
            "Total internal migration volume by year",
            "Top origin regions (total outflow, all years)",
        ),
        specs=[
            [{"type": "bar"},             {"type": "bar"}],
            [{"type": "scattergeo"},      {"type": "scatter"}],
            [{"type": "bar"},             {"type": "bar"}],
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.08,
        row_heights=[0.33, 0.34, 0.33],
    )

    # ── Panel 1: Net migration bar chart (2023) ───────────────────────────────
    net23 = get_net_migration(2023)
    clrs  = ["#2563EB" if v >= 0 else "#DC2626" for v in net23["net"]]

    fig.add_trace(go.Bar(
        x=net23["net"], y=net23.index,
        orientation="h",
        marker_color=clrs,
        text=[f"{v:+,.0f}" for v in net23["net"]],
        textposition="outside",
        textfont=dict(size=8, family="IBM Plex Mono"),
        hovertemplate="%{y}<br>Arrivals: %{customdata[0]:,}<br>Departures: %{customdata[1]:,}<br>Net: %{x:+,}<extra></extra>",
        customdata=list(zip(net23["arrivals"].astype(int), net23["departures"].astype(int))),
        name="Net migration",
        showlegend=False,
    ), row=1, col=1)

    # ── Panel 2: Top corridors (2023) ─────────────────────────────────────────
    top10 = (
        df[df["year"] == 2023]
        .sort_values("flow", ascending=True)
        .tail(10)
    )
    top10["label"] = top10["origin"] + " → " + top10["destination"]

    fig.add_trace(go.Bar(
        x=top10["flow"], y=top10["label"],
        orientation="h",
        marker_color="#2563EB",
        text=[f"{v:,}" for v in top10["flow"]],
        textposition="outside",
        textfont=dict(size=8, family="IBM Plex Mono"),
        hovertemplate="%{y}: %{x:,} people<extra></extra>",
        name="Corridor flow",
        showlegend=False,
    ), row=1, col=2)

    # ── Panel 3: Bubble map (2023) ────────────────────────────────────────────
    net23_full = get_net_migration(2023)
    lats, lons, texts, bcolors, sizes = [], [], [], [], []
    for region in net23_full.index:
        if region in coords:
            lat, lon = coords[region]
            v = net23_full.loc[region, "net"]
            lats.append(lat)
            lons.append(lon)
            texts.append(f"<b>{region}</b><br>Net: {v:+,.0f}<br>Arrivals: {int(net23_full.loc[region,'arrivals']):,}<br>Departures: {int(net23_full.loc[region,'departures']):,}")
            bcolors.append(net_color(v))
            sizes.append(max(8, min(42, abs(v) / 1100)))

    fig.add_trace(go.Scattergeo(
        lat=lats, lon=lons,
        text=texts, hoverinfo="text",
        mode="markers",
        marker=dict(size=sizes, color=bcolors, opacity=0.85,
                    line=dict(width=0.8, color="white")),
        showlegend=False,
    ), row=2, col=1)

    # ── Panel 4: City trend lines ─────────────────────────────────────────────
    cities = ["Astana", "Almaty city", "Shymkent"]
    city_palette = {"Astana": "#1A1A2E", "Almaty city": "#2563EB", "Shymkent": "#D97706"}

    for city in cities:
        trend = []
        for yr in all_years:
            net = get_net_migration(yr)
            v = net.loc[city, "net"] if city in net.index else 0
            trend.append({"year": yr, "net": v})
        trend_df = pd.DataFrame(trend)
        fig.add_trace(go.Scatter(
            x=trend_df["year"], y=trend_df["net"],
            mode="lines+markers",
            name=city,
            line=dict(color=city_palette[city], width=2),
            marker=dict(size=5),
            hovertemplate=f"{city} %{{x}}: %{{y:+,}}<extra></extra>",
        ), row=2, col=2)

    # ── Panel 5: Total volume by year ─────────────────────────────────────────
    vol = df.groupby("year")["flow"].sum().reset_index()
    fig.add_trace(go.Bar(
        x=vol["year"], y=vol["flow"],
        marker_color="#1A1A2E",
        text=[f"{v/1000:.0f}k" for v in vol["flow"]],
        textposition="outside",
        textfont=dict(size=9, family="IBM Plex Mono"),
        hovertemplate="Year %{x}: %{y:,} moves<extra></extra>",
        showlegend=False,
    ), row=3, col=1)

    # ── Panel 6: Top origin regions ───────────────────────────────────────────
    top_origins = (
        df.groupby("origin")["flow"].sum()
        .sort_values(ascending=True)
        .tail(10)
    )
    fig.add_trace(go.Bar(
        x=top_origins.values, y=top_origins.index,
        orientation="h",
        marker_color="#EF4444",
        text=[f"{v/1000:.0f}k" for v in top_origins.values],
        textposition="outside",
        textfont=dict(size=8, family="IBM Plex Mono"),
        hovertemplate="%{y}: %{x:,} total departures<extra></extra>",
        showlegend=False,
    ), row=3, col=2)

    # ── Global layout ─────────────────────────────────────────────────────────
    fig.update_layout(
        title=dict(
            text=(
                "Kazakhstan — Internal Migration Flows Dashboard<br>"
                "<sup>Source: Bureau of National Statistics, Republic of Kazakhstan (stat.gov.kz) · "
                "Origin-destination flow records 2010–2025 · Author: Diar Islambekov</sup>"
            ),
            font=dict(size=17, family="IBM Plex Sans", color="#1A1A2E"),
            x=0.01, xanchor="left",
        ),
        height=1200,
        paper_bgcolor="#F7F8FA",
        plot_bgcolor="#FFFFFF",
        font=dict(family="IBM Plex Sans", size=11, color="#374151"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.005,
            xanchor="right", x=1,
            font=dict(size=11),
            title=dict(text="City trend:"),
        ),
        margin=dict(l=40, r=60, t=100, b=40),
    )

    # Axis styling
    for row, col in [(1,1),(1,2),(3,1),(3,2)]:
        fig.update_xaxes(showgrid=True, gridcolor="#F3F4F6",
                         zeroline=True, zerolinecolor="#D1D5DB",
                         tickfont=dict(size=9), row=row, col=col)
        fig.update_yaxes(tickfont=dict(size=9), row=row, col=col)

    fig.update_xaxes(tickfont=dict(size=10), tickvals=all_years, row=2, col=2)
    fig.update_yaxes(showgrid=True, gridcolor="#F3F4F6",
                     tickformat=",", row=2, col=2)
    fig.update_xaxes(tickangle=-30, tickfont=dict(size=10), row=3, col=1)

    fig.update_geos(
        visible=True,
        showcoastlines=True,  coastlinecolor="#D1D5DB",
        showland=True,        landcolor="#F9FAFB",
        showborders=True,     bordercolor="#E5E7EB",
        showocean=True,       oceancolor="#EFF6FF",
        center=dict(lat=48, lon=68),
        projection_scale=4.2,
        lataxis_range=[40, 57],
        lonaxis_range=[49, 88],
    )

    for ann in fig.layout.annotations:
        ann.font = dict(size=11, family="IBM Plex Sans", color="#1A1A2E")

    return fig


# ── Run ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading data...")
    print(f"  {len(df):,} migration flow records")
    print(f"  Years: {all_years}")
    print(f"  Regions: {len(all_regions)}")
    print()
    print("Building dashboard...")

    fig = build_dashboard()

    output = "kazakhstan_migration_dashboard.html"
    fig.write_html(
        output,
        include_plotlyjs="cdn",
        full_html=True,
        config={
            "displayModeBar": True,
            "modeBarButtonsToRemove": ["sendDataToCloud"],
            "displaylogo": False,
            "responsive": True,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "kazakhstan_migration_dashboard",
                "scale": 2,
            },
        },
    )
    print(f"Dashboard saved → {output}")
    print("Run `open kazakhstan_migration_dashboard.html` to view it.")
