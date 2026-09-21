// CRUD Operations
use("CrudDb")

db.createCollection("courses")

// Create (Insert)

db.courses.insertOne({
    name: "My Web Dev course",
    price: 0,
    assignments: 12, 
    projects: 45
})

db.courses.insertMany(
    [
        {
          "name": "My Web Dev Course",
          "price": 0,
          "assignments": 12,
          "projects": 45
        },
        {
          "name": "Advanced Python",
          "price": 200,
          "assignments": 20,
          "projects": 30
        },
        {
          "name": "Java for Beginners",
          "price": 150,
          "assignments": 15,
          "projects": 25
        },
        {
          "name": "Full Stack Development",
          "price": 300,
          "assignments": 25,
          "projects": 50
        },
        {
          "name": "Machine Learning Basics",
          "price": 250,
          "assignments": 18,
          "projects": 35
        },
        {
          "name": "React and Redux",
          "price": 180,
          "assignments": 10,
          "projects": 20
        },
        {
          "name": "Data Structures in Python",
          "price": 100,
          "assignments": 22,
          "projects": 40
        },
        {
          "name": "CSS Mastery",
          "price": 80,
          "assignments": 8,
          "projects": 15
        },
        {
          "name": "JavaScript Essentials",
          "price": 120,
          "assignments": 12,
          "projects": 28
        },
        {
          "name": "SQL and Databases",
          "price": 90,
          "assignments": 14,
          "projects": 25
        }
      ]
)

// Read 

let a = db.courses.find({price: 0})
console.log(a.count())

let b = db.courses.findOne({price: 90})
console.log(b)

// Update 

db.courses.updateOne({price: 120}, {$set: {price: 150}})

db.courses.updateMany({name: "Data Structures in Python"}, {$set: {projects: 20}})

db.courses.updateMany({}, {$mul: {price: 1.2}})

// Delete

db.courses.deleteOne({price: 0})

db.courses.deleteMany({})

// https://www.mongodb.com/docs/manual/reference/operator/query/