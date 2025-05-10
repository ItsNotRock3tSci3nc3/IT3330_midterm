import mysql.connector
from mysql.connector import errorcode

def get_db_connection():
    #create a connection to the module2 database
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            port="6603",
            database="hr"
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
            exit()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            exit()
        else:
            print(f"Error: {err}")
            print("Service not available")
            exit()

    
    return mydb


#read data methods--------------------------------------------------------------------------------------------------------------------------
def get_employees_hired():
    #get a coneection to the database
    mydb = get_db_connection()

    #create a cursor to execute ueries
    db_cursor = mydb.cursor(dictionary=True)

    year = 0
    year = input("Enter year or \'All\' to view hiring data for all years in departments: ")
    if year.isalpha():
        year = year.lower()
        year = year.capitalize()

    
    err_invalid = False
    sql_query = ""
    if year == "All" :
        sql_query =(
        """
        SELECT YEAR(hire_date) AS "Year", department_name, COUNT(employee_id) AS "Employees Hired"
        FROM employees, departments
        GROUP BY department_name, YEAR(hire_date)
        ORDER BY department_name;
        """
        )
        db_cursor.execute(sql_query)
    else:
        sql_query =(
        """
        SELECT YEAR(hire_date) AS "Year", department_name, COUNT(employee_id) AS "Employees Hired"
        FROM employees, departments
        WHERE YEAR(hire_date) = (%s)
        GROUP BY department_name, YEAR(hire_date)
        ORDER BY department_name;
        """
        )
        db_cursor.execute(sql_query, (year,))

    
    
    query_result = db_cursor.fetchall()
    if len(query_result) == 0:
        print(f"No results for \'{year}\'")
        return

    print("Hires by year and department\n---------------------")
    for record in query_result:
        print(f"{record['Year']}  {record['department_name']}:   {record['Employees Hired']} hire(s)")
    
    mydb.close()
    return



def get_avg_salary_per_title():
    #get a coneection to the database
    mydb = get_db_connection()

    #create a cursor to execute ueries
    db_cursor = mydb.cursor(dictionary=True)

    job = ""
    job = input("Enter a job title or \'All\' to view hiring data for all years in departments: ")
    job = job.lower()
    job = job.capitalize()

    err_invalid = False
    sql_query = ""
    if job == "All" :
        sql_query =(
        """
        SELECT j.job_title, AVG(e.salary) AS "Average Salary", COUNT(e.employee_id) AS "Number of Employees"
        FROM employees e, jobs j
        WHERE e.job_id = j.job_id
        GROUP BY job_title
        ORDER BY AVG(salary) DESC;
        """
        )
        db_cursor.execute(sql_query)
          
    else:
        sql_query =(
        """
        SELECT j.job_title, AVG(e.salary) AS "Average Salary", COUNT(e.employee_id) AS "Number of Employees"
        FROM employees e, jobs j
        WHERE e.job_id = j.job_id AND j.job_title = %s
        GROUP BY job_title
        ORDER BY AVG(salary) DESC;
        """
        )
        db_cursor.execute(sql_query, (job,))

    
    
    query_result = db_cursor.fetchall()
    if len(query_result) == 0:
        print(f"No results for \'{job}\'")
        return
    
    print("Average salary per department\n---------------------")
    for record in query_result:
        print(f"{record['job_title']}:  ${record['Average Salary']}")
    
    mydb.close()
    return



def get_avg_salary_per_dept():
    #get a coneection to the database
    mydb = get_db_connection()

    #create a cursor to execute ueries
    db_cursor = mydb.cursor(dictionary=True)

    dept = ""
    dept = input("Enter a job title or \'All\' to view hiring data for all years in departments: ")
    dept = dept.lower()
    dept = dept.capitalize()

    sql_query = ""
    if dept == "All" :
        sql_query =(
        """
        SELECT d.department_name, AVG(e.salary) AS "Average Salary", COUNT(e.employee_id) AS "Number of Employees"
        FROM employees e, departments d
        WHERE e.department_id = d.department_id 
        GROUP BY department_name
        ORDER BY AVG(salary) DESC;
        """
        )
        db_cursor.execute(sql_query)
    else:
        sql_query =(
        """
        SELECT d.department_name, AVG(e.salary) AS "Average Salary", COUNT(e.employee_id) AS "Number of Employees"
        FROM employees e, departments d
        WHERE e.department_id = d.department_id AND d.department_name = %s
        GROUP BY department_name
        ORDER BY AVG(salary) DESC;
        """
        )
        db_cursor.execute(sql_query, (dept,))

    
    
    query_result = db_cursor.fetchall()
    if len(query_result) == 0:
        print(f"No results for \'{dept}\'")
        return

    print("Average salary per department\n---------------------")
    for record in query_result:
        print(f"{record['department_name']}:  ${record['Average Salary']}")
    
    mydb.close()
    return
