import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import openpyxl as xl

# Set page config for full-screen layout
st.set_page_config(page_title="Little BusBuddy Dashboard", page_icon="😍", layout="wide")

# Streamlit app title and layout
st.title("😍 BusBuddy Performance Dashboard")
st.subheader("2025 Quarterly Targets vs Achieved")

# Filters
product_filter = st.selectbox("Product:", ["All Products", "SaaS", "TaaS"])
quarter_filter = st.selectbox("Quarter:", ["Q1", "Q2", "Q3", "Q4", "YTD"])

try:
    # Load data from Excel file
    revenue_data = pd.read_excel("busbuddy.xlsx", sheet_name="Revenue")
    acquisition_data = pd.read_excel("busbuddy.xlsx", sheet_name="Acquisition")

    # Clean percentage data (remove % and convert to float), ensuring string input
    for df in [revenue_data, acquisition_data]:
        df["% of Target"] = df["% of Target"].astype(str).str.replace("%", "").replace("", np.nan).astype(float)

    # Filter data based on product and quarter
    def filter_data(df, product, quarter):
        if product != "All Products":
            df = df[df["Product"] == product]
        if quarter != "YTD":
            df = df[df["Quarter"] == quarter]
        else:
            df = df[df["Quarter"] == "Cumulative Performance (YTD)"]
        return df

    revenue_df = filter_data(revenue_data, product_filter, quarter_filter)
    acquisition_df = filter_data(acquisition_data, product_filter, quarter_filter)

    # Calculate totals
    net_revenue_total = pd.to_numeric(revenue_df[revenue_df["Metric"] == "Net Revenue"]["Achieved ($)"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce").sum()
    gross_revenue_total = pd.to_numeric(revenue_df[revenue_df["Metric"] == "Gross Revenue"]["Achieved ($)"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce").sum()
    gross_adds_total = pd.to_numeric(acquisition_df[acquisition_df["Metric"] == "Gross Adds"]["Achieved"].astype(str), errors="coerce").sum()
    net_adds_total = pd.to_numeric(acquisition_df[acquisition_df["Metric"] == "Net Adds"]["Achieved"].astype(str), errors="coerce").sum()

    net_revenue_target = pd.to_numeric(revenue_df[revenue_df["Metric"] == "Net Revenue"]["Target ($)"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce").sum()
    gross_revenue_target = pd.to_numeric(revenue_df[revenue_df["Metric"] == "Gross Revenue"]["Target ($)"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce").sum()
    gross_adds_target = pd.to_numeric(acquisition_df[acquisition_df["Metric"] == "Gross Adds"]["Target"].astype(str), errors="coerce").sum()
    net_adds_target = pd.to_numeric(acquisition_df[acquisition_df["Metric"] == "Net Adds"]["Target"].astype(str), errors="coerce").sum()

    net_revenue_pct = (net_revenue_total / net_revenue_target * 100) if net_revenue_target else 0
    gross_revenue_pct = (gross_revenue_total / gross_revenue_target * 100) if gross_revenue_target else 0
    gross_adds_pct = (gross_adds_total / gross_adds_target * 100) if gross_adds_target else 0
    net_adds_pct = (net_adds_total / net_adds_target * 100) if net_adds_target else 0

    # Display totals with styled boxes
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div style="background-color: #00008B; padding: 5px; border-radius: 5px; margin-bottom: 10px; font-style: italic; text-align: center;">
                <h3 style="margin: 0;">Net Revenue</h3>
                <p style="font-size: 30px; margin: 5px 0;">${net_revenue_total:,.0f}</p>
                <p style="margin: 0;">{net_revenue_pct:.0f}% of target</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div style="background-color: #00008B; padding: 5px; border-radius: 5px; margin-bottom: 10px; font-style: italic; text-align: center;">
                <h3 style="margin: 0;">Gross Revenue</h3>
                <p style="font-size: 30px; margin: 5px 0;">${gross_revenue_total:,.0f}</p>
                <p style="margin: 0;">{gross_revenue_pct:.0f}% of target</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div style="background-color: #00008B; padding: 5px; border-radius: 5px; margin-bottom: 10px; font-style: italic; text-align: center;">
                <h3 style="margin: 0;">Gross Adds</h3>
                <p style="font-size: 30px; margin: 5px 0;">{gross_adds_total:,.0f}</p>
                <p style="margin: 0;">{gross_adds_pct:.0f}% of target</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"""
            <div style="background-color: #00008B; padding: 5px; border-radius: 5px; margin-bottom: 10px; font-style: italic; text-align: center;">
                <h3 style="margin: 0;">Net Adds</h3>
                <p style="font-size: 30px; margin: 5px 0;">{net_adds_total:,.0f}</p>
                <p style="margin: 0;">{net_adds_pct:.0f}% of target</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Revenue Performance
    st.subheader("Revenue Performance")
    revenue_df_display = revenue_df[["Quarter", "Product", "Metric", "Target ($)", "Achieved ($)", "% of Target"]].copy()
    revenue_df_display["Target ($)"] = pd.to_numeric(revenue_df_display["Target ($)"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce")
    revenue_df_display["Achieved ($)"] = pd.to_numeric(revenue_df_display["Achieved ($)"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce")
    st.table(revenue_df_display.style.format({
        "Target ($)": "${:,.0f}",
        "Achieved ($)": "${:,.0f}",
        "% of Target": "{:.0f}%"
    }))

    # Acquisition Metrics
    st.subheader("Acquisition Metrics")
    acquisition_df_display = acquisition_df[["Quarter", "Product", "Metric", "Target", "Achieved", "% of Target"]].copy()
    acquisition_df_display["Target"] = pd.to_numeric(acquisition_df_display["Target"].astype(str), errors="coerce")
    acquisition_df_display["Achieved"] = pd.to_numeric(acquisition_df_display["Achieved"].astype(str), errors="coerce")
    st.table(acquisition_df_display.style.format({
        "Target": "{:,.0f}",
        "Achieved": "{:,.0f}",
        "% of Target": "{:.0f}%"
    }))

    # Quarterly Trends for Revenue Performance (Comparison Bar Charts with Plotly)
    if quarter_filter != "YTD":
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        revenue_df_all = revenue_data[revenue_data["Quarter"].isin(quarters)].copy()

        # Pivot data to aggregate by quarter
        gross_revenue_pivot = revenue_df_all[revenue_df_all["Metric"] == "Gross Revenue"].pivot_table(
            index="Quarter", values=["Target ($)", "Achieved ($)"], aggfunc="sum", fill_value=0
        )
        net_revenue_pivot = revenue_df_all[revenue_df_all["Metric"] == "Net Revenue"].pivot_table(
            index="Quarter", values=["Target ($)", "Achieved ($)"], aggfunc="sum", fill_value=0
        )

        # Gross Revenue Comparison Bar Chart
        st.subheader("Gross Revenue Trends")
        gross_target = pd.to_numeric(gross_revenue_pivot["Target ($)"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce").reindex(quarters, fill_value=0)
        gross_achieved = pd.to_numeric(gross_revenue_pivot["Achieved ($)"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce").reindex(quarters, fill_value=0)
        forecast_gross = gross_target * 1.1
        chart_data = pd.DataFrame({
            "Quarter": quarters * 3,
            "Value": list(gross_target) + list(gross_achieved) + list(forecast_gross),
            "Type": ["Target"] * 4 + ["Achieved"] * 4 + ["Forecast"] * 4
        })
        fig = px.bar(chart_data, x="Quarter", y="Value", color="Type", barmode="group", title="Gross Revenue Trends",
                     color_discrete_map={"Target": "red", "Achieved": "green", "Forecast": "yellow"})
        st.plotly_chart(fig)

        # Net Revenue Comparison Bar Chart
        st.subheader("Net Revenue Trends")
        net_target = pd.to_numeric(net_revenue_pivot["Target ($)"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce").reindex(quarters, fill_value=0)
        net_achieved = pd.to_numeric(net_revenue_pivot["Achieved ($)"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce").reindex(quarters, fill_value=0)
        forecast_net = net_target * 1.05
        chart_data = pd.DataFrame({
            "Quarter": quarters * 3,
            "Value": list(net_target) + list(net_achieved) + list(forecast_net),
            "Type": ["Target"] * 4 + ["Achieved"] * 4 + ["Forecast"] * 4
        })
        fig = px.bar(chart_data, x="Quarter", y="Value", color="Type", barmode="group", title="Net Revenue Trends",
                     color_discrete_map={"Target": "red", "Achieved": "green", "Forecast": "yellow"})
        st.plotly_chart(fig)

    # Quarterly Trends for Acquisition Metrics (Comparison Bar Charts with Plotly)
    if quarter_filter != "YTD":
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        acquisition_df_all = acquisition_data[acquisition_data["Quarter"].isin(quarters)].copy()

        # Pivot data to aggregate by quarter
        gross_adds_pivot = acquisition_df_all[acquisition_df_all["Metric"] == "Gross Adds"].pivot_table(
            index="Quarter", values=["Target", "Achieved"], aggfunc="sum", fill_value=0
        )
        net_adds_pivot = acquisition_df_all[acquisition_df_all["Metric"] == "Net Adds"].pivot_table(
            index="Quarter", values=["Target", "Achieved"], aggfunc="sum", fill_value=0
        )

        # Gross Adds Comparison Bar Chart
        st.subheader("Gross Adds Trends")
        gross_adds_target = pd.to_numeric(gross_adds_pivot["Target"].astype(str), errors="coerce").reindex(quarters, fill_value=0)
        gross_adds_achieved = pd.to_numeric(gross_adds_pivot["Achieved"].astype(str), errors="coerce").reindex(quarters, fill_value=0)
        forecast_gross_adds = gross_adds_target * 1.1
        chart_data = pd.DataFrame({
            "Quarter": quarters * 3,
            "Value": list(gross_adds_target) + list(gross_adds_achieved) + list(forecast_gross_adds),
            "Type": ["Target"] * 4 + ["Achieved"] * 4 + ["Forecast"] * 4
        })
        fig = px.bar(chart_data, x="Quarter", y="Value", color="Type", barmode="group", title="Gross Adds Trends",
                     color_discrete_map={"Target": "red", "Achieved": "green", "Forecast": "yellow"})
        st.plotly_chart(fig)

        # Net Adds Comparison Bar Chart
        st.subheader("Net Adds Trends")
        net_adds_target = pd.to_numeric(net_adds_pivot["Target"].astype(str), errors="coerce").reindex(quarters, fill_value=0)
        net_adds_achieved = pd.to_numeric(net_adds_pivot["Achieved"].astype(str), errors="coerce").reindex(quarters, fill_value=0)
        forecast_net_adds = net_adds_target * 1.05
        chart_data = pd.DataFrame({
            "Quarter": quarters * 3,
            "Value": list(net_adds_target) + list(net_adds_achieved) + list(forecast_net_adds),
            "Type": ["Target"] * 4 + ["Achieved"] * 4 + ["Forecast"] * 4
        })
        fig = px.bar(chart_data, x="Quarter", y="Value", color="Type", barmode="group", title="Net Adds Trends",
                     color_discrete_map={"Target": "red", "Achieved": "green", "Forecast": "yellow"})
        st.plotly_chart(fig)

    # Cumulative Performance
    if quarter_filter == "YTD":
        st.subheader("Cumulative Performance")
        ytd_df = revenue_df[["Quarter", "Product", "Metric", "Target ($)", "Achieved ($)", "% of Target"]].rename(columns={
            "Target ($)": "Annual Target",
            "Achieved ($)": "YTD Achieved",
            "% of Target": "% of Annual"
        })
        ytd_df["Annual Target"] = pd.to_numeric(ytd_df["Annual Target"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce")
        ytd_df["YTD Achieved"] = pd.to_numeric(ytd_df["YTD Achieved"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce")
        st.table(ytd_df.style.format({
            "Annual Target": "${:,.0f}",
            "YTD Achieved": "${:,.0f}",
            "% of Annual": "{:.0f}%"
        }))

except Exception as e:
    st.error(f"Error fetching data: {str(e)}")
    st.write("Please ensure the 'busbuddy.xlsx' file is in the project directory with 'Revenue' and 'Acquisition' sheets.")