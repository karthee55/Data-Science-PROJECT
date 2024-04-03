import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import sqlite3

#1 Connection to the database

db=#file path (movies.sqlite)
conn=sqlite3.connect(db)
cur=conn.cursor()

#2 data about movies
cur.execute('select*from movies')
movies= cur.fetchall()

#
movie= pd.DataFrame(movies,columns=['id','originial_title','budget','popularity','release_date','revenue','title','vote_average','vote_count','overview','agline','uid','director_id'])
movie.info()

#3 Data about directors
cur.execute('select*from directors')
directors= cur.fetchall()

#
director=pd.DataFrame(directors,columns=['Name','ID','Gender','UID','Department'])
director.info() 

#4 Number of movies present in the IMDB database
cur.execute('select count(Title) from movies')
count=cur.fetchall()
print(f"The Number of movies present in the IMDB database is {count[0]}")

#5 find these directors
cur.execute("select*from directors where name=='James Cameron'or name=='Luc Besson' or name= 'John Woo' ")
three_directors=cur.fetchall()
print(three_directors)

#6 the directors whose names are starting with the word 'Steven'
cur.execute(' select*from directors where name like "Steven%" ' )
name_like=cur.fetchall()
print(f"The directors whose names are starting with the word 'Steven' are: {name_like}")

#7 count number of female directors
cur.execute("SELECT COUNT(*) FROM directors WHERE gender=='1'")
females=cur.fetchall()
print(f"The number of female directors is {females[0][0]}")

#8 name of the 10th women director
cur.execute('SELECT name FROM directors WHERE gender==1')
female=cur.fetchall()
#print(f"The name of the 10th women director is {female[9][0]}")

#9 What are the 3 most popular movies
cur.execute("SELECT title FROM movies ORDER BY popularity DESC LIMIT  3")
most_popularity=cur.fetchall()
print(f"The 3 mostpopular movies are: {most_popularity[0][0]}, {most_popularity[1][0]} and {most_popularity[2][0]}")

#10 the 3most bankable movies
cur.execute('SELECT title FROM movies ORDER BY budget DESC LIMIT 3')
most_bankable=cur.fetchall()
print(f"The 3 mostbankable movies are: {most_bankable[0][0]}, {most_bankable[1][0]} and {most_bankable[2][0]}")

#11 Most awarded average rated movie since the jan 1st, 2000?
cur.execute("SELECT original_title FROM movies where Release_date> '2000-01-01' ORDER BY vote_average DESC LIMIT 1")
most_awarderd=cur.fetchall()
print(f"The most awarded avearage rated movie is {most_awarderd[0][0]}")

#12 which movie is directed by Brenda chapman?
cur.execute("SELECT original_title FROM movies JOIN directors on directors.id=movies.director_id where directors.name='Brenda Chapman' ")
dirc_name=cur.fetchall()
print(f"The movie(s) directed by Brenda Chapman is {dirc_name[0][0]}" )

#13 Name the director who has made the most movies?
cur.execute("SELECT name FROM directors JOIN movies on directors.id=movies.director_id GROUP BY director_id ORDER BY COUNT(name) DESC limit 1")
director_movie=cur.fetchall()
print(f"The director who made the most movie is {director_movie[0][0]}")

#14 Name of the director who is the most bankable
cur.execute("SELECT name FROM directors JOIN movies on directors.id=movies.director_id GROUP BY director_id ORDER BY SUM(budget) DESC limit 1")
most_bankalbe_dir=cur.fetchall()
print(f"The Most Bankable director is {most_bankalbe_dir[0][0]}")

##BUDGET ANALYSIS
#1 Tell the top 10 hidhest budget making movie
cur.execute('Select * FROM movies ORDER BY budget DESC LIMIT 10')
top_10 = cur.fetchall()
most_popular = pd.DataFrame(top_10, columns=['id', 'original_title', 'budget', 'popularity', 'release_date',
       'revenue', 'title', 'vote_average', 'vote_count', 'overview', 'tagline',
       'uid', 'director_id'])
print(most_popular)

##REVENUE ANALYSIS
#1Find top 10 revenue making movies
cur.execute("SELECT * FROM movies ORDER BY revenue DESC LIMIT 10")
top10_movies = cur.fetchall()
most_revenue = pd.DataFrame(top10_movies,  columns= ['id','original_title','budget','popularity','release_date',
                                    'revenue', 'title','vote_average','vote_count','overview',
                                    'tagline','uid','director_id'])
print(most_revenue)

##VOTING ANALYSIS
#1 Find the most popuar movies ith highest vote_average
cur.execute("SELECT * FROM movies ORDER BY vote_average DESC LIMIT 10")
most_pop = cur.fetchall() 
most_popular_movie = pd.DataFrame(most_pop,columns =['id', 'original_title', 'budget', 'popularity', 'release_date',
       'revenue', 'title', 'vote_average', 'vote_count', 'overview', 'tagline',
       'uid', 'director_id'])
print(most_popular_movie)

##DIRECTOR ANALYSIS
#1. Name all the directors with the number of movies and revenue where Revenue should be taken into account for doing the analysis. The director who has the highest revenue should comes at the top and so on and so forth.
cur.execute("SELECT name,COUNT(*) AS 'Total Movies',SUM(revenue) AS 'Total Revenue' FROM  directors JOIN movies WHERE directors.id==movies.director_id GROUP BY director_id ORDER BY SUM(revenue) DESC")
director_revenue=cur.fetchall()
director_most_revenue=pd.DataFrame(director_revenue,columns=['Director_Name','Total Movies','Total Revenue'])
print(director_most_revenue.head(10))

#2. Name all the directors with the number of movies and revenue where number of movies should be taken into account for doing the analysis. The director who has the highest number of movies should comes at the top and so on and so forth.
cur.execute("SELECT name, COUNT(title), SUM(revenue) FROM directors JOIN movies ON movies.director_id = directors.id GROUP by director_id ORDER BY  COUNT(title) DESC LIMIT 10")
director_movies = cur.fetchall()
director_most_movies = pd.DataFrame(director_movies,columns=['name','no_of_title','revenue'])
print(director_most_movies)

#3. Give the Title of the movie, realease_date, budget, revenue, popularity and vote_average made by Steven Spielberg
cur.execute("SELECT title, release_date,budget,revenue,popularity,vote_average FROM directors JOIN movies ON directors.id==movies.director_id WHERE directors.name=='Steven Spielberg'")
movies_list=cur.fetchall()
movies_list_Steven_Spielberg=pd.DataFrame(movies_list,columns=['Movie_Name','Release_Date','Total Budget','Total_Revenue','Popularity','Vote_Average'])
print(movies_list_Steven_Spielberg)
