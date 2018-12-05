import logging
from ConvClass import Conv
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
from kamene.all import *
'''
in: string filename
out: 
'''
def parse(filename):
	cList = {}
	with PcapReader(filename) as pcap_reader:
		ports = [80,25]
		ln=0
		for pkt in pcap_reader:
			print("\rparsing line",ln,end='\r')
			ln+=1
			if TCP in pkt and (pkt[TCP].sport in ports or
					pkt[TCP].dport in ports):
				#if the pkt is part of a smtp conversation
				x = (str(pkt.time)+" "+pkt.sprintf("%IP.src%")+" "+
					pkt.sprintf("%IP.dst%")+" "+pkt.sprintf("%TCP.load%"))
				#print(x)
				'''print(pkt.time,pkt.sprintf("%IP.src%"),
					pkt.sprintf("%IP.dst%"),pkt.sprintf("%TCP.load%"),file=dataset)'''
				
				if x.find('MAIL FROM') != -1:
					#create new Conv object
					#print(x)
					tmp = Conv(x)
					if tmp.test == "test1":
						cList[tmp.key]= tmp
				else:
					if x.find('RCPT TO') != -1:
						#update Conv object with rcptTime
						tmp2 = x.split()
						for i in cList:
							if cList[i].isConv(tmp2[1],tmp2[2]):
								cList[i].rcptTime = tmp2[0]
								#cList[i].printConv(None)
								break
					else:
						if x.find('DATA') !=-1:
							#update Conv object with dataTime
							tmp3 = x.split()
							for j in cList:
								if cList[j].isConv(tmp3[1],tmp3[2]):
									cList[j].dataTime = tmp3[0]
									break
									
	return cList