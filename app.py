import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# 1️⃣ Load the dataset
# ----------------------------------------------------------
df = pd.read_csv("university_student_data.csv")

st.set_page_config(page_title="University Student Dashboard", layout="wide")

st.title("🎓 University Student Dashboard")
st.markdown("Interactive dashboard displaying key student metrics such as retention, satisfaction, and enrollments.")

# ----------------------------------------------------------
# 2️⃣ Interactive Filters
# ----------------------------------------------------------
years = st.multiselect(
    "Select Year(s):",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

terms = st.multiselect(
    "Select Term(s):",
    options=df["Term"].unique(),
    default=df["Term"].unique()
)

departments = st.multiselect(
    "Select Department(s):",
    options=["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"],
    default=["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
)

# Filter dataset based on year and term (department filter applies later)
filtered_df = df[(df["Year"].isin(years)) & (df["Term"].isin(terms))]

# ----------------------------------------------------------
# 3️⃣ KPI Cards
# ----------------------------------------------------------
avg_retention = filtered_df["Retention Rate (%)"].mean()
avg_satisfaction = filtered_df["Student Satisfaction (%)"].mean()
total_enrolled = filtered_df["Enrolled"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("📊 Average Retention Rate (%)", f"{avg_retention:.2f}")
col2.metric("😊 Average Student Satisfaction (%)", f"{avg_satisfaction:.2f}")
col3.metric("🎓 Total Enrollments", f"{int(total_enrolled)}")

# ----------------------------------------------------------
# 4️⃣ Chart 1 - Line Plot: Retention Trend Over Time
# ----------------------------------------------------------
st.subheader("📈 Retention Rate Trend Over Time")

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

# ----------------------------------------------------------
# 5️⃣ Chart 2 - Bar Chart: Average Satisfaction per Year
# ----------------------------------------------------------
st.subheader("🏫 Average Student Satisfaction per Year")

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

# ----------------------------------------------------------
# 6️⃣ Chart 3 - Pie Chart: Enrollment Distribution by Department
# ----------------------------------------------------------
st.subheader("🟢 Enrollment Distribution by Department")

# Apply department filter dynamically
dept_totals = filtered_df[departments].sum().reset_index()
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

# ----------------------------------------------------------
# ✅ End of Dashboard
# ----------------------------------------------------------
st.success("✅ Dashboard loaded successfully.")


