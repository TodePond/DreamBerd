match Program
- = {tab | space}
_ = {tab | space | newline}

Program = File { Break File }

File = { Line }

Line = {
    match Explicit | Implicit
    Explicit = Expression - Terminator
    Implicit = todo
}

Terminator = ("!" | "?")+

Expression = {
    match todo
}

Break = {
    match Named | Anonymous
    Anonymous = "=====" {"="}
    Named = Anonymous - Name - [Anonymous]
    Name = any+ ".db"
}
