# baltimore-city-police-data-636

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### Motivation
The motivation behind this proposal is to use visualization to better understand
the crime, arrests, traffic stops, and service calls to provide insight into more
effective policing for the city of Baltimore.

### Dataset Description
The crime dataset involves multiple featured attributes including incidents
dates/time, crime codes, categories, geography and location related
information. Since crime is a multifaceted and socio-economic issue, we will
join other available datasets such as census and demographic data to help in
analyzing trends in crime between neighborhoods of income inequality.

### Visualization Approaches
Several visualization techniques will be employed to thoroughly illustrate and
explore the evolutionary tendency and incident patterns spatially and temporarily.
Then, we will apply one or two technologies for the final release. Considering the geographic nature of the crime incidents, an interactive
map of Baltimore City will be used for geo-spatial visualization.

### Roles of participants
* Dingyi Pei: Matlab programmer, Data Analyst (Tableau)
* Jason Seaman: Web Developer, Data Analyst (Tableau)
* Paul Ledala: Python Developer, Data Engineer
* Rohit Mokashi: Web Developer, D3.js, Data Analyst (Tableau)
* Vineeth NC: Data Engineer, Python Programmer

### Visualizations
* Map of municipal bounds of Baltimore city in the main view. The varied colored spots represent different types of the crime happened and recorded by Baltimore Police Department.

![Baltimore city map with crime points](https://github.com/rohitmokashi16/baltimore-city-police-data/blob/main/visualizations/screenshot-1.png)

* The view of dashboard with parameter selection and visualization plotted.

![Neighborhood view with crime points](https://github.com/rohitmokashi16/baltimore-city-police-data/blob/main/visualizations/screenshot-3.png)

* Monthly averaged crimes happened on different districts of Baltimore city in 2019. The incidents are illustrated as a box plot, showing the averaged incidents over month as well as the range of number of crimes.

![Incidents by district grouped by month](https://github.com/rohitmokashi16/baltimore-city-police-data/blob/main/visualizations/screenshot-4.png)

* Monthly averaged crimes happened on different districts of Baltimore city in 2019. The incidents are illustrated as a bar chart, showing the total numbers of incidents happened over month.

![Bar chart of incident count by districts](https://github.com/rohitmokashi16/baltimore-city-police-data/blob/main/visualizations/screenshot-6.png)

* Monthly averaged crimes happened indoors/outdoors of Baltimore city in 2019. The incidents are illustrated as a line chart, showing the tendency of the total numbers of incidents happened over month.

![Bar chart of incident count by districts](https://github.com/rohitmokashi16/baltimore-city-police-data/blob/main/visualizations/screenshot-5.png)

* Incident heatmap calendar of year 2016. The total number of happened each day is represented as a heatmap in a calendar, providing a general view of the amount of the crime over a year.

![Bar chart of incident count by districts](https://github.com/rohitmokashi16/baltimore-city-police-data/blob/main/visualizations/screenshot-8.png)
