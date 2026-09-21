import fs from "fs/promises"

let a = await fs.readFile("nonsync.txt")

let b = await fs.appendFile("nonsync.txt", "\n\n\n\nthis is amazing")
console.log(a.toString(), b)