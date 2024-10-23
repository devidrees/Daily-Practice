CREATE TABLE movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(100),
    director_id INT
);

INSERT INTO movies (movie_id, title, director_id) VALUES
(1, 'Inception', 101),
(2, 'Interstellar', 101),
(3, 'Dunkirk', 102),
(4, 'Memento', 103),
(5, 'Inception', 104),
(6, 'Inception', 105),
(7, 'Inception', 106)

CREATE TABLE directors (
    director_id INT PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO directors (director_id, name) VALUES
(101, 'Christopher Nolan'),
(102, 'Quentin Tarantino'),
(104, 'Steven Spielberg');

SELECT * FROM movies
SELECT * FROM directors

SELECT columns -- List the columns you want to show in the result (e.g., table1.column1, table2.column2).
FROM table1		-- This is your first table.
INNER JOIN table2 -- This is the second table you're joining with the first one.
ON table1.column = table2.column; -- This specifies the condition that links the two tables, typically a common column (like an ID).

SELECT movies.title, directors.name, directors.director_id
FROM movies
FULL JOIN directors
ON movies.director_id = directors.director_id;