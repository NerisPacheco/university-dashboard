import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="University Student Dashboard", layout="wide")

# Header and Team Info
st.title("University Student Dashboard")
st.markdown("""
This interactive dashboard displays key metrics such as retention rate, satisfaction, 
and enrollments across different years, semesters, and departments.
""")

st.markdown("""
**Developed by:**  
**Elis García Morales** and **Neris Pacheco Orozco**  
Students of Systems Engineering in the *Data Mining* subject — Universidad de la Costa
""")

# Data Loading and Preparation
df = pd.read_csv("university_student_data.csv")
df["Term"] = df["Term"].replace({"Spring": "Semester 1", "Fall": "Semester 2"})

# Interactive Filters (all selected by default, "omit" style)
years = st.multiselect(
    "Select the Year(s) you want to omit:",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

terms = st.multiselect(
    "Select the Semester(s) you want to omit:",
    options=df["Term"].unique(),
    default=df["Term"].unique()
)

departments = st.multiselect(
    "Select the Department(s) you want to omit:",
    options=["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"],
    default=["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
)

# Data Filtering: include only items NOT selected
filtered_df = df[~df["Year"].isin(years) & ~df["Term"].isin(terms)]
if departments:
    dept_columns = [col for col in departments if col in df.columns]
else:
    dept_columns = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]

# KPI Metrics
avg_retention = filtered_df["Retention Rate (%)"].mean()
avg_satisfaction = filtered_df["Student Satisfaction (%)"].mean()
total_enrolled = filtered_df["Enrolled"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Average Retention Rate (%)", f"{avg_retention:.2f}")
col2.metric("Average Student Satisfaction (%)", f"{avg_satisfaction:.2f}")
col3.metric("Total Enrollments", f"{int(total_enrolled)}")

# Visualization 1 - Retention Trend
st.subheader("Retention Rate Trend Over Time")
retention_by_year = filtered_df.groupby("Year")["Retention Rate (%)"].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.lineplot(
    data=retention_by_year,
    x="Year",
    y="Retention Rate (%)",
    marker="o",
    color="steelblue",
    ax=ax1
)
ax1.set_title("Retention Rate Trend Over Time")
ax1.set_ylabel("Retention Rate (%)")
st.pyplot(fig1)

# Visualization 2 - Satisfaction by Year
st.subheader("Average Student Satisfaction per Year")
satisfaction_by_year = filtered_df.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(
    data=satisfaction_by_year,
    x="Year",
    y="Student Satisfaction (%)",
    hue="Year",
    palette="viridis",
    legend=False,
    ax=ax2
)
ax2.set_title("Average Student Satisfaction per Year")
ax2.set_ylabel("Satisfaction (%)")
st.pyplot(fig2)

# Visualization 3 - Enrollment by Department
st.subheader("Enrollment Distribution by Department")
dept_totals = filtered_df[dept_columns].sum().reset_index()
dept_totals.columns = ["Department", "Enrolled Students"]

fig3, ax3 = plt.subplots()
ax3.pie(
    dept_totals["Enrolled Students"],
    labels=dept_totals["Department"],
    autopct="%1.1f%%",
    startangle=90
)
ax3.set_title("Enrollment Share by Department")
st.pyplot(fig3)

# Footer
st.caption("© 2025 Universidad de la Costa — Data Mining Project | Developed for academic purposes only.")

