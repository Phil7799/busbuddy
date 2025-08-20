import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page config for full-screen layout
st.set_page_config(page_title="Little BusBuddy Dashboard", page_icon="https://res.cloudinary.com/dnq8ne9lx/image/upload/v1753860594/infograph_ewfmm6.ico", layout="wide")

# Streamlit app title and layout
st.title("😍 BusBuddy Performance Dashboard")
st.subheader("2025 Quarterly Targets vs Achieved")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    owner_filter = st.selectbox("Owner:", ["All Owners", "Peter", "Mercy"])
with col2:
    product_filter = st.selectbox("Product:", ["All Products", "SaaS", "TaaS"])
with col3:
    quarter_filter = st.selectbox("Quarter:", ["Q1", "Q2", "Q3", "Q4", "YTD"])

try:
    # Load data from Excel file
    revenue_data = pd.read_excel("busbuddy.xlsx", sheet_name="Revenue")
    acquisition_data = pd.read_excel("busbuddy.xlsx", sheet_name="Acquisition")

    # Normalize column names (rename (KES) columns if present)
    for df in [revenue_data, acquisition_data]:
        if "Target (KES)" in df.columns:
            df.rename(columns={"Target (KES)": "Target", "Achieved (KES)": "Achieved"}, inplace=True)

    # Clean and convert columns to numeric, removing KES and commas
    for df in [revenue_data, acquisition_data]:
        df["Target"] = pd.to_numeric(df["Target"].astype(str).str.replace("[KES,]", "", regex=True), errors="coerce")
        df["Achieved"] = pd.to_numeric(df["Achieved"].astype(str).str.replace("[KES,]", "", regex=True), errors="coerce")
        # Calculate % of Target dynamically
        df["% of Target"] = (df["Achieved"] / df["Target"] * 100).round(0)
        df["% of Target"] = df["% of Target"].replace([np.inf, -np.inf], np.nan).fillna(0)

    # Filter data based on owner, product, and quarter (for KPIs and tables only)
    def filter_data(df, owner, product, quarter):
        filtered_df = df.copy()
        if owner != "All Owners":
            filtered_df = filtered_df[filtered_df["Owner"] == owner]
        if product != "All Products":
            filtered_df = filtered_df[filtered_df["Product"] == product]
        if quarter != "YTD":
            filtered_df = filtered_df[filtered_df["Quarter"] == quarter]
        else:
            filtered_df = filtered_df[filtered_df["Quarter"] == "Cumulative Performance (YTD)"]
        return filtered_df

    revenue_df = filter_data(revenue_data, owner_filter, product_filter, quarter_filter)
    acquisition_df = filter_data(acquisition_data, owner_filter, product_filter, quarter_filter)

    # Calculate totals (using filtered data for KPIs)
    net_revenue_total = revenue_df[revenue_df["Metric"] == "Net Revenue"]["Achieved"].sum()
    gross_revenue_total = revenue_df[revenue_df["Metric"] == "Gross Revenue"]["Achieved"].sum()
    gross_adds_total = acquisition_df[acquisition_df["Metric"] == "Gross Adds"]["Achieved"].sum()
    net_adds_total = acquisition_df[acquisition_df["Metric"] == "Net Adds"]["Achieved"].sum()
    free_trial_total = acquisition_df[acquisition_df["Metric"] == "Free Trial"]["Achieved"].sum()

    net_revenue_target = revenue_df[revenue_df["Metric"] == "Net Revenue"]["Target"].sum()
    gross_revenue_target = revenue_df[revenue_df["Metric"] == "Gross Revenue"]["Target"].sum()
    gross_adds_target = acquisition_df[acquisition_df["Metric"] == "Gross Adds"]["Target"].sum()
    net_adds_target = acquisition_df[acquisition_df["Metric"] == "Net Adds"]["Target"].sum()
    free_trial_target = acquisition_df[acquisition_df["Metric"] == "Free Trial"]["Target"].sum()

    net_revenue_pct = (net_revenue_total / net_revenue_target * 100) if net_revenue_target else 0
    gross_revenue_pct = (gross_revenue_total / gross_revenue_target * 100) if gross_revenue_target else 0
    gross_adds_pct = (gross_adds_total / gross_adds_target * 100) if gross_adds_target else 0
    net_adds_pct = (net_adds_total / net_adds_target * 100) if net_adds_target else 0
    free_trial_pct = (free_trial_total / free_trial_target * 100) if free_trial_target else 0

    # Display totals with styled boxes
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(
            f"""
            <div style="background-color: #00008B; padding: 5px; border-radius: 5px; margin-bottom: 10px; font-style: italic; text-align: center;">
                <h3 style="margin: 0;">Net Revenue</h3>
                <p style="font-size: 30px; margin: 5px 0;">KES{net_revenue_total:,.0f}</p>
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
                <p style="font-size: 30px; margin: 5px 0;">KES{gross_revenue_total:,.0f}</p>
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
    with col5:
        st.markdown(
            f"""
            <div style="background-color: #00008B; padding: 5px; border-radius: 5px; margin-bottom: 10px; font-style: italic; text-align: center;">
                <h3 style="margin: 0;">Free Trials</h3>
                <p style="font-size: 30px; margin: 5px 0;">{free_trial_total:,.0f}</p>
                <p style="margin: 0;">{free_trial_pct:.0f}% of target</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Revenue Performance
    st.subheader("Revenue Performance")
    revenue_df_display = revenue_df[["Quarter", "Owner", "Product", "Metric", "Target", "Achieved", "% of Target"]].copy()
    st.table(revenue_df_display.style.format({
        "Target": "KES{:,.0f}",
        "Achieved": "KES{:,.0f}",
        "% of Target": "{:.0f}%"
    }))

    # Acquisition Metrics
    st.subheader("Acquisition Metrics")
    acquisition_df_display = acquisition_df[["Quarter", "Owner", "Product", "Metric", "Target", "Achieved", "% of Target"]].copy()
    st.table(acquisition_df_display.style.format({
        "Target": "{:,.0f}",
        "Achieved": "{:,.0f}",
        "% of Target": "{:.0f}%"
    }))

    # Quarterly Trends for Revenue Performance (using unfiltered data)
    if quarter_filter != "YTD":
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        revenue_df_all = revenue_data[revenue_data["Quarter"].isin(quarters)].copy()

        # Pivot data to aggregate by quarter
        gross_revenue_pivot = revenue_df_all[revenue_df_all["Metric"] == "Gross Revenue"].pivot_table(
            index="Quarter", values=["Target", "Achieved"], aggfunc="sum", fill_value=0
        )
        net_revenue_pivot = revenue_df_all[revenue_df_all["Metric"] == "Net Revenue"].pivot_table(
            index="Quarter", values=["Target", "Achieved"], aggfunc="sum", fill_value=0
        )

        # Gross Revenue Comparison Bar Chart
        st.subheader("Gross Revenue Trends")
        gross_target = gross_revenue_pivot["Target"].reindex(quarters, fill_value=0)
        gross_achieved = gross_revenue_pivot["Achieved"].reindex(quarters, fill_value=0)
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
        net_target = net_revenue_pivot["Target"].reindex(quarters, fill_value=0)
        net_achieved = net_revenue_pivot["Achieved"].reindex(quarters, fill_value=0)
        forecast_net = net_target * 1.05
        chart_data = pd.DataFrame({
            "Quarter": quarters * 3,
            "Value": list(net_target) + list(net_achieved) + list(forecast_net),
            "Type": ["Target"] * 4 + ["Achieved"] * 4 + ["Forecast"] * 4
        })
        fig = px.bar(chart_data, x="Quarter", y="Value", color="Type", barmode="group", title="Net Revenue Trends",
                     color_discrete_map={"Target": "red", "Achieved": "green", "Forecast": "yellow"})
        st.plotly_chart(fig)

    # Quarterly Trends for Acquisition Metrics (using unfiltered data)
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
        free_trial_pivot = acquisition_df_all[acquisition_df_all["Metric"] == "Free Trial"].pivot_table(
            index="Quarter", values=["Target", "Achieved"], aggfunc="sum", fill_value=0
        )

        # Gross Adds Comparison Bar Chart
        st.subheader("Gross Adds Trends")
        gross_adds_target = gross_adds_pivot["Target"].reindex(quarters, fill_value=0)
        gross_adds_achieved = gross_adds_pivot["Achieved"].reindex(quarters, fill_value=0)
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
        net_adds_target = net_adds_pivot["Target"].reindex(quarters, fill_value=0)
        net_adds_achieved = net_adds_pivot["Achieved"].reindex(quarters, fill_value=0)
        forecast_net_adds = net_adds_target * 1.05
        chart_data = pd.DataFrame({
            "Quarter": quarters * 3,
            "Value": list(net_adds_target) + list(net_adds_achieved) + list(forecast_net_adds),
            "Type": ["Target"] * 4 + ["Achieved"] * 4 + ["Forecast"] * 4
        })
        fig = px.bar(chart_data, x="Quarter", y="Value", color="Type", barmode="group", title="Net Adds Trends",
                     color_discrete_map={"Target": "red", "Achieved": "green", "Forecast": "yellow"})
        st.plotly_chart(fig)

        # Free Trial Comparison Bar Chart
        if free_trial_pivot["Target"].sum() > 0 or free_trial_pivot["Achieved"].sum() > 0:
            st.subheader("Free Trial Trends")
            free_trial_target = free_trial_pivot["Target"].reindex(quarters, fill_value=0)
            free_trial_achieved = free_trial_pivot["Achieved"].reindex(quarters, fill_value=0)
            forecast_free_trial = free_trial_target * 1.1
            chart_data = pd.DataFrame({
                "Quarter": quarters * 3,
                "Value": list(free_trial_target) + list(free_trial_achieved) + list(forecast_free_trial),
                "Type": ["Target"] * 4 + ["Achieved"] * 4 + ["Forecast"] * 4
            })
            fig = px.bar(chart_data, x="Quarter", y="Value", color="Type", barmode="group", title="Free Trial Trends",
                         color_discrete_map={"Target": "red", "Achieved": "green", "Forecast": "yellow"})
            st.plotly_chart(fig)
        else:
            st.write("No Free Trial data available for visualization.")

    # Cumulative Performance
    if quarter_filter == "YTD":
        st.subheader("Cumulative Performance (Revenue)")
        ytd_df = revenue_df[["Quarter", "Owner", "Product", "Metric", "Target", "Achieved", "% of Target"]].rename(columns={
            "Target": "Annual Target",
            "Achieved": "YTD Achieved",
            "% of Target": "% of Annual"
        })
        st.table(ytd_df.style.format({
            "Annual Target": "KES{:,.0f}",
            "YTD Achieved": "KES{:,.0f}",
            "% of Annual": "{:.0f}%"
        }))

        st.subheader("Cumulative Performance (Acquisition)")
        ytd_acq_df = acquisition_df[["Quarter", "Owner", "Product", "Metric", "Target", "Achieved", "% of Target"]].rename(columns={
            "Target": "Annual Target",
            "Achieved": "YTD Achieved",
            "% of Target": "% of Annual"
        })
        st.table(ytd_acq_df.style.format({
            "Annual Target": "{:,.0f}",
            "YTD Achieved": "{:,.0f}",
            "% of Annual": "{:.0f}%"
        }))

except Exception as e:
    st.error(f"Error fetching data: {str(e)}")
    st.write("Please ensure the 'busbuddy.xlsx' file is in the project directory with 'Revenue' and 'Acquisition' sheets. Verify that the sheets contain columns: 'Quarter', 'Owner', 'Product', 'Metric', 'Target', and 'Achieved'. Ensure values in 'Target' and 'Achieved' are numeric or formatted as text with 'KES' and commas (e.g., 'KES1,000').")