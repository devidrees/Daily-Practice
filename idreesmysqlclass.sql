mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| moviesdb           |
| mysql              |
| performance_schema |
| sakila             |
| sys                |
| world              |
+--------------------+
7 rows in set (0.00 sec)

mysql> use moviesdb;
Database changed
mysql> select current_user();
+----------------+
| current_user() |
+----------------+
| root@localhost |
+----------------+
1 row in set (0.00 sec)

mysql> show variables like'datadir';
+---------------+---------------------------------------------+
| Variable_name | Value                                       |
+---------------+---------------------------------------------+
| datadir       | C:\ProgramData\MySQL\MySQL Server 8.0\Data\ |
+---------------+---------------------------------------------+
1 row in set (0.00 sec)

mysql> --tee C:/Users/Devid/desktop/savefile.sql
    -> ;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '--tee C:/Users/Devid/desktop/savefile.sql' at line 1
mysql> --tee C:/Users/Devid/desktop/savefile.sql;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '--tee C:/Users/Devid/desktop/savefile.sql' at line 1
mysql> -- tee C:/Users/Devid/desktop/savefile.sql;
mysql> - Create the Courses table
    -> CREATE TABLE courses (
    ->     course_id INT PRIMARY KEY,
    ->     course_name VARCHAR(100)
    -> );
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '- Create the Courses table
CREATE TABLE courses (
    course_id INT PRIMARY KEY,' at line 1
mysql> -- Create the Courses table
mysql> CREATE TABLE courses (
    ->     course_id INT PRIMARY KEY,
    ->     course_name VARCHAR(100)
    -> );
Query OK, 0 rows affected (0.01 sec)

mysql> -- Create the Students table
mysql> CREATE TABLE students (
    ->     student_id INT PRIMARY KEY,
    ->     student_name VARCHAR(100),
    ->     course_id INT,
    ->     FOREIGN KEY (course_id) REFERENCES courses(course_id)
    -> );
Query OK, 0 rows affected (0.03 sec)

mysql> select * from students
    -> ;
Empty set (0.00 sec)

mysql> select * from students;
Empty set (0.00 sec)

mysql> -- Insert data into Students
mysql> INSERT INTO students (student_id, student_name, course_id) VALUES
    -> (1, 'Alice', 1),
    -> (2, 'Bob', 2),
    -> (3, 'Charlie', 1),
    -> (4, 'David', NULL);  -- David is not enrolled in any course
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`moviesdb`.`students`, CONSTRAINT `students_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`))
mysql> select * from students
    -> limit 10;
Empty set (0.00 sec)

mysql> INSERT INTO students (student_id, student_name, course_id) VALUES
    -> (1, 'Alice', 1),
    -> (2, 'Bob', 2),
    -> (3, 'Charlie', 1),
    -> (4, 'David', NULL);
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`moviesdb`.`students`, CONSTRAINT `students_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`))
mysql> delete students;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1
mysql> delete * students;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '* students' at line 1
mysql> drop students;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'students' at line 1
mysql> drop courses;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'courses' at line 1
mysql> use moviesdb
Database changed
mysql> drop courses;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'courses' at line 1
mysql> drop table students;
Query OK, 0 rows affected (0.01 sec)

mysql> drop table courses;
Query OK, 0 rows affected (0.01 sec)

mysql> -- Create the Courses table
mysql> CREATE TABLE courses (
    ->     course_id INT PRIMARY KEY,
    ->     course_name VARCHAR(100)
    -> );
Query OK, 0 rows affected (0.02 sec)

mysql> 
mysql> -- Create the Students table
mysql> CREATE TABLE students (
    ->     student_id INT PRIMARY KEY,
    ->     student_name VARCHAR(100),
    ->     course_id INT,
    ->     FOREIGN KEY (course_id) REFERENCES courses(course_id)
    -> );
Query OK, 0 rows affected (0.02 sec)

mysql> -- Insert data into Courses
mysql> INSERT INTO courses (course_id, course_name) VALUES
    -> (1, 'Mathematics'),
    -> (2, 'Physics'),
    -> (3, 'Chemistry');
Query OK, 3 rows affected (0.01 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> -- Insert data into Students
mysql> INSERT INTO students (student_id, student_name, course_id) VALUES
    -> (1, 'Alice', 1),   -- Enrolled in Mathematics
    -> (2, 'Bob', 2),     -- Enrolled in Physics
    -> (3, 'Charlie', 1), -- Enrolled in Mathematics
    -> (4, 'David', NULL);  -- David is not enrolled in any course (NULL is acceptable)
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM courses;
+-----------+-------------+
| course_id | course_name |
+-----------+-------------+
|         1 | Mathematics |
|         2 | Physics     |
|         3 | Chemistry   |
+-----------+-------------+
3 rows in set (0.00 sec)

mysql> SELECT * FROM students;
+------------+--------------+-----------+
| student_id | student_name | course_id |
+------------+--------------+-----------+
|          1 | Alice        |         1 |
|          2 | Bob          |         2 |
|          3 | Charlie      |         1 |
|          4 | David        |      NULL |
+------------+--------------+-----------+
4 rows in set (0.00 sec)

mysql> SELECT s.Alice,c.Physics
    -> FROM students s
    -> INNER JOIN courses c ON s.course_id = c.course_id;
ERROR 1054 (42S22): Unknown column 's.Alice' in 'field list'
mysql> SELECT s.Alice,c.Mathematics
    -> FROM students s;
ERROR 1054 (42S22): Unknown column 's.Alice' in 'field list'
mysql> SELECT s.student_name, c.course_name
    -> FROM students s
    -> INNER JOIN courses c ON s.course_id = c.course_id;
+--------------+-------------+
| student_name | course_name |
+--------------+-------------+
| Alice        | Mathematics |
| Charlie      | Mathematics |
| Bob          | Physics     |
+--------------+-------------+
3 rows in set (0.00 sec)

mysql> select * FROM c.course_id;
ERROR 1049 (42000): Unknown database 'c'
mysql> select * FROM c;
ERROR 1146 (42S02): Table 'moviesdb.c' doesn't exist
mysql> select * FROM courses;
+-----------+-------------+
| course_id | course_name |
+-----------+-------------+
|         1 | Mathematics |
|         2 | Physics     |
|         3 | Chemistry   |
+-----------+-------------+
3 rows in set (0.00 sec)

mysql> select * FROM students;
+------------+--------------+-----------+
| student_id | student_name | course_id |
+------------+--------------+-----------+
|          1 | Alice        |         1 |
|          2 | Bob          |         2 |
|          3 | Charlie      |         1 |
|          4 | David        |      NULL |
+------------+--------------+-----------+
4 rows in set (0.00 sec)

mysql> SELECT s.student_name, c.course_name
    -> FROM students s
    -> INNER JOIN courses c ON s.course_id = c.course_id;
+--------------+-------------+
| student_name | course_name |
+--------------+-------------+
| Alice        | Mathematics |
| Charlie      | Mathematics |
| Bob          | Physics     |
+--------------+-------------+
3 rows in set (0.00 sec)

mysql> Terminal close -- exit!
