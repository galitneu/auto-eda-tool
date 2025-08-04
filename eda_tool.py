import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#מציגה תיאור כללי של הקובץ.
def show_file_description(df_desc):
    st.write("**File Description:**")
    st.write("This section provides a general overview of the uploaded file, including its size, number of rows and columns, and data types of each column.")
    st.write("**First 5 Rows of the File:**")
    st.write(df_desc.head(5))  # הצגת 5 שורות ראשונות של הקובץ
    row, col = df_desc.shape
    st.write(f"Rows in file: {row}, Columns in file: {col}") # הצגת מספר השורות והעמודות בקובץ
    df_size=df_desc.size
    df_nullcells = df_desc.isnull().sum().sum()
    nullcells_perc=(df_nullcells/df_size)*100
    st.write(f"Number of cells: {df_size} Number of empty cells: {df_nullcells} (which are {nullcells_perc:.2f}% of all cells)") # הצגת מספר התאים בקובץ, מספר התאים הריקים ואחוז התאים הריקים
    
    # הצגת סוגי הנתונים וערכים חסרים
    st.write("**Columns Data Types and Missing Values:**")
    summary_dict = {
    'Data Type': df_desc.dtypes,
    'Missing Values': df_desc.isnull().sum()
                    }
    st.dataframe(pd.DataFrame(summary_dict))

    st.write("**Missing Values Distribution:**")
    # מסננים כדי להציג רק עמודות שיש בהן ערכים חסרים
    missing_values = df_desc.isnull().sum()
    missing_values = missing_values[missing_values > 0]

    if not missing_values.empty:
        st.bar_chart(missing_values)
    
    
    #חישוב והצגת ערכים חריגים
    st.write("**Outliers Detection:**")
    numeric_list = df_desc.select_dtypes(include=np.number).columns.tolist()
    results = [] # רשימה ריקה לאיסוף התוצאות
    
    if not numeric_list:
        st.write("No numeric columns found for outlier detection.")
    else:
        for col_name in numeric_list:
            Q1, Q3 =  pd.Series(df_desc[col_name]).quantile([0.25, 0.75])
            ICQ = Q3 - Q1
            lower_bound = Q1 - 1.5 * ICQ
            upper_bound = Q3 + 1.5 * ICQ   
            outliers = df_desc[(df_desc[col_name] < lower_bound) | (df_desc[col_name] > upper_bound)] 
            #החזרת מספר השורות עם ערכים חריגיםה
            outlier_count = outliers.shape[0]
            #הוספת התוצאה לרשימה
            if outlier_count > 0:
                results.append({
                    'Column': col_name,
                    'Outlier Count': outlier_count,
                    'Lower Bound': lower_bound,
                    'Upper Bound': upper_bound
                })
        if not results:
            st.write("No outliers detected in numeric columns.")
        else:
            #הצגת התוצאות
            outlier_df = pd.DataFrame(results)
            st.dataframe(outlier_df)
            st.write("**Outliers Distribution:**")
            for col_name in outlier_df['Column']:
                st.write(f"**Box Plot for: {col_name}**")
                fig, ax = plt.subplots()
                sns.boxplot(data=df_desc, x=col_name, ax=ax)
                st.pyplot(fig)
        

    #st.write("**Pair Plot:**")
    #st.info("Note: If you uploaded a large file, this might take a while")
    #fig = sns.pairplot(df_desc)
    #st.pyplot(fig)

#מציגה ניתוח קשרים בין שתי עמודות.
def show_bivariate(df, numeric_list, all_list):
    
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

# מציגה ניתוח עבור עמודה בודדת
def show_single_variable_analysis(df, all_list, numeric_list):
    col_selected = st.selectbox("Select a column to analyze:", options=all_list, key='univar_col')

    if col_selected:
        #במקרה של עמודה מספרית
        if col_selected in numeric_list:
            st.write(f"**Analysis of Numeric Column: {col_selected}**")
            st.dataframe(df[col_selected].describe())
            
            st.write("**Distribution:**")
            fig, ax = plt.subplots()
            sns.histplot(data=df, x=col_selected, kde=True, ax=ax)
            st.pyplot(fig)

            #יצירת df רק של עמודות מספריות
            numeric_df = df.select_dtypes(include=np.number)
            if numeric_df.shape[1] > 1:
                st.write(f"**Correlation with other numeric columns:**")
                corr_matrix = numeric_df.corr()
                fig, ax = plt.subplots()
                #הצגת קורלציות רק של העמודה הנבחרת
                sns.barplot(x=corr_matrix[col_selected].values, y=corr_matrix[col_selected].index, ax=ax)
                st.pyplot(fig)
        else:
            #במקרה של עמודה קטגוריאלית
            st.write(f"**Analysis of Categorical Column: {col_selected}**")
            st.dataframe(df[col_selected].value_counts())
            
            st.write("**Distribution:**")
            fig, ax = plt.subplots()
            sns.countplot(data=df, y=col_selected, ax=ax)
            st.pyplot(fig)


