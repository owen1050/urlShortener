import subprocess, time

pings = 0
timeout = 0
totalPing = 0
avgPing = 0
last10 = 0
ip = "8.8.8.8"
printEvery = 100
maxPing = 0
maxLast10 = 0
lastTotalPing = 0
pingsOver100 = 0

while True:
    
    a = str(subprocess.run("ping -c 1 " + ip,shell = True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE))
   # print(a)
    if a.find("timed out") > 0:
        timeout = timeout + 1
        print("timeout")
    else:
        pings = pings + 1
        i0 = a.find("time=") + 5
        i1 = a.find("ms", i0)-1
        cp = float(a[i0:i1])
        totalPing = totalPing + cp

        if cp > 100:
            pingsOver100 = pingsOver100 + 1
        if cp > maxLast10:
            maxLast10 = cp
        if cp > maxPing:
            maxPing = cp
        
    if pings % printEvery == 0:
        last10Ping = (totalPing - lastTotalPing) / printEvery
        avgPing = totalPing/pings
        packetLoss = (timeout/pings) * 100
        f = open("newModemPingTest2.txt", "a")
        summary = "time:" + str(time.time()) + "\tIP:"+ ip+ "\ttotalPings:"+ str(pings)+ "\tavgPing:"+ '{0:3.1f}'.format(avgPing)+ "\tmaxPing:"+ str(maxPing)+ "\tlast10Avg:"+ '{0:3.1f}'.format(last10Ping)+ "\tlast10Max:"+ str(maxLast10)+ "\tpingsOver100:"+ str(pingsOver100) + "\tpercentageOfPingsOver100:" + str('{0:3.1f}'.format(100*(pingsOver100/pings)))+ "%\ttimeout:"+ str(timeout)+ "\tpacketLoss:"+ str('{0:3.1f}'.format(packetLoss)) + "%\n"
        print(summary)
        f.write(summary)
        f.close()
        maxLast10 = 0
        lastTotalPing = totalPing
    time.sleep(0.005)
    
