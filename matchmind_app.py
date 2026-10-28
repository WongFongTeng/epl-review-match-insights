
import streamlit as st

st.set_page_config(
    page_title="MatchMind AI",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ MatchMind AI")
st.subheader("Football Analytics & Key-Moment Insights")

st.info(
    "Welcome! MatchMind AI analyses football events "
    "to uncover team activity, passing performance, "
    "and important moments during a match."
)

st.header("Our First Simulated Match")

col1, col2 = st.columns(2)

with col1:
    st.metric("Arsenal", "248 events")

with col2:
    st.metric("Liverpool", "202 events")

st.caption(
    "Demo data: this is a fictional simulated match, "
    "not an actual Premier League result."
)

st.markdown("---")
st.write("Built for the Microsoft Inside the Game Hackathon.")



st.header("Match Statistics")

st.subheader("Event Comparison")

import pandas as pd

# Create simulated event data for Key Moments
import random

random.seed(42)

events = []

for minute in range(1, 91):
    for _ in range(5):
        team = random.choice(["Arsenal", "Liverpool"])
        event_type = random.choices(
            ["pass", "shot", "tackle", "pressure"],
            weights=[65, 10, 10, 15],
            k=1
        )[0]

        events.append({
            "minute": minute,
            "team": team,
            "event_type": event_type
        })

df = pd.DataFrame(events)



event_data = pd.DataFrame({
    "Event Type": ["Passes", "Shots", "Tackles", "Pressure"],
    "Arsenal": [165, 17, 25, 41],
    "Liverpool": [135, 17, 20, 30]
})

st.bar_chart(
    event_data.set_index("Event Type")
)

st.subheader("Pass Completion Rate")

pass_data = pd.DataFrame({
    "Team": ["Arsenal", "Liverpool"],
    "Completion Rate (%)": [82.4, 85.2]
})

st.bar_chart(
    pass_data.set_index("Team")
)

# Key Moments
st.markdown("---")
st.header("Key Moments")

st.write(
    "MatchMind AI identifies the busiest periods of the simulated match "
    "by analysing shots and pressure events."
)

# Count shots and pressure events in each 10-minute period
df["period_start"] = ((df["minute"] - 1) // 10) * 10 + 1

key_events = df[df["event_type"].isin(["shot", "pressure"])]

activity = (
    key_events.groupby(["period_start", "team", "event_type"])
    .size()
    .unstack(fill_value=0)
)

for event in ["shot", "pressure"]:
    if event not in activity.columns:
        activity[event] = 0

activity["key_activity"] = activity["shot"] + activity["pressure"]

period_summary = (
    activity.groupby(level="period_start")[["shot", "pressure", "key_activity"]]
    .sum()
    .sort_values("key_activity", ascending=False)
)

if not period_summary.empty:
    busiest_period = int(period_summary.index[0])
    busiest = period_summary.iloc[0]

    period_end = min(busiest_period + 9, 90)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Busiest Period",
        f"{busiest_period}–{period_end} min"
    )

    col2.metric("Shots", int(busiest["shot"]))

    col3.metric("Pressure Events", int(busiest["pressure"]))

    st.subheader("Top 5 Key Moments")

    top_periods = period_summary.head(5).reset_index()
    top_periods["Period"] = top_periods["period_start"].apply(
        lambda minute: f"{minute}–{min(minute + 9, 90)} min"
    )

    top_periods = top_periods[
        ["Period", "shot", "pressure", "key_activity"]
    ]

    top_periods.columns = [
        "Match Period",
        "Shots",
        "Pressure Events",
        "Total Key Events"
    ]

    st.dataframe(top_periods, hide_index=True, use_container_width=True)

    st.bar_chart(
        period_summary[["shot", "pressure"]].sort_index()
    )

    st.info(
        f"The busiest period was minutes {busiest_period}–{period_end}, "
        f"with {int(busiest['shot'])} shots and "
        f"{int(busiest['pressure'])} pressure events."
    )

st.caption(
    "Key moments are calculated from fictional simulated match data."
)


st.markdown("---")

st.subheader("⚽ Explore EPL Review")

st.write(
    "MatchMind AI is an experimental football analytics project "
    "exploring match statistics and key-moment insights."
)

st.markdown(
    "[Visit EPL Review](https://www.eplreview.com/)"
)

st.caption(
    "This demo uses fictional simulated match data, "
    "not data sourced from EPL Review."
)


