# Tamil Nadu Healthcare Performance and Disease Surveillance Dashboard

An interactive Power BI dashboard that tracks disease surveillance and healthcare performance across districts and healthcare levels in Tamil Nadu.

## Project Overview

This project brings healthcare data into one place so that trends and performance can be seen quickly. The dashboard covers:

* Disease surveillance and positivity rates
* Hospital utilization (OPD and IPD admissions)
* Emergency bite cases
* Bed occupancy
* Hospital deaths
* Doctor attendance

All of these can be viewed by district, month, disease, and healthcare level.

## Tools Used

* Python (Pandas) for data cleaning and validation
* Excel for the source data
* Power BI for the data model and dashboard
* DAX for KPI calculations

## Data Cleaning (Python)

The raw healthcare data was cleaned with a Python script using Pandas, so the same steps can be run again on new data. The script:

* Removes duplicate records
* Standardizes category names so the same value is not written in different ways
* Checks and fixes inconsistent healthcare records

## Data Model (Power BI)

The model has a Date dimension and a Facility dimension connected to the main healthcare data. This makes it easy to filter and compare by time, district, and healthcare level.

## KPIs Created with DAX

* Positivity rate
* OPD and IPD admissions
* Bed occupancy
* Doctor attendance

## Interactive Features

* Slicers for district, month, disease, and healthcare level
* Visuals to find trends and compare healthcare performance between districts

## Data Source

The data used in this project is synthetic. It is not real patient or hospital data, so the numbers shown in the dashboard do not describe the actual healthcare situation in Tamil Nadu. The project is meant to show data cleaning, data modeling, and dashboard skills.

## Author

Dharshini R, Bioinformatics Postgraduate and Data Analyst
[LinkedIn](https://www.linkedin.com/in/dharshini-ramamoorthy-778636308) | [GitHub](https://github.com/Dharshini-0106)
