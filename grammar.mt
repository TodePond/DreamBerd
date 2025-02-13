
//======
let _ = Primitive.Whitespace
let - = Primitive.Gap

let Primitive = {
    let Space = " "
    let Tab = "	"
    let LineBreak = "\n"

    let Gap = {Tab | Space}
    let Whitespace = {Gap | LineBreak}
}

//======
match Program
let Program = File 

let Break = {
    match Named | Anonymous
    
    let Anonymous = "=====" {"="}
    let Named = Anonymous - Name - [Anonymous]
    
    let Name = any+ ".db"
}

//=== FILE ===
let File = {
    match {Statement.Loose _} Statement.Strict
}

//=== STATEMENT ===
let Statement = {
    let Loose = todo
    let Strict = todo
    
    let Declaring = Declaration - Terminator
    let Expressing = Expression - Terminator
    let Controlling = Control
    let Emailing = Email

    let Terminator = ("!" | "?”)+
}
