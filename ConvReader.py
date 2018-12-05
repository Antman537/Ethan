from ConvClass import Conv
import re
import sys
from PcapReader import parse

def main():
	#test list with only one smtp line
	#convList = {"keenness": Conv("     11 0.097460       128.187.82.253        23.103.156.74         SMTP     152    C: MAIL FROM:<spf-test@lmcc7ka.test1.keenness.spf-test.internet-measurement.cs.byu.edu>")}
	print("parsing",sys.argv[1])
	convList = parse(sys.argv[1])
	print("parsePCAP complete   ")
	#convList = parseSMTP()
	#print("parseSMTP complete   ")
	parseQuery(convList)
	print("parseQuery complete  ")
	
	evCount = 0 #number of early validations
	lateData = 0 #number of base ev's before data
	dmarcless = 0 #number of ev's w/out dmarcs
	dataEV = 0 #number of ev's without data
	
	noRCPT = 0 #number of conv's without rcpts
	
	dmarc = 0 #number of conv's with dmarcs
	dataDM = 0 #number of dmarc conv's without data
	noRCPTdm = 0 #number of dmarc conv's without RCPT TO
	validateDM = 0 #number of dmarc conv's with validation
	
	
	l2Count = 0 #number of l2's before rcpt
	l2Data = 0 #number of conv with l2 before data
	l2nd = 0 #number of l2's with no data
	l2ndDmarc = 0 #number of l2's with no data but a dmarc
	l2Only = 0 #number of l2's with no rcpt or data
	l2dmarc = 0#number of l2's as above with a dmarc
	
	l3rcpt = 0 #number of l3's before rcpt
	l3data = 0 #number of l3's before data
	l3nd = 0 #number of l3's with no data
	l3ndDmarc = 0 #number of l3's with no data but a dmarc
	l3Only = 0 #number of l3's with no rcpt or data
	l3dmarc = 0 #number of l3's as above with a dmarc
	
	#new vars for sum2
	nol2 = 0 #number of early base queries with no l2
	parallel = 0 #number of parallel validations with data before l2
	parallel2 = 0 #number of parallel validations with data before l3
	lazy = 0 #number of conv's with data, but base or l2 after it
	soft = 0 #number of conv's with DMARC and DATA
	
	#outFile = open("conv_timetable.txt","w")
	sumFile = open("conv_summary.txt","w")
	sum2File = open("conv_sum2.txt","w")
	#compilations of various categories
	noSPF = open("no_spf.txt","w")
	serialSPF = open("serial_spf.txt","w")
	parallelSPF = open("parallel_spf.txt","w")
	lazySPF = open("lazy_spf.txt","w")
	strictDMARC = open("strict_dmarc_spf.txt","w")
	softDMARC = open("soft_dmarc_spf","w")
	#initialize files woth headers
	print("Sender ID\t","Receiver ID\t\t\t","test #\t","Key\t\t","Mail Time\t",
		"Validate Time\t","dmarc Time\t","L2 Time\tL3 Time\t","RCPT Time\t\tData Time",
		file=noSPF)
	print("Sender ID\t","Receiver ID\t\t\t","test #\t","Key\t\t","Mail Time\t",
		"Validate Time\t","dmarc Time\t","L2 Time\tL3 Time\t","RCPT Time\t\tData Time",
		file=serialSPF)
	print("Sender ID\t","Receiver ID\t\t\t","test #\t","Key\t\t","Mail Time\t",
		"Validate Time\t","dmarc Time\t","L2 Time\tL3 Time\t","RCPT Time\t\tData Time",
		file=parallelSPF)
	print("Sender ID\t","Receiver ID\t\t\t","test #\t","Key\t\t","Mail Time\t",
		"Validate Time\t","dmarc Time\t","L2 Time\tL3 Time\t","RCPT Time\t\tData Time",
		file=lazySPF)
	print("Sender ID\t","Receiver ID\t\t\t","test #\t","Key\t\t","Mail Time\t",
		"Validate Time\t","dmarc Time\t","L2 Time\tL3 Time\t","RCPT Time\t\tData Time",
		file=strictDMARC)
	print("Sender ID\t","Receiver ID\t\t\t","test #\t","Key\t\t","Mail Time\t",
		"Validate Time\t","dmarc Time\t","L2 Time\tL3 Time\t","RCPT Time\t\tData Time",
		file=softDMARC)
	
	complete = len(convList) #number of complete conv's (contains a base response or l2)
	
	
	for i in convList:
		c=convList.get(i)
		#c.printConv(outFile)
		if c.earlyValidation()==1 or c.earlyL2() == 1:
			evCount+= 1
			if c.beforeData()==1: 
				if c.l2Time!="unknown":
					parallel+=1
					c.printConv(parallelSPF)
				else:
					nol2+=1
			elif c.l3Test()==1:
				parallel2+=1
				c.printConv(parallelSPF)
		else:
			if c.earlyValidation()==-1 and c.earlyL2()==-1:
				complete = complete-1
				c.printConv(noSPF)
			elif c.beforeData() == 0 and c.l3Test()<2:
				lazy+=1
				c.printConv(lazySPF)
		if c.beforeData() >0:
			lateData+=1
			if c.beforeData()>1:
				l2Data+=1
				c.printConv(serialSPF)
				if c.beforeData()>2:
					l2nd+=1
					c.printConv(serialSPF)
					if c.dmarcTime != "unknown":
						l2ndDmarc+=1
		l3t = c.l3Test()
		if l3t>0:
			l3rcpt +=1
			if l3t>1:
				l3data+=1
				if l3t>2:
					l3nd+=1
					if c.dmarcTime != "unknown":
						l3ndDmarc +=1
		if c.rcptTime == "unknown":
				noRCPT += 1
				if c.l2Time != "unknown" and c.dataTime =="unknown":
					l2Only+=1
					if c.dmarcTime != "unknown":
						l2dmarc +=1
				if c.l3Time != "unknown" and c.dataTime =="unknown":
					l3Only+=1
					if c.dmarcTime != "unknown":
						l3dmarc +=1
					
		if c.dataTime =="unknown":
				dataEV+=1
		if c.earlyL2() == 1:
			l2Count+=1
		
		if c.dmarcTime!="unknown":
			dmarc+=1
			if c.dataTime=="unknown":
				dataDM+=1
				c.printConv(strictDMARC)
			else:
				soft += 1
				c.printConv(softDMARC)
			if c.rcptTime=="unknown":
				noRCPTdm+=1
			if c.validateTime!="unknown" or c.l2Time!="unknown":
				validateDM+=1
		elif c.validateTime!="unknown" or c.l2Time!="unknown":
			dmarcless+=1
	
	#print results
	print("There are",len(convList),"conversations",file=sumFile)
	print("There are",len(convList),"conversations",file=sum2File)
	print((complete/len(convList))*100,"% (",complete,")","of the SMTP transactions had a corresponding base or l2 lookup for test1",
		file=sumFile)
	if complete>0:
		print("\tOf those,",(evCount/complete)*100,"% (",evCount,")","had an l2 or base lookup before the RCPT TO",
			file=sumFile)
		print("\t",(l2Count/complete)*100,"% (",l2Count,")","had an l2 lookup before the RCPT TO",
			file=sumFile)
		print("\t",(lateData/complete)*100,"% (",lateData,")","had an l2 or base lookup before the DATA",
			file=sumFile)
		print("\t",(l2Data/complete)*100,"% (",l2Data,")","had an l2 lookup before the DATA",
			file=sumFile)
		print("\t",(l2nd/complete)*100,"% (",l2nd,")","had an l2 lookup, but no DATA",
			file=sumFile)
		if l2nd>0:
			print("\t\tOf these,",(l2ndDmarc/l2nd)*100,"% (",l2ndDmarc,")","had a corresponding _dmarc",
				file=sumFile)
		print("\t",(l2Only/complete)*100,"% (",l2Only,")","had an l2 lookup, but no RCPT TO or DATA",
			file=sumFile)
		if l2Only>0:
			print("\t\tOf these,",(l2dmarc/l2Only)*100,"% (",l2dmarc,")","had a corresponding _dmarc",
				file=sumFile)
		print("\t",(l3rcpt/complete)*100,"% (",l3rcpt,")","had an l3 lookup before the RCPT TO",
			file=sumFile)
		print("\t",(l3data/complete)*100,"% (",l3data,")","had an l3 lookup before the DATA",
			file=sumFile)
		print("\t",(l3nd/complete)*100,"% (",l3nd,")","had an l3 lookup, but no DATA",
			file=sumFile)
		if l3nd>0:
			print("\t\tOf these,",(l3ndDmarc/l3nd)*100,"% (",l3ndDmarc,")","had a corresponding _dmarc",
				file=sumFile)
		print("\t",(l3Only/complete)*100,"% (",l3Only,")","had an l3 lookup, but no RCPT TO or DATA",
			file=sumFile)
		if l3Only>0:
			print("\t\t Of these,",(l3dmarc/l3Only)*100,"% (",l3dmarc,")","had a corresponding _dmarc",
				file=sumFile)
		print("\t",(dmarcless/complete)*100,"% (",dmarcless,")","had no _dmarc",
			file=sumFile)
		print((noRCPT/len(convList))*100,"% (",noRCPT,")","of the SMTP transactions had no RCPT TO",
			file=sumFile)
		print((dataEV/len(convList))*100,"% (",dataEV,")","of the SMTP transactions had no DATA",
			file=sumFile)
			
	print((dmarc/len(convList))*100,"% (",dmarc,")","of the SMTP transactions had a corresponding _dmarc lookup",
		file=sumFile)
	if dmarc>0:
		print("\tOf those,",(dataDM/dmarc)*100,"% (",dataDM,")","had no DATA",
			file=sumFile)
		print("\t",(noRCPTdm/dmarc)*100,"% (",noRCPTdm,")","had no RCPT TO",
			file=sumFile)
		print("\t",(validateDM/dmarc)*100,"% (",validateDM,")","had base or l2 lookup for test1",
			file=sumFile)
			
	#print sum2
	length = len(convList)
	print("No spf validation:",file = sum2File)
	print("\t",(length-complete)/length*100,"% (",(length-complete),") had no base or l2 queries detected",
		file=sum2File)
	print ("Serial SPF Validation:",file=sum2File)
	print("\t",((l2Data-l2nd)/length)*100,"% (",l2Data-l2nd,") had an l2 lookup before DATA",
		file=sum2File)
	print ("\t",(l2nd/length)*100,"% (",l2nd,") had an l2 lookup, but no DATA",
		file=sum2File)
	print("Parallel SPF Validation:",file = sum2File)
	print("\tAfter an early base response,",file = sum2File)
	print ("\t",(parallel/length)*100,"%  (",parallel,") had an l2 query after the DATA",
		file=sum2File)
	print ("\t",(parallel2/length)*100,"%  (",parallel2,") had an l3 query after the DATA",
		file=sum2File)
	print ("\t",(nol2/length)*100,"%  (",nol2,") had no l2",
		file=sum2File)
	print("Lazy SPF Validation:",file = sum2File)
	print ("\t",(lazy/length)*100,"%  (",lazy,") had a base query or l2 after the DATA",
		file=sum2File)
	print("SPF validation with strict DMARC adherence:",file = sum2File)
	print ("\t",(dataDM/length)*100,"%  (",dataDM,") had a DMARC query and no DATA",
		file=sum2File)
	print("SPF validation with soft DMARC:",file = sum2File)
	print ("\t",(soft/length)*100,"%  (",soft,") had a DMARC query and DATA",
		file=sum2File)
	
		
