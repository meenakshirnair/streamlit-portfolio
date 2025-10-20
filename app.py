
import streamlit as st
import pandas as pd
import plotly.express as px
import yaml
from pathlib import Path

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Meenakshi | Business Analytics Portfolio",
    page_icon="📊",
    layout="wide"
)

# ----------------------------
# Helper functions
# ----------------------------
def load_projects(path: Path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    return []

def kpi_card(label, value, subtext=""):
    c = st.container(border=True)
    c.markdown(f"**{label}**")
    c.markdown(f"<h2 style='margin:0'>{value}</h2>", unsafe_allow_html=True)
    if subtext:
        c.caption(subtext)

def project_card(p):
    col = st.container(border=True)
    title = p.get("title","Untitled Project")
    desc = p.get("description","")
    tags = p.get("tags", [])
    links = p.get("links", {})
    image = p.get("image", "")
    cols = st.columns([1,2])
    with cols[0]:
        if image and Path(image).exists():
            st.image(image, use_container_width=True)
        else:
            st.image("placeholder.png", use_container_width=True)
    with cols[1]:
        st.subheader(title)
        st.write(desc)
        if tags:
            st.write("**Tags:** " + " · ".join(tags))
        link_line = []
        if "github" in links:
            link_line.append(f"[GitHub]({links['github']})")
        if "demo" in links:
            link_line.append(f"[Demo]({links['demo']})")
        if "report" in links:
            link_line.append(f"[Report]({links['report']})")
        if link_line:
            st.write(" | ".join(link_line))

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("📁 Portfolio")
page = st.sidebar.radio("Navigate", ["Home","Projects","Visual Gallery","Contact"])

# ----------------------------
# Data
# ----------------------------
projects = load_projects(Path("projects.yaml"))

# ----------------------------
# Pages
# ----------------------------
if page == "Home":
    st.title("Business Analytics in Action")
    st.write(
        "Hi, I'm **Meenakshi Rajeev Nair** — a Business Analytics graduate student at ASU with prior experience at EY. "
        "I build practical analytics, optimization, and automation solutions that turn data into decisions."
    )

    st.markdown("---")
    st.markdown("### Key Results (selected)")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Employee Attrition Model", "91.9% acc.", "AUC 0.97")
    with c2: kpi_card("Workflow Automation", "25% ↓ time", "EY client operations")
    with c3: kpi_card("AI Routing Optimization", "100% SLA", "Cost-minimizing LP")
    with c4: kpi_card("Rent Forecasting", "81% R²", "Polynomial regression")

    st.markdown("---")
    st.markdown("### Recent Work")
    if projects:
        cols = st.columns(2)
        for i, p in enumerate(projects[:4]):
            with cols[i % 2]:
                project_card(p)
    else:
        st.info("Add your projects in `projects.yaml` to feature them here.")

elif page == "Projects":
    st.title("Projects")
    st.caption("Curated analytics projects with a focus on measurable business outcomes.")
    if not projects:
        st.warning("No projects found. Add them in `projects.yaml`.")
    else:
        for p in projects:
            project_card(p)

elif page == "Visual Gallery":
    st.title("Visual Gallery")
    st.caption("A few quick visuals to showcase analytics storytelling.")
    # Demo chart 1: Feature importance bar
    st.subheader("Top Features Impacting Attrition (demo)")
    df = pd.DataFrame({
        "feature": ["JobInvolvement", "JobLevel", "WorkLifeBalance", "StockOptionLevel", "MonthlyIncome"],
        "importance": [0.28, 0.22, 0.18, 0.16, 0.12]
    })
    fig = px.bar(df, x="importance", y="feature", orientation="h")
    st.plotly_chart(fig, use_container_width=True)

    # Demo chart 2: Optimization cost curve
    st.subheader("Cost vs SLA Trade-off (demo)")
    df2 = pd.DataFrame({
        "SLA_compliance": [90, 92, 95, 97, 99, 100],
        "Cost_$": [100, 96, 92, 91, 90.5, 90.5]
    })
    fig2 = px.line(df2, x="SLA_compliance", y="Cost_$", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Contact":
    st.title("Contact")
    st.write("Let's connect!")
    st.write("**Email:** meenakshirnair712@gmail.com")
    st.write("**LinkedIn:** https://www.linkedin.com/in/meenakshi-rajeev-nair-43301b248")
    st.write("**GitHub:** https://github.com/meenakshirnair")
    st.markdown("---")
    with st.form("contact_form"):
        st.write("Send a quick message:")
        name = st.text_input("Name")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Thanks! You can also reach me directly by email.")
