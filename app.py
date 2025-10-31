import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# 1️ Cargar el archivo CSV con los datos
# ----------------------------------------------------------
df = pd.read_csv("university_student_data.csv")

st.set_page_config(page_title="University Dashboard", layout="wide")

st.title("🎓 University Student Dashboard")
st.markdown("Panel interactivo con datos de retención, satisfacción y matrículas.")

# ----------------------------------------------------------
# 2️ Filtros interactivos
# ----------------------------------------------------------
years = st.multiselect(
    "Selecciona Año(s):",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

terms = st.multiselect(
    "Selecciona Semestre(s):",
    options=df["Term"].unique(),
    default=df["Term"].unique()
)

# Filtrar datos según los filtros seleccionados
filtered_df = df[(df["Year"].isin(years)) & (df["Term"].isin(terms))]

# ----------------------------------------------------------
# 3️ Indicadores principales (KPI)
# ----------------------------------------------------------
avg_retention = filtered_df["Retention Rate (%)"].mean()
avg_satisfaction = filtered_df["Student Satisfaction (%)"].mean()
total_enrolled = filtered_df["Enrolled"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("📊 Promedio Retención (%)", f"{avg_retention:.2f}")
col2.metric("😊 Promedio Satisfacción (%)", f"{avg_satisfaction:.2f}")
col3.metric("🎓 Total Matrículas", f"{int(total_enrolled)}")

# ----------------------------------------------------------
# 4️ Gráfico 1 - Línea: Tendencia de Retención por Año
# ----------------------------------------------------------
st.subheader("📈 Tendencia de la Tasa de Retención por Año")

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
ax1.set_title("Tendencia de Retención a lo largo del tiempo")
st.pyplot(fig1)

# ----------------------------------------------------------
# 5️ Gráfico 2 - Barras: Satisfacción por Año
# ----------------------------------------------------------
st.subheader("🏫 Puntuaciones de Satisfacción Estudiantil por Año")

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
ax2.set_title("Satisfacción Promedio por Año")
st.pyplot(fig2)

# ----------------------------------------------------------
# 6️Gráfico 3 - Circular: Distribución de Matrículas por Departamento
# ----------------------------------------------------------
st.subheader(" Distribución de Matrículas por Departamento")

dept_cols = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
dept_totals = filtered_df[dept_cols].sum().reset_index()
dept_totals.columns = ["Departamento", "Estudiantes Matriculados"]

fig3, ax3 = plt.subplots()
ax3.pie(
    dept_totals["Estudiantes Matriculados"],
    labels=dept_totals["Departamento"],
    autopct="%1.1f%%",
    startangle=90
)
ax3.set_title("Porcentaje de Matrículas por Departamento")
st.pyplot(fig3)

# ----------------------------------------------------------
# Fin del dashboard
# ----------------------------------------------------------
st.success("Dashboard generado correctamente.")
