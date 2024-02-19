import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Disable PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Set Streamlit page configuration
st.set_page_config(
    page_title="Vanguard Client Engagement Report",
    page_icon=":bar_chart:",
    layout="centered",  # Centers the content on the page
    initial_sidebar_state="expanded",  # Show the sidebar by default
)

# Set custom theme and chart colors
st.markdown(
    """
    <style>
        /* Custom Streamlit theme */
        .streamlit-container {
            background-color: #46464a; /* Main background color */
            color: #ffffff; /* Text color */
        }
        .sidebar .sidebar-content {
            background-color: #46464a; /* Sidebar background color */
        }
        /* Change color of Matplotlib plots */
        .stPlotlyChart, .stVegaLiteChart, .stAltairChart, .stBokehChart, .stMatplotlibChart {
            color: #808080; /* Grey color for plots */
        }
    </style>
    """,
    unsafe_allow_html=True
)

def load_data(file_path):
    return pd.read_csv(file_path)

def demographic_analysis(df):
    st.header("Demographic Analysis")
    age_max = df["clnt_age"].max()
    age_min = df["clnt_age"].min()
    age_avg = df["clnt_age"].mean()
    st.write(f"Our oldest customer is {age_max:.0f} years old")
    st.write(f"Our youngest customer is {age_min:.0f} years old")
    st.write(f"The average age of our customers is {age_avg:.0f} years old")

def process_step_analysis(df):
    st.header("Process Step Analysis")
    process_step_counts = df['process_step'].value_counts()
    st.write("Process Step Counts:")
    st.write(process_step_counts)

def hypothesis_testing(df):
    st.header("Hypothesis Testing")
    control_process_steps = df[df['Variation'] == 'Control']['process_step'].str.extract('(\d+)', expand=False).fillna(-1).astype(float)
    test_process_steps = df[df['Variation'] == 'Test']['process_step'].str.extract('(\d+)', expand=False).fillna(-1).astype(float)
    t_stat, p_value = ttest_ind(control_process_steps, test_process_steps)
    st.write(f"T-statistic: {t_stat}")
    st.write(f"P-value: {p_value}")

def visualize_data(df, column, variation):
    st.header("Visualize Data")
    if column == "Age Distribution":
        st.subheader("Age Distribution")
        fig, ax = plt.subplots(figsize=(8, 6))
        df["clnt_age"].hist(ax=ax, color='grey', bins=30)  # Setting plot color to grey
        ax.set_title('Age Distribution', fontsize=18)
        ax.set_xlabel('Age', fontsize=14)
        ax.set_ylabel('Frequency', fontsize=14)
        st.pyplot(fig)

    elif column == "Process Step Completion Rates":
        st.subheader("Process Step Completion Rates")
        fig, ax = plt.subplots(figsize=(10, 6))
        control_completion_rate = df[df['Variation'] == variation]['process_step'].value_counts(normalize=True)
        control_completion_rate.plot(kind='bar', color='grey', alpha=0.7, label='Control', ax=ax)  # Setting plot color to grey
        ax.set_title('Process Step Completion Rates', fontsize=18)
        ax.set_xlabel('Process Step', fontsize=14)
        ax.set_ylabel('Completion Rate', fontsize=14)
        ax.legend()
        st.pyplot(fig)

def main():
    # Load data
    file_path = 'All_data.csv'
    df = load_data(file_path)

    st.title("Vanguard Client Engagement Report")

    # Sidebar - User Input
    st.sidebar.image('Vanguard.png', width=270)  # Insert the image as a logo on the sidebar header
    st.sidebar.header("Select to visualize:")
    analysis_option = st.sidebar.selectbox("Choose Analysis:", ["Demographic Analysis", "Process Step Analysis", "Hypothesis Testing"])
    if analysis_option == "Process Step Analysis" or analysis_option == "Hypothesis Testing":
        variation = st.sidebar.selectbox("Choose Variation:", df['Variation'].unique())

    # Perform Analysis
    if analysis_option == "Demographic Analysis":
        demographic_analysis(df)

    elif analysis_option == "Process Step Analysis":
        process_step_analysis(df)

    elif analysis_option == "Hypothesis Testing":
        hypothesis_testing(df)

    # Visualizations
    if analysis_option == "Process Step Analysis" or analysis_option == "Hypothesis Testing":
        column = st.selectbox("Choose Visualization:", ["Age Distribution", "Process Step Completion Rates"])
        visualize_data(df, column, variation)

if __name__ == "__main__":
    main()
