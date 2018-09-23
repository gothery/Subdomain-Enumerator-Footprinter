from dns import resolver
import dns
import os
import csv
errcountA = 0
errcountCNAME = 0
errcountCNAME2 = 0
count = 0
fileLength = 0
list = []
combolist = [['url','A','CNAME','CNAME2']]
print("Starting")


#Must change below for where you have the files
domainNameListFile = "d:/downloads/test.txt"
outputFile = "d:/downloads/subsresolvedtest.csv"

with open (domainNameListFile) as sublist:
    #count lines to allow user to know approximately how long it will take
    for line in sublist:
        if line.strip():
            fileLength += 1
    sublist.seek(0) #go back to beginning

    #check A record, CNAME, 2nd CNAME
    for url in sublist:
        if not url.strip(): continue
        A = ''
        CNAME = []
        CNAME2 = []
        url = url.strip()
        try:
            answer = resolver.query(url, 'A')
            for rdata in answer:
                A = (rdata.address)
        except:
            A = "no IPV4 found"
            errcountA += 1
            pass #using pass vice continue
        try:
            answer = resolver.query(url, 'CNAME')
            for rdata in answer:
                CNAME = rdata.target.to_text()[:-1] #changed to make it a string
        except:
            CNAME = "no CNAME found"
            errcountCNAME += 1
            pass
        try:
            answer = resolver.query(CNAME, 'CNAME')
            for rdata in answer:
                CNAME2 = rdata.target.to_text()[:-1] #changed to make it a string
        except:
            CNAME2 = "no nested CNAMEs"
            errcountCNAME2 += 1
            pass
        list = [url, A, CNAME, CNAME2]
        combolist.append(list)
        count += 1
        print('{}: {} out of {} complete\n'.format(url,count, fileLength))

#use 'wb' vice 'w' for python 2.7
with open(outputFile, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(combolist) #simplified output

print ('There were {} A record errors'.format(errcountA))
print ("There were {} CNAME record errors".format(errcountCNAME))
print ("{} CNAME records are not nested".format(errcountCNAME2))
print("\n")
print("Done")
