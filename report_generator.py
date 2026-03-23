import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet


# Setup
os.makedirs("charts", exist_ok=True)

# Load data
df = pd.read_csv("C:\Data Analyst\Swiss_Projects\Swiss_Tourism_Trend_Analysis\Data\Cleaned_tourism_data_2019-2023.csv")

# Chart 1: Total Tourism Trend
yearly = df.groupby("Year")[["Swiss", "Foreigners", "Total"]].sum().reset_index()

plt.figure()
sns.lineplot(data=yearly, x="Year", y="Total", marker="o")
plt.title("Total Tourism Trend (2019–2023)")
plt.savefig("Charts/total_trend.png")
plt.close()

# Chart 2: Swiss vs Foreign
plt.figure()
sns.barplot(data=yearly.melt(id_vars="Year"), x="Year", y="value", hue="variable")
plt.title("Swiss vs Foreign Tourists")
plt.savefig("Charts/swiss_vs_foreign.png")
plt.close()

# Chart 3: Top 5 Regions (2023)
top5 = df[df["Year"] == 2023].sort_values(by="Total", ascending=False).head(5)

plt.figure()
sns.barplot(data=top5, x="Total", y="Region")
plt.title("Top 5 Regions (2023)")
plt.savefig("Charts/top5.png")
plt.close()

# PDF REPORT GENERATION
doc = SimpleDocTemplate("Swiss_Tourism_Report.pdf")
styles = getSampleStyleSheet()

content = []

# Title
content.append(Paragraph("Swiss Tourism Analysis Report (2019–2023)", styles["Title"]))
content.append(Spacer(1, 20))

# Overview
content.append(Paragraph(
    "This report presents an analysis of Swiss tourism trends using official government data. "
    "The objective is to understand tourism patterns, COVID impact, and regional performance.",
    styles["BodyText"]
))
content.append(Spacer(1, 20))

# Key Insights
content.append(Paragraph("Key Insights:", styles["Heading2"]))
content.append(Spacer(1, 10))

insights = [
    "Tourism dropped significantly in 2020 due to COVID-19.",
    "Swiss domestic tourism remained relatively stable during pandemic years.",
    "Foreign tourism recovered strongly in 2022 and 2023.",
    "Zurich, Bern, and Lucerne are the top-performing regions.",
    "Urban regions showed higher volatility compared to mountain regions."
]

for point in insights:
    content.append(Paragraph(f"- {point}", styles["BodyText"]))
    content.append(Spacer(1, 5))

content.append(Spacer(1, 20))

# Add Charts
content.append(Paragraph("Total Tourism Trend", styles["Heading2"]))
content.append(Image("Charts/total_trend.png", width=400, height=250))
content.append(Spacer(1, 20))

content.append(Paragraph("Swiss vs Foreign Tourists", styles["Heading2"]))
content.append(Image("Charts/swiss_vs_foreign.png", width=400, height=250))
content.append(Spacer(1, 20))

content.append(Paragraph("Top 5 Regions (2023)", styles["Heading2"]))
content.append(Image("Charts/top5.png", width=400, height=250))

content.append(Paragraph("Region-wise Tourism Distribution", styles["Heading2"]))
content.append(Image("Charts/region_year_stacked_bar.png", width=400, height=250))
content.append(Spacer(1, 20))

content.append(Paragraph("Zurich vs Geneva vs Bern Trend", styles["Heading2"]))
content.append(Image("Charts/zurich_geneva_bern_trend.png", width=400, height=250))
content.append(Spacer(1, 20))

# Build PDF
doc.build(content)

print("✅ PDF Report Generated: Swiss_Tourism_Report.pdf")