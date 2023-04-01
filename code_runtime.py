import editor_compiler as ec



vc = []
vcfunc = []
def compile():
    
    with open("temp.tmp", "r") as f:
        name = f.read()
    scripts = name.split("\n")
    toCompile = []
    for nam in scripts:
        with open(f"projects\\{nam}\\{nam}.ugerc", "r") as f:
            toCompile.append(f.read())

    
    compiled = []
    for i in toCompile:
        compiled.append(ec.compile(i, vc))
    return compiled
    
    
def exce():
    c = compile()
    for d in c:
        for cmd in range(len(d[0])):
            vcfunc[cmd]()



    
