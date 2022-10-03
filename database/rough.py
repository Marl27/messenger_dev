'''
-- TEST DATA EMPLOYEES
INSERT INTO employees
( first_name, middle_name, last_name, username, password, start_date, leaving_date)
VALUES( 'char', 's', 'Rut', 'char.rut', 'password', '01/01/2022', '');

INSERT INTO employees
( first_name, middle_name, last_name, username, password, start_date, leaving_date)
VALUES( 'him', 's', 'sah', 'him.s', 'password', '30/10/2022', '');

INSERT INTO employees
( first_name, middle_name, last_name, username, password, start_date, leaving_date)
VALUES( 'random', 's', 'person', 'random.p', 'password', '28/10/2022', '');


-- TEST DATA MESSENGER
INSERT INTO messenger
(sender, receiver, is_broadcasted, group_name, message, stared)
VALUES(1, '2,3', 0, 'group_1', 'anyone home?', 0	);

INSERT INTO messenger
(sender, receiver, is_broadcasted, message, stared)
VALUES(1, '2', 0, 'private message', 0	);



SELECT * FROM employees e

SELECT *
FROM messenger m
WHERE receiver = 2
'''