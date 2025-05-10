--1: calculate the number of employees hired each year in each department, Order results by department name. 
-- Remember the SQL $year function, and you will have to group by two columns
SELECT YEAR(hire_date) AS "Year", department_name, COUNT(employee_id) AS "Employees Hired"
FROM employees, departments
WHERE YEAR(hire_date) = $
GROUP BY department_name, YEAR(hire_date)
ORDER BY department_name;

--2: calculate the average salary for each job title. 
--Display the job title, average salary in a column named "Average salary", and number of employees with that title in a column called "Number of Employees"  
--display results in descending order by average salary.
SELECT j.job_title, AVG(e.salary) AS "Average Salary", COUNT(e.employee_id) AS "Number of Employees"
FROM employees e, jobs j
WHERE e.job_id = j.job_id AND j.job_title = $
GROUP BY job_title
ORDER BY AVG(salary) DESC;

--3: calculate average salaries for each department. 
--Display the department name, average salary in a column named "Average salary", 
--and number of employees with that title in a column called "Number of Employees"
SELECT d.department_name, AVG(e.salary) AS "Average Salary", COUNT(e.employee_id) AS "Number of Employees"
FROM employees e, departments d
WHERE e.department_id = d.department_id
GROUP BY department_name
ORDER BY AVG(salary) DESC;

--Add dependent: Insert into dependents table
INSERT INTO dependents(first_name, last_name, relationship, employee_id)
VALUES ($, $, $, $)

--Delete dependent: delete dependent info from table
DELETE FROM dependents
WHERE dependent_id = $

--Update Data
UPDATE jobs
SET max_salary = CASE
    WHEN $ > (SELECT min_salary FROM jobs) THEN $
    ELSE max_salary
END
WHERE job_id = $

