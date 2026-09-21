/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// Select the database to use.
use('WebdevDatabase');

// Insert a few documents into the courses collection.
db.getCollection('courses').insertMany([
    {
      "name": "Python",
      "price": 15000
    },
    {
      "name": "JavaScript",
      "price": 18000
    },
    {
      "name": "HTML",
      "price": 12000
    },
    {
      "name": "CSS",
      "price": 13000
    },
    {
      "name": "React",
      "price": 25000
    },
    {
      "name": "Node.js",
      "price": 23000
    },
    {
      "name": "C++",
      "price": 22000
    },
    {
      "name": "SQL",
      "price": 17000
    },
    {
      "name": "Ruby",
      "price": 19000
    },
    {
      "name": "PHP",
      "price": 16000
    }
  ]
  );


console.log(`Done Inserting Data`);
