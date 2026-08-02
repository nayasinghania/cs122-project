# Weather Analysis App (CS 122 Summer 2026 Project)

## Authors
- Naya Singhania (Web data access and data organization)
- Jaden Navidad (Data analysis and visualization)

## Description
Our CS 122 project will be a historical weather analysis TKinter desktop application. 
This application will query historical data for a specific time period and location using a freely available weather API.
Upon pulling the specified data from this weather API, the data will be stored in a CSV file that can then be used for various analysis applications, such as a time series plot or calculations of average, maximum, and minimum temperature. 
The main goal of this application is to provide users insights into historical weather for where they live. 
With this information, they can better understand what future weather may look like in their area, whether it be for everyday use or enviormental awareness. Depending on feasability, this application may show the real-time weather for a selected location as well. 


## Outline
- We will use TKinter to create our user interface
- We will use CSV files to store data pulled from a weather API
- We will use numpy to analyze temperature trends over a specific period of time
- We will represent this data with a time series plot

## Detailed Description
This Weather Analysis App generates a historical graph of weather data. Users will be able to enter a US city of their choosing to get a time series plot of low and high temperatures throughout 3 time frames: 7 days, 30 days, and 1 year. Users will not only be able to see how temperatures rise and fall daily but can also view best fit trend lines of the data. They can also zoom in and out of the graph and save the plot as a PNG file onto their device. Additionally, users can also view the current temperature and overcast of their selected city, which will be displayed in a separate popup window.

## Installation Instructions
install conda python and matplotlib (will elaborate more on in a future edit)

## Changes/Updates We Would Pursue in the Future
(clean up later)
- update ui to be more visually interesting. it's quite bland currently
- update zoom function so that users can zoom into a specific part of the graph of their choosing, rather than just the middle
- add more cities?
