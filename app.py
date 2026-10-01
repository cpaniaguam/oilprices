import json
from pathlib import Path

import pandas as pd
import streamlit as st

HISTORY_FILE = Path(__file__).parent / "price_history.json"


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    records = json.loads(path.read_text())
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df["price"] = pd.to_numeric(df["price"])
    # Stable sort keeps same-day entries in the order they were recorded.
    return df.sort_values("date", kind="stable").reset_index(drop=True)


st.set_page_config(page_title="Oil Prices", page_icon="🛢️", layout="wide")
st.title("🛢️ Heating Oil Price History")

df = load_data(HISTORY_FILE)

# --- Sidebar filters ---
st.sidebar.header("Filters")

min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

companies = sorted(df["company"].unique())
selected_companies = st.sidebar.multiselect(
    "Companies",
    options=companies,
    default=companies,
)

# --- Apply filters ---
filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[
        (filtered["date"].dt.date >= start) & (filtered["date"].dt.date <= end)
    ]
if selected_companies:
    filtered = filtered[filtered["company"].isin(selected_companies)]

if filtered.empty:
    st.warning("No records match the current filters.")
    st.stop()

# The service appends a new entry whenever the low changes during a day,
# so the last entry per date is that day's lowest price.
daily = filtered.drop_duplicates("date", keep="last")

# --- Latest low price ---
best = daily.iloc[-1]
latest_date = best["date"]

# --- KPIs ---
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
col1.metric("Records", len(filtered))
col2.metric("Companies", filtered["company"].nunique())
col3.metric("Lowest price", f"${filtered['price'].min():.3f}")
col4.metric("Average price", f"${filtered['price'].mean():.3f}")
col5.metric("Latest low", best["company"])
col5.markdown(f"**${best['price']:.3f} on {latest_date.date()}**")

trend_tab, top_tab, records_tab = st.tabs(["📈 Trend", "🏆 Top 3", "📋 Records"])

# --- Price trend (daily low) ---
with trend_tab:
    st.line_chart(daily.set_index(daily["date"].dt.date)["price"].rename("lowest_price"))

# --- Top providers (most often the lowest price) ---
with top_tab:
    st.caption("Providers ranked by how often they had the lowest price.")
    counts = filtered["company"].value_counts()
    total = len(filtered)
    medals = ["🥇", "🥈", "🥉"]
    for medal, (company, count) in zip(medals, counts.head(3).items()):
        st.markdown(f"### {medal} {company}")
        st.markdown(f"**{count} times** · {count / total:.0%} of records")

# --- Raw data ---
with records_tab:
    st.dataframe(
        filtered.assign(date=filtered["date"].dt.date).sort_values(
            "date", ascending=False
        ),
        width="stretch",
        hide_index=True,
    )
