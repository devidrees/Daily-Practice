

"C:\Users\devid\Desktop\moviesds\links.csv"

movieID, imdbId, tmdbId

CREATE TABLE links (
	movieID INT, 
	imdbId INT, 
	tmdbId INT
);

select * from links

\COPY links(movieID, imdbId, tmdbId)
FROM 'C:\Users\devid\Desktop\moviesds\links.csv'
DELIMITER ','
CSV HEADER;


