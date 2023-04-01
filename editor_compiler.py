
def compile(text, func_names):

    import time

    #Return vars
    valid_cmds = []
    invalid_cmds = []
    
    toCompile = text.split("\n")
    for ig in range(len(toCompile)):
        i = toCompile[ig]
        selfindex = toCompile.index(i)
        
        for o in func_names:
            if o in i:
                if i.index(o) == 0:
                    valid_cmds.append(i+";"+str(func_names.index(i)))
                else:
                    invalid_cmds.append(i)
    return valid_cmds, invalid_cmds
                    


if __name__ == "__main__":
    def test1():
        print("called1")
    def test2():
        print("called2")
    t = "rrff\nege\nrff\nege"
    func = ["ege", "rff"]
    funcs = [test1, test2]
    vcmp, icmp = compile(t, func)
    for i in vcmp:
        funcs[vcmp.index(i)]()
