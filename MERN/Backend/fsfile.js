const fs = require("fs")

console.log("starting")

let innertext = "Content of file"
fs.writeFile("nonsync.txt", innertext , () =>{
    console.log("done")
    fs.readFile("nonsync.txt", (error, data) =>{
        console.log(error, data.toString())
    })
})

fs.appendFile("nonsync.txt", "robo", (e, d)=>{
    console.log(d)
})

console.log("ending")