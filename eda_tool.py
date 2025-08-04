import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# הגדרה קטנה למניעת הודעת אזהרה נפוצה
#st.set_option('deprecation.showPyplotGlobalUse', False)

def show_file_description(df_desc):
    """מציגה תיאור כללי של הקובץ."""
    row, col = df_desc.shape
    st.write(f"Rows in file: {row}, Columns in file: {col}")
    st.write("**Columns Data Types:**")
    st.dataframe(df_desc.dtypes.to_frame('Data Type'))
    
    #st.write("**Pair Plot:**")
    #st.info("Note: If you uploaded a large file, this might take a while")
    #fig = sns.pairplot(df_desc)
    #st.pyplot(fig)

def show_bivariate(df, numeric_list, all_list):
    """מציגה ניתוח קשרים בין שתי עמודות."""
    col1 = st.selectbox("Select a numeric column (X-axis):", options=numeric_list, key='bivar_col1')
    col2 = st.selectbox("Select a second column (Y-axis or category):", options=all_list, key='bivar_col2')

    if col1 and col2:
        if col2 in numeric_list:
            st.write(f"**Scatter Plot: {col1} vs {col2}**")
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=col1, y=col2, ax=ax)
            st.pyplot(fig)
        else:
            st.write(f"**Box Plot: {col1} by {col2}**")
            st.dataframe(df.groupby(col2)[col1].describe())
            fig, ax = plt.subplots()
            sns.boxplot(x=col2, y=col1, data=df, ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

def show_single_variable_analysis(df, all_list, numeric_list):
    """מציגה ניתוח עבור עמודה בודדת."""
    col_selected = st.selectbox("Select a column to analyze:", options=all_list, key='univar_col')

    if col_selected:
        if col_selected in numeric_list:
            st.write(f"**Analysis of Numeric Column: {col_selected}**")
            st.dataframe(df[col_selected].describe())
            
            st.write("**Distribution:**")
            fig, ax = plt.subplots()
            sns.histplot(data=df, x=col_selected, kde=True, ax=ax)
            st.pyplot(fig)

            numeric_df = df.select_dtypes(include=np.number)
            if numeric_df.shape[1] > 1:
                st.write(f"**Correlation with other numeric columns:**")
                corr_matrix = numeric_df.corr()
                fig, ax = plt.subplots()
                sns.barplot(x=corr_matrix[col_selected].values, y=corr_matrix[col_selected].index, ax=ax)
                st.pyplot(fig)
        else:
            st.write(f"**Analysis of Categorical Column: {col_selected}**")
            st.dataframe(df[col_selected].value_counts())
            
            st.write("**Distribution:**")
            fig, ax = plt.subplots()
            sns.countplot(data=df, y=col_selected, ax=ax)
            st.pyplot(fig)


st.title("Exploratory Data Analysis (EDA) Tool")

uploaded_file = st.file_uploader("Upload your CSV file")

if uploaded_file is not None:
    #בדיקה שזה קובץ csv
    if uploaded_file.name[-4:]=='.csv':
        try:
            df_original = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {e}")
        #בדיקה שיש רשומות
        if not df_original.empty:
            #show_file_description(df)
            with st.form(key='cleaning_form'):
                cleaning_options = [
                                    "Do not clean missing values",
                                    "Remove rows that are completely empty",
                                    "Remove any row with a missing value"
                                    ]
                old_row, old_col = df_original.shape
                st.write(f"Rows in file: {old_row}, Columns in file: {old_col}")
                cleaning_selection = st.radio("Select cleaning option:", cleaning_options)
                submitted = st.form_submit_button("plese choose")  
                if submitted:
                    if cleaning_selection == cleaning_options[0]: # אין צורך לעשות כלום
                        df_cleaned = df_original 
                    elif cleaning_selection == cleaning_options[1]: # מחיקת שורות שהן ריקות לגמרי
                        df_cleaned = df_original.dropna(how='all')
                    elif cleaning_selection == cleaning_options[2]: # מחיקת שורות שיש בהן עמודות ריקות
                        df_cleaned = df_original.dropna(how='any')

                    new_row, new_col = df_cleaned.shape
                    deleted_rows=old_row-new_row
                    st.success(f"**Deletd: {deleted_rows}** rows")
                    st.session_state['cleaned_df'] = df_cleaned

            if 'cleaned_df' in st.session_state:
                df = st.session_state['cleaned_df']
            else:
                df = df_original

            # חישוב רשימות העמודות המספריות והקטגוריאליות
            numeric_list = df.select_dtypes(include=np.number).columns.tolist() 
            categorical_list = [c for c in df.select_dtypes(exclude=np.number).columns if (df[c].nunique() <= 8)]
            # יצירת רשימה מאוחדת
            all_list = df.columns.tolist()

            # התפריט הראשי
            menu = [
                    'File General Description', 
                    'Single Column Analysis', 
                    'Bivariate Analysis'
                    ]
            
            st.sidebar.title("Navigation Menu")
            selection = st.sidebar.radio("Select:", menu)

            # הבחירה של המשתמש בתפריט
            if selection == menu[0]: #תיאור כללי של הקובץ
                st.header("General File Description")
                show_file_description(df)
            elif selection == menu[1]: # חישוב לעמודה בודדת
                st.header("Single Column Analysis (Univariate)")
                show_single_variable_analysis(df, all_list, numeric_list)
            else: # חישוב לשתי עמודות
                st.header("Bivariate Analysis")
                show_bivariate(df, numeric_list, all_list)
        else:
            st.error('The file has now data')
    else:
        st.error('please choose a csv file')