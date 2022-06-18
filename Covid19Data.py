
import pandas as pd
import numpy as np
import plotly.express as px

# Get data
Covid_Tan = pd.read_csv("Covid_Tan.csv", parse_dates = ["StatisticsProfileDate"])
age_group = Covid_Tan.Age.unique()

# Create one new dataset for graphing the Percentage of Total Hospitalised Cases per Total Confirmed Cases by Age
Covid_Tan_max = Covid_Tan[Covid_Tan.StatisticsProfileDate == Covid_Tan.StatisticsProfileDate.max()].copy()
Covid_Tan_max["HospitalisedPercentagePerCase"] = Covid_Tan_max.HospitalisedCases * 100/Covid_Tan_max.Cases

# Create a new dataset to show the relationship between Hospitalised Cases Percentage and Confirmed Cases Percentage in all Age Group
Covid_Tan_max["Hospitalised"] = Covid_Tan_max.HospitalisedCases * 100/Covid_Tan_max.HospitalisedCovidCases
Covid_Tan_max["Confirmed Cases"] = Covid_Tan_max.Cases * 100/Covid_Tan_max.CovidCasesConfirmed

Covid_Tan_new = Covid_Tan_max.loc[:,["Age","Confirmed Cases","Hospitalised"]].copy()
Covid_Tan_new_melt = pd.melt(Covid_Tan_new, id_vars="Age",value_name="Percentage %",var_name="Type")

# Function 
def totalCovidConfirmCase(ages):
    mask = Covid_Tan.Age.isin(ages)
    fig = px.line(Covid_Tan[mask], 
        x="StatisticsProfileDate", y="Cases", color = "Age", title= "Total Confirmed Cases By Date",
        labels={"StatisticsProfileDate": "Statistics Date",  "Cases": "Total Confirmed Cases", "Age": "Age Group"}
             )
    fig.update_layout(title_font_color="#800000", title_x=0.5)
    return fig
    
def medianAge():
    fig = px.line(Covid_Tan.head(660), x="StatisticsProfileDate", y = "Median_Age", title= "Median Age of Total Confirmed Cases By Date ",
    labels={"StatisticsProfileDate": "Statistics Date",  "Median_Age": "Median Age"}
            )
    fig.update_layout(title_font_color="#800000", title_x=0.5) 
    return fig

def dailyCasebyAge(ages):
    mask = Covid_Tan.Age.isin(ages)
    fig = px.line(Covid_Tan[mask], x="StatisticsProfileDate", y = "CaseByDay", color = "Age" , 
    title= "Daily Confirmed Cases",
    labels={"StatisticsProfileDate": "Statistics Date",  "CaseByDay": "Confirmed Cases", "Age": "Age Group"}
             )
    fig.update_layout(title_font_color="#800000", title_x=0.5)
    return fig

def dailyHospitalbyAge(ages):
    mask = Covid_Tan.Age.isin(ages)
    fig = px.line(Covid_Tan[mask], x="StatisticsProfileDate", y = "HospitalCaseByDay", color = "Age", 
    title= "Daily Hospitalised Cases",
    labels={"StatisticsProfileDate": "Statistics Date",  "HospitalCaseByDay": "Hospitalised Cases", "Age": "Age Group"}
             )
    fig.update_layout(title_font_color="#800000", title_x=0.5)
    return fig

def pctHospitalPerCase(ages):
    mask = Covid_Tan_max.Age.isin(ages)
    fig = px.bar(Covid_Tan_max[mask], x="HospitalisedPercentagePerCase", y = "Age", title= "Percentage of Total Hospitalised Cases per Total Confirmed Cases",
    labels={"HospitalisedPercentagePerCase": "Percentage of Hospitalised Cases", "Age": "Age Group"}
             )
    fig.update_layout(title_font_color="#800000", title_x=0.5)
    return fig
    
def relationHospitalCase(ages):
    mask = Covid_Tan_new_melt.Age.isin(ages)
    fig = px.bar(Covid_Tan_new_melt[mask], x="Percentage %", y = "Age", color = "Type", barmode = "group", 
    title= "Percentage of Hospitalised Cases and Confirmed Cases by Age Groups",
    labels={"Type": "", "Age": "Age Group"}
             )
    fig.update_layout(title_font_color="#800000", title_x=0.5)
    return fig
