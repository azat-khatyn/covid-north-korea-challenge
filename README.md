### About this project

The goal is to estimate how many people are infected with COVID-19 in North Korea which doesn’t report its numbers. 
The only information provided regarding North Korea, is that its first case was on the 1st of March. It should be possible to make an estimation for any successive date. 

Data provided:  COVID-19 API, the World Bank API.
(https://github.com/azat-khatyn/covid-north-korea-challenge/blob/master/1_download_countries_data.ipynb
https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-country-api-queries)


### Solution

The approach chosen to tackle this problem is to first find most similar countries to North Korea and then make an estimation of the number of confirmed cases there by aggregating a value based on the numbers of cases fo the 'neighbors'.

To implement the solution, a k-nearest-Neighbors algorithm is used to find the countries, that would be 'closest' to North Korea based on the data provided. Once the list of 'neighbors' is generated, the according countries should be found in the dataset, providing information about the reported numbers on the Covid-infection. The data should be filted by the date of interest.
A mean of the "neighbors'" number of confirmed cases will be the final estimation for North Korea.

Next, Flask framework is used to implement a web application, taking in an integer representing the number of days since the 1st of Match and showing an estimated number of confirmed cases in North Korea for this date. 

The application was deployed on an AWS ic2 instance. 


### About this repository

This repository constits of following notebooks:


- 1_download_countries_data.ipynb
- 2_data_preprocessing.ipynb
- 3_find_knn.ipynb
- 4_download_covid_data.ipynb
- 4_5_countries_mapping.ipynb
- 5_explore_k_nearest_countries.ipynb (Web application)
- limitations.ipybn

The first six files correspond to the architecture of the workflow presented below. 
limitations.ipubn contains reflections on current as well as potential limitaions of this project.


![Architecture of the pipeline](architecture.png)