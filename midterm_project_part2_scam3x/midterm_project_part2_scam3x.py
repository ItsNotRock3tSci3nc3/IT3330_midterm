import pymongo
from pymongo import MongoClient
import sys

def connect_db():
    try:
        mongo_client = MongoClient(
            host="localhost:17027",
            username = "",
            password = "",
            socketTimeoutMS=3000
    )

    except Exception as err:
        print(f"Error Occured: {err}\nExiting the program...")
        quit()

    #get a connection to classicmodels
    db = mongo_client["classicmodels"]  
    return db

def view_total_payments_by_customer(db): #1
    try:
        collection = db.customers
        user_input = input("Enter customer name or (All) to view total payments for all customers: ").strip()
        
        pipeline = [
            {"$group": {
                "_id": "$customerName",
                "totalPayments": {"$sum": "$payments.amount"}}},
            {"$sort": {"totalPayments": -1}}
        ]
        
        if user_input.lower() != "all":
            pipeline.insert(
                0, {"$match": { "customer.customerName": user_input }}
            )
        
        results = list(collection.aggregate(pipeline))
        
        if results:
            for r in results:
                print(f"{r['_id']}: ${r['totalPayments']:.2f}")
        else:
            print("No data found for the specified input.")
    except Exception as e:
        print(f"Error in query: {e}")

def view_product_inventory_value(db): #2
    try:
        collection = db.products
        user_input = input("Enter product name or (All) to view inventory values for all products: ")
        
        pipeline = [
            {"$project": {
                "_id": "$productName",
                "dollarValue": {"$multiply": ["$quantityInStock", "$buyPrice"]}
            }},
            {"$sort": {"dollarValue": -1}}
        ]
        results = list(collection.aggregate(pipeline))
        
        if user_input.lower() != "all":
            results = [r for r in results if r["_id"].lower() == user_input.lower()]
        
        if results:
            for r in results:
                print(r)
        else:
            print("No data found for the specified product.")
    except Exception as e:
        print(f"Error in query: {e}")

def view_total_products_ordered(db): #3
    try:
        collection = db.orderdetails
        user_input = input("Enter product name or (All) to view total quantity ordered for all products: ").strip()
        
        pipeline = []

        if user_input.lower() != "all":
            pipeline.append({"$match": {"orderDetails.productName": user_input}})

        pipeline.extend([
            {"$group": {
                "_id": "$orderDetails.productName",
                "quantityOrdered": {"$sum": "$orderDetails.quantityOrdered"}
            }},
            {"$sort": {"quantityOrdered": -1}}
        ])
        
        results = list(collection.aggregate(pipeline))
        
        if results:
            for r in results:
                print(f"{r['_id']}: {r['quantityOrdered']}")
            else:
                print("No data found for the specified product.")
    except Exception as e:
        print(f"Error in query: {e}")

def add_employee(db): #4
    try:
        collection = db.employees
        employee_id = input("Enter employee _id: ").strip()
        last_name = input("Enter employee last name: ").strip()
        first_name = input("Enter employee first name: ").strip()
        
        employee = {
            "_id": employee_id,
            "lastName": last_name,
            "firstName": first_name,
            "jobTitle": ""  # default job title
        }
        result = collection.insert_one(employee)
        if result.acknowledged:
            print("Employee added successfully.")
        else:
            print("Employee not added.")
    except Exception as e:
        print(f"Error adding employee: {e}")

def update_employee_job_title(db): #5
    try:
        collection = db.employees
        employee_id = input("Enter employee _id to update: ").strip()
        new_title = input("Enter new job title: ").strip()
        
        result = collection.update_one({"_id": employee_id}, {"$set": {"jobTitle": new_title}})
        if result.modified_count > 0:
            print("Employee job title updated successfully.")
        else:
            print("No matching employee found or no change made.")
    except Exception as e:
        print(f"Error updating employee: {e}")

def delete_employee(db): #6
    try:
        collection = db.employees
        employee_id = input("Enter employee _id to delete: ").strip()
        
        result = collection.delete_one({"_id": employee_id})
        if result.deleted_count > 0:
            print("Employee deleted successfully.")
        else:
            print("No employee found with the given _id.")
    except Exception as e:
        print(f"Error deleting employee: {e}")

def print_menu():
    print("\nClassic Models Application")
    print("1. View Total Payments by Customer")
    print("2. View Product Inventory Value")
    print("3. View Total Number of Products Ordered")
    print("4. Add an Employee")
    print("5. Update Employee Job Title")
    print("6. Delete an Employee")
    print("7. Exit")

def main():
    db = connect_db()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            view_total_payments_by_customer(db)
        elif choice == "2":
            view_product_inventory_value(db)
        elif choice == "3":
            view_total_products_ordered(db)
        elif choice == "4":
            add_employee(db)
        elif choice == "5":
            update_employee_job_title(db)
        elif choice == "6":
            delete_employee(db)
        elif choice == "7":
            print("Exiting application.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