#תוכנית ראשית
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
            
            if 'cleaned_df' not in st.session_state:

                    st.write("**File Overview:**")
                    #הרצת הפונקיציה להציג תיאור כללי של הקובץ
                    show_file_description(df_original)
                
                    
                    #בדיקה אם יש עמודות עם ערכים חסרים
                    missing_cols = df_original.columns[df_original.isnull().any()].tolist()
                    if missing_cols:
                        #הצגת אפשרויות ניקוי
                        with st.form(key='cleaning_form'):
                            cleaning_options = [
                                            "Do not clean missing values",
                                            "Remove rows that are completely empty",
                                            "Remove any row with a missing value"
                                            ]
                            #הצגת בחירה לגבי ניקוי הקובץ
                            cleaning_selection = st.radio("Select cleaning option:", cleaning_options)
                            submitted = st.form_submit_button("please choose")  
                            
                            if submitted:
                                old_row, old_col = df_original.shape
                                if cleaning_selection == cleaning_options[0]: # אין צורך לעשות כלום
                                    df_cleaned = df_original.copy() 
                                elif cleaning_selection == cleaning_options[1]: # מחיקת שורות שהן ריקות לגמרי
                                    df_cleaned = df_original.dropna(how='all')
                                elif cleaning_selection == cleaning_options[2]: # מחיקת שורות שיש בהן עמודות ריקות
                                    df_cleaned = df_original.dropna(how='any')

                                new_row, new_col = df_cleaned.shape
                                deleted_rows=old_row-new_row
                                st.success(f"**Deletd: {deleted_rows}** rows")
                                st.session_state['cleaned_df'] = df_cleaned
                                st.rerun()
                            

                    else:
                        st.write("No columns with missing values.")
                        st.session_state['cleaned_df'] = df_original
                        st.rerun()

            else:        
                df_to_analyze = st.session_state['cleaned_df']
                # חישוב רשימות העמודות המספריות והקטגוריאליות
                numeric_list = df_to_analyze.select_dtypes(include=np.number).columns.tolist() 
                categorical_list = [c for c in df_to_analyze.select_dtypes(exclude=np.number).columns if (df_to_analyze[c].nunique() <= 8)]
                # יצירת רשימה מאוחדת
                all_list = df_to_analyze.columns.tolist()


                # התפריט הראשי
                menu = [
                        'Guidelines and Instruction', 
                        'General Description', 
                        'Single Column Analysis', 
                        'Bivariate Analysis'
                        ]
                    
                st.sidebar.title("Navigation Menu")
                placeholder = st.empty()  # יצירת פלייסהולדר כדי למנוע רענון התוכן בעת בחירת תפריט  
                selection = st.sidebar.radio("Select:", menu)
                
                with placeholder.container():

                    # הבחירה של המשתמש בתפריט
                    if selection == menu[0]: #הוראות שימוש
                    
                        st.info("""
                        1. You've Uploaded a CSV file using the file uploader.
                        2. Select a column for single variable analysis or two columns for bivariate analysis.
                        3. Visualizations will be generated based on your selections.
                        """)
                        st.write("**Note:** If you uploaded a large file, some operations may take longer to complete.")

                    elif selection == menu[1]: #תיאור כללי של הקובץ
                    
                        st.header("General File Description")
                        show_file_description(df_to_analyze)
                    elif selection == menu[2]: # חישוב לעמודה בודדת
                    
                        st.header("Single Column Analysis (Univariate)")
                        show_single_variable_analysis(df_to_analyze, all_list, numeric_list)
                    else: # חישוב לשתי עמודות
                    
                        st.header("Bivariate Analysis")
                        show_bivariate(df_to_analyze, numeric_list, all_list)
                
        else:
            st.error('The file has no data')
    else:
        st.error('Please choose a csv file')

    
