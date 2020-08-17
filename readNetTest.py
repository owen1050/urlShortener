import matplotlib.pyplot as plt
from time import gmtime, strftime

class StringUtil:
    dataArray = []
    def __init__(self, string):
        lines= string.split("\n")

        for line in lines:
            try:
                datafield = line.split("\t")
                lineDataTemp = []
                for data in datafield:
                    dat = data.split(":")
                    lineDataTemp.append(dat[1])
                self.dataArray.append(lineDataTemp)
            except:
                pass


filename = "pingTestDay3.txt"

f = open(filename, "r")
text = f.read()
f.close()


su = StringUtil(text)

i1 = text.find("\n")
print(text[0:i1])
last10Avg = []
time = []
x = []
i = 0
for line in su.dataArray:
    dat = float(line[6])
    print(dat)
    last10Avg.append(dat)
    x.append(i)
    i = i + 1
print(len(last10Avg))
plt.scatter( x, last10Avg)
plt.show()


