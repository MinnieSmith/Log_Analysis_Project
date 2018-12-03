# Log Analysis Project

A reporting tool for extracting useful high level information from a historical database of an article website.

## Overview

The website is a newspaper site. It collects information log for each time the reader loads the web page. This information is stored in a relational database. This repository holds a Python 2.7 program which is able to connect to this database, uses SQL queries to analyse the data and outputs useful information.

## Requirements

Python 2.7 with psycopg2 installed (to connect to the pSQL database).

```bash
pip install psycopg2
```

## Quick Start Guide

Clone the directory and you should able to run the program out of the box. The program does not accept any input arguments.

```bash
# Clone the directory.
git clone https://github.com/MinnieSmith/Log_Analysis_Project.git

# Go into the directory.
cd Log_Analysis_Project

# Run the program in your active Python environment.
python loganalysisprogram.py
```

After running the program you should see some output in `stdout` that looks like this:

![SampleOutput](SampleOutput.png)

## Function Design

| Function              | Returns | Description                                                  |
| --------------------- | ------- | ------------------------------------------------------------ |
| `get_posts(query)`    | `list`  | This function connects to and retrieves information from the database. It accepts one string argument  `query`  which is a SQL query. |
| ` popular_articles()` | `None`  | Print a list of the most popular articles and number of views. |
| `popular_authors()`   | `None`  | Prints a list of the authors with most articles viewed and the number of views. |
| ` request_errors()`   | `None`  | Prints a list of days where the error rate was higher than 1% and the percentage. |



## Additional Explantion

```python
def get_posts(query):
```

Connects to the database, send queries and fectches results of different psql. This function allows us to get different outputs from the database by changing the psql `query` input.  

```python
def popular_articles():
```

Queries the database for the most popular article and the number of views. This is achieved by concatinating '/article/' to articles.slug so articles and logs could be joined. The query returns the top three articles and number of views. 

```python
def popular_authors():
```

This queries joins articles.slug and log.path with authors.name to render the top three authors with the most number of articles viewed.

```python 
def request_errors():
```

Multiple subqueries were employed to return the error count and the total number of rows. They were grouped by day to calculate the percentage error. The query returns a datetime string and the percentage error on days where the error rate was higher than 1%. The datetime string  had to be formated with the `date time.strftime()` function.



## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/MinnieSmith/Log_Analysis_Project/blob/master/License.txt) file for details