#end read data methods


#add data method(s) -- add dependent ---------------------------------------------------------------------------------------------------------
def add_dependent():
    print("ADD DEPENDENT")
    first_name = input("Enter dependent first name: ")
    last_name = input("Enter dependent last name: ")
    relationship = input("Enter relationship to dependent: ")
    
    try:
        employee_id = int(input("Enter employee ID: "))
    except ValueError:
        print("Error: Employee ID must be a number.")
        return

    try:
        # Establish connection to your MySQL database (update connection details as needed)
        mydb = get_db_connection()
        db_cursor = mydb.cursor()

        sql_query = """
            INSERT INTO dependents (first_name, last_name, relationship, employee_id)
            VALUES (%s, %s, %s, %s);
        """
        db_cursor.execute(sql_query, (first_name, last_name, relationship, employee_id))
        mydb.commit()

        print("Dependent added successfully!")
    except mysql.connector.Error as err:
        print("Error while adding dependent:", err)
    finally:
        if mydb.is_connected():
            db_cursor.close()
            mydb.close()
    return
#end add data method(s)


#delete data method(s) -----------------------------------------------------------------------------------------------------------------------
def delete_dependent():
    print("DELETE DEPENDENT")
    try:
        dependent_id = int(input("Enter the dependent ID to delete: "))
    except ValueError:
        print("Error: Dependent ID must be a number.")
        return

    try:
        # Use the existing function to get a database connection
        mydb = get_db_connection()
        db_cursor = mydb.cursor()

        sql_query = """
            DELETE FROM dependents
            WHERE dependent_id = %s;
        """
        db_cursor.execute(sql_query, (dependent_id,))
        mydb.commit()

        if db_cursor.rowcount > 0:
            print("Dependent deleted successfully!")
        else:
            print("No dependent found with that ID.")

    except Exception as e:
        print("Error while deleting dependent:", e)
    finally:
        if mydb.is_connected():
            db_cursor.close()
            mydb.close()
    return
#end delete data method(s)


#update data method(s) -------------------------------------------------------------------------------------------------------------------------
def update():
    print("UPDATE JOB MAXIMUM SALARY")
    try:
        # Prompt for inputs
        job_id = input("Enter job ID: ")
        new_max_salary = float(input("Enter new maximum salary: "))
    except ValueError:
        print("Error: Job ID should be a valid identifier and salary must be a number.")
        return

    try:
        # Connect to the database using the provided connection method
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Retrieve the current minimum salary for the job
        select_query = "SELECT min_salary FROM jobs WHERE job_id = %s"
        cursor.execute(select_query, (job_id,))
        result = cursor.fetchone()

        if not result:
            print("Error: No job found with the provided job ID.")
            return

        min_salary = result['min_salary']

        # Check if the new maximum salary is greater than the minimum salary
        if new_max_salary <= min_salary:
            print("Error: The new maximum salary must be greater than the minimum salary.")
            return

        # Proceed to update the job's maximum salary
        update_query = "UPDATE jobs SET max_salary = %s WHERE job_id = %s"
        cursor.execute(update_query, (new_max_salary, job_id))
        conn.commit()

        if cursor.rowcount > 0:
            print("Job's maximum salary updated successfully!")
        else:
            print("No rows updated. Please verify the job ID.")

    except Exception as e:
        print("Error updating job maximum salary:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    return
#end update data method(s)


def menu():
    while True:
        print("\nSelect an option:")
        print("1: View Hiring Data by year and department")
        print("2: View average salary data by job title")
        print("3: View average salary data by department")
        print("4: Add dependent")
        print("5: Delete a dependent")
        print("6: Update job maximum salary")
        print("7: Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            get_employees_hired()  # Ensure this function is defined
        elif choice == "2":
            get_avg_salary_per_title()              # Ensure this function is defined
        elif choice == "3":
            get_avg_salary_per_dept()             # Ensure this function is defined
        elif choice == "4":
            add_dependent()                             # Previously defined add_dependent function
        elif choice == "5":
            delete_dependent()                          # Previously defined delete_dependent function
        elif choice == "6":
            update()                       # Previously defined update_job_max_salary function
        elif choice == "7":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 7.")

# Example usage: call the menu function to start the program.
if __name__ == "__main__":
    menu()