def parseQuery(convList):
	f = open("dns-query-logs-minimal.txt")
	l = f.readlines()
	ln = 0
	for x in l:
		print("\rparsing line",ln,end='\r')
		ln +=1
		m = re.search(RE_ULTIMATE,x)
		if m is not None:
			#convert to list of strings; not actually necessary
			#counter = 0
			#log_elements = []
			#while counter < 13:
			#	log_elements.append(m.group(counter))
			#	counter += 1

			if m[8] == "test1":
				c = convList.get(m[9])
				if c is not None:
					#if this is the l2 message
					if m[6] == "l2" and c.l2Time == "unknown":
						c.l2Time = m[1]
						#c.printConv(None)
					if m[6] =="l3" and c.l3Time =="unknown":
						c.l3Time = m[1]
						#c.printConv(None)
					if m[2] is not None:
						c.dmarcTime = m[1]
						#c.printConv(None)
					else:
						#if no other message has yet been received 
						if c.validateTime == "unknown":
							c.validateTime = m[1]
							#c.printConv(None)
		
def parseSMTP():
	f = open("dataset.txt","r")
	l = f.readlines()
	cList = {}
	ln = 0
	for x in l:
		print("\rparsing line",ln,end='\r')
		ln += 1
		#print(x)
		if x.find('MAIL FROM') != -1:
			#create new Conv object
			tmp = Conv(x)
			#tmp.printConv()
			if tmp.test == "test1":
				cList[tmp.key]= tmp
		else:
			if x.find('RCPT TO') != -1:
				#update Conv object with rcptTime
				tmp2 = x.split()
				for i in cList:
					if cList[i].isConv(tmp2[2],tmp2[3]):
						cList[i].rcptTime = tmp2[1]
						#cList[i].printConv()
						break
			else:
				if x.find('DATA') !=-1:
					tmp3 = x.split()
					for j in cList:
						if cList[j].isConv(tmp3[2],tmp3[3]):
							cList[j].dataTime = tmp3[1]
							break
	return cList
	


#Grouping: 1 = recorded decimal time | 2 = _dmarc | 3 = _\w+ | 4 = _\w+ | 5 = the group that six is in | 6 = l#. | 7 = endcoded time stamp
#8 = test## | 9 = generated name | 10 = #00ms | 11 =  | 12 = Record look-up type			
RE_ULTIMATE = re.compile(r'(\d+\.\d+)\s(_dmarc\.)?(\w+[^\d+]\.|x\.|m5\.)?(\w+[^\d+]\.)?((l\d+|a|b)\.)?([^\.|\s]+)\.(test\d+)\.([^\.]+)\.spf-test\.(\d00ms\.)?internet-measurement\.cs\.byu\.edu([^\s]+)?\s(\w+)', re.IGNORECASE)
			
if __name__ == "__main__":
	main()