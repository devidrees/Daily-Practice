SELECT FROM idreesdb




CREATE TABLE movie_cast (
    movie_id INT REFERENCES movies(movie_id), 
    actor_id INT REFERENCES actors(actor_id),
    role VARCHAR(100),
    PRIMARY KEY (movie_id, actor_id)
)


SELECT * FROM movies

SELECT * FROM actors
SELECT * FROM movie_cast
SELECT * FROM directors

INSERT INTO movie_cast(movie_id,actor_id,role)
	VALUES (4,4,'Santosh'),
			(5,5,'Prakash');


SELECT columns -- List the columns you want to show in the result (e.g., table1.column1, table2.column2).
FROM table1		-- This is your first table.
INNER JOIN table2 -- This is the second table you're joining with the first one.
ON table1.column = table2.column; -- This specifies the condition that links the two tables, typically a common column (like an ID).


SELECT actors.first_name, actors.last_name, movie_cast.movie_id
FROM actors
INNER JOIN movie_cast ON actors.actor_id = movie_cast.actor_id

SELECT actors.first_name, actors.last_name, movie_cast.movie_id
FROM actors
FULL JOIN movie_cast ON actors.actor_id = movie_cast.actor_id

SELECT actors.first_name, movie_cast.movie_id
FROM actors
INNER JOIN movie_cast ON actors.actor_id = movie_cast.actor_id

SELECT actors.first_name, movie_cast.movie_id
FROM actors
RIGHT JOIN movie_cast ON actors.actor_id = movie_cast.actor_id

SELECT actors.first_name, movie_cast.movie_id
FROM actors
LEFT JOIN movie_cast ON actors.actor_id = movie_cast.actor_id


SELECT actors.first_name, movie_cast.movie_id
FROM actors
FULL OUTER JOIN movie_cast ON actors.actor_id = movie_cast.actor_id







DROP Table movies_cast











