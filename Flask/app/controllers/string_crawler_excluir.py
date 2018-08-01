frase = """class SVM:
    def __init__(self):
        pass

    def sub(self, <<abacate>>,<<b>>):
        c = a - b
        return c

    def sum(self, <<trelo>>, <<cebolinha>>):
        c = a + b + a +b + b + a + b
        return c"""

print(frase)
tamanho = len(frase)
param = []

i = 0
for i in range(0,tamanho):
    if frase[i] == "<":
        if frase[i+1] == "<":
            j=i+2
            for j in range(j, tamanho):
                if frase[j] == ">":
                    if frase[j + 1] == ">":
                        new = ""
                        for c in range(i+2, j):
                            new += frase[c]
                        param.append(new)
                        break

for p in param:
    print(p)

frase2=["param1", "param2", "param3", "param4"]
for p in param:
    frase = frase.replace("<<" + str(p) + ">>", frase2[1])

print(frase)



