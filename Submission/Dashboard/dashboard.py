import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
from pathlib import Path

def create_season_df(df):
    byseason_df = df.groupby(by="season").instant.nunique().reset_index()
    byseason_df.rename(columns={
        "instant": "sum"
    }, inplace=True)
    return byseason_df

def create_yr_df(df):
    byyr_df = df.groupby(by="yr").instant.nunique().reset_index()
    byyr_df.rename(columns={
        "instant": "sum"
    }, inplace=True)
    return byyr_df

def create_holiday_df(df):
    byholiday_df = df.groupby(by="holiday").instant.nunique().reset_index()
    byholiday_df.rename(columns={
        "instant": "sum"
    }, inplace=True)
    return byholiday_df

def create_workingday_df(df):
    byworkingday_df = df.groupby(by="workingday").instant.nunique().reset_index()
    byworkingday_df.rename(columns={
        "instant": "sum"
    }, inplace=True)
    return byworkingday_df

def create_weathersit_df(df):
    byweathersit_df = df.groupby(by="weathersit").instant.nunique().reset_index()
    byweathersit_df.rename(columns={
        "instant": "sum"
    }, inplace=True)
    return byweathersit_df

def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()

    with st.sidebar:
        st.image(
            "https://raw.githubusercontent.com/sugengcahyono/Bike_Sharing/main/Submission/Dashboard/BikeSharing.png", 
            caption="Bike Sharing Dashboard",
            use_column_width=True
        )



        date = st.date_input(
            label="Rentang Waktu", 
            min_value=min_date, 
            max_value=max_date,
            value=[min_date, max_date]
        )


    return date

def display_chart(title, x, y, data, xlabel=None, ylabel=None):
    st.subheader(title)
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(x=x, y=y, data=data, ax=ax, palette="viridis")
    ax.set_title(title, fontsize=25, color="navy")

    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)
    sns.despine()
    st.pyplot(fig)  

if __name__ == "__main__":
    sns.set(style="darkgrid")
    st.title("Bike Sharing Dashboard ")
    st.markdown("""---""")

    # Load data
    day_df_csv = "https://raw.githubusercontent.com/sugengcahyono/Bike_Sharing/main/Submission/Dashboard/day_clean.csv"
    day_df = pd.read_csv(day_df_csv)

    # Sidebar
    date = sidebar(day_df)
    if len(date) == 2:
        main_df = day_df[(day_df["dteday"] >= str(date[0])) & (day_df["dteday"] <= str(date[1]))]
    else:
        main_df = day_df

    # Create DataFrames for Visualization
    season_df = create_season_df(main_df)
    year_df = create_yr_df(main_df)
    holiday_df = create_holiday_df(main_df)
    workingday_df = create_workingday_df(main_df)
    weathersit_df = create_weathersit_df(main_df)

    # Visualizations
    st.markdown("### Overview of Bike Sharing Data")
    display_chart("Bike Sharing by Season", "season", "sum", season_df)
    display_chart("Bike Sharing by Year", "yr", "sum", year_df)
    display_chart("Bike Sharing by Holiday", "holiday", "sum", holiday_df)
    display_chart("Bike Sharing by Working Day", "workingday", "sum", workingday_df)
    display_chart("Bike Sharing by Weather Situation", "weathersit", "sum", weathersit_df)

    # Footer
    st.markdown("""---""")
    year_copyright = datetime.date.today().year
    st.caption(
        f"Copyright © {year_copyright} | Bike Sharing Dashboard | All Rights Reserved | "
        f"Made by [@SugengCahyono](https://www.linkedin.com/in/muhamad-sugeng-cahyono/)"
    )
