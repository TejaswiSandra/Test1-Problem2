import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("university_student_dashboard_data.csv")

# Load data
data = load_data()

# Set page title
st.title("University Student Dashboard")

# Sidebar for filters
st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", data['Year'].unique())
selected_term = st.sidebar.selectbox("Select Term", data['Term'].unique())

# Filter data based on selections
filtered_data = data[(data['Year'] == selected_year) & (data['Term'] == selected_term)]

# Display KPIs
st.header("Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Applications", filtered_data['Applications'].sum())
with col2:
    st.metric("Total Admissions", filtered_data['Admitted'].sum())
with col3:
    st.metric("Total Enrollments", filtered_data['Enrolled'].sum())

# Retention Rate Trends
st.header("Retention Rate Trends Over Time")
retention_data = data.groupby(['Year', 'Term'])['Retention Rate (%)'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=retention_data, x='Year', y='Retention Rate (%)', hue='Term', marker='o')
plt.title("Retention Rate Trends Over Time")
plt.xlabel("Year")
plt.ylabel("Retention Rate (%)")
st.pyplot(plt)

# Student Satisfaction Trends
st.header("Student Satisfaction Trends Over Time")
satisfaction_data = data.groupby(['Year', 'Term'])['Student Satisfaction (%)'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=satisfaction_data, x='Year', y='Student Satisfaction (%)', hue='Term', marker='o')
plt.title("Student Satisfaction Trends Over Time")
plt.xlabel("Year")
plt.ylabel("Student Satisfaction (%)")
st.pyplot(plt)

# Enrollment Breakdown by Department
st.header("Enrollment Breakdown by Department")
enrollment_data = filtered_data[['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].melt()
plt.figure(figsize=(10, 6))
sns.barplot(data=enrollment_data, x='variable', y='value')
plt.title("Enrollment Breakdown by Department")
plt.xlabel("Department")
plt.ylabel("Number of Students")
st.pyplot(plt)

# Comparison Between Spring and Fall Terms
st.header("Spring vs Fall Term Trends")
term_comparison = data.groupby('Term').agg({
    'Applications': 'mean',
    'Admitted': 'mean',
    'Enrolled': 'mean',
    'Retention Rate (%)': 'mean',
    'Student Satisfaction (%)': 'mean'
}).reset_index()
st.write(term_comparison)

# Department-wise Comparison
st.header("Department-wise Comparison")
department_data = data.groupby('Year').agg({
    'Engineering Enrolled': 'sum',
    'Business Enrolled': 'sum',
    'Arts Enrolled': 'sum',
    'Science Enrolled': 'sum'
}).reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=department_data.melt(id_vars='Year'), x='Year', y='value', hue='variable', marker='o')
plt.title("Department-wise Enrollment Trends Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Students")
st.pyplot(plt)

# Key Findings and Insights
st.header("Key Findings and Insights")
st.write("""
1. **Retention Rates**: Retention rates have shown a steady increase over the years, with Fall terms consistently performing slightly better than Spring terms.
2. **Student Satisfaction**: Student satisfaction scores have also improved, indicating a positive trend in student experience.
3. **Department Enrollment**: Engineering and Business departments have seen the highest enrollment, while Science and Arts have remained relatively stable.
4. **Spring vs Fall**: Fall terms generally have higher applications, admissions, and enrollments compared to Spring terms.
""")
