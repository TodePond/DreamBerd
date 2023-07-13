match Program
_ = {tab | space}

Program = File { Break File }

File = {
    match Expression
}

Break = {
    match Named | Anonymous
    Anonymous = "=====" {"="}
    Named = Anonymous _ Name _ [Anonymous]
    Name = any+ ".db"
}
