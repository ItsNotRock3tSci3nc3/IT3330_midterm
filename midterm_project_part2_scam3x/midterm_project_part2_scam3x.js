// Query 1: View Total Payments by Customer
db.payments.aggregate([
  {
    $lookup: {
      from: "customers",
      localField: "customerNumber",
      foreignField: "customerNumber",
      as: "customer"
    }
  },
  { $unwind: "$customer" },
  {
    $group: {
      _id: "$customer.customerName",
      totalPayments: { $sum: "$amount" }
    }
  },
  { $sort: { totalPayments: -1 } }
]);

// Query 2: View Product Inventory Value
db.products.aggregate([
  {
    $project: {
      _id: "$productName",
      dollarValue: { $multiply: ["$quantityInStock", "$buyPrice"] }
    }
  },
  { $sort: { dollarValue: -1 } }
]);

// Query 3: View Total Number of Products Ordered
db.orderdetails.aggregate([
  {
    $lookup: {
      from: "products",
      localField: "productCode",
      foreignField: "productCode",
      as: "product"
    }
  },
  { $unwind: "$product" },
  {
    $group: {
      _id: "$product.productName",
      quantityOrdered: { $sum: "$quantityOrdered" }
    }
  },
  { $sort: { quantityOrdered: -1 } }
]);

// CRUD Operations for Employees:

// (a) Insert/Add an Employee
db.employees.insertOne({
  _id: "EMP1001",           // Use a unique employee id (string or number)
  lastName: "Smith",         // Example last name
  firstName: "John",         // Example first name
  jobTitle: ""               // Default job title is an empty string
});

// (b) Update Employee Job Title
db.employees.updateOne(
  { _id: "EMP1001" },        // Replace with the employee id
  { $set: { jobTitle: "Sales Manager" } }  // Replace with the new job title
);

// (c) Delete an Employee
db.employees.deleteOne({ _id: "EMP1001" });  // Replace with the employee id to delete
