class Conv:
	
	
	def __init__(self,input):
		tmp = input.split()
		self.mailTime = tmp[0]
		self.sender = tmp[1]
		self.receiver = tmp[2]
		self.parseBody(tmp[4])
		self.rcptTime = "unknown"
		self.validateTime = "unknown"
		self.dmarcTime = "unknown"
		self.l2Time = "unknown"
		self.l3Time = "unknown"
		self.dataTime = "unknown"
		
		#print(tmp[0],tmp[1],tmp[2],tmp[3])
		
	def parseBody(self,input):
		tmp = input.split('.')
		if len(tmp) >= 3:
			self.test = tmp[1]
			self.key = tmp[2]
		else:
			self.test = "unknown"
			self.key = "unknown"
	
	def isConv(self,sender,receiver):
		if self.sender == sender and self.receiver == receiver:
			return True
		else:
			return False
	
	def earlyValidation(self):
		if self.validateTime == "unknown":
			return -1
		if self.rcptTime=="unknown" or self.validateTime < self.rcptTime:
			return 1
		else:
			return 0
			
	def earlyL2(self):
		if self.l2Time == "unknown":
			return -1
		if self.rcptTime=="unknown" or self.l2Time < self.rcptTime:
			return 1
		else:
			return 0	
	
	def beforeData(self):
		out = 0
		if self.validateTime!="unknown" and self.validateTime<self.dataTime:
			out = 1
		if self.l2Time!="unknown" and self.l2Time<self.dataTime:
			out = 2
			if self.dataTime == "unknown":
				out = 3
		return out
	
	def l3Test(self):
		out = 0
		if self.l3Time != "unknown":
			if self.rcptTime == "unknown" or self.l3Time<self.rcptTime:
				out = 1
			if self.dataTime == "unknown" or self.l3Time<self.dataTime:
				out = 2
			if self.dataTime == "unknown":
				out = 3
		return out
	
	def printConv(self,writeFile):
		if writeFile is None:
			print("Sender ID\t","Receiver ID\t\t\t","test #\t","Key\t\t","Mail Time\t",
		"Validate Time\t","dmarc Time\t","L2 Time\tL3 Time\t","RCPT Time\t\tData Time")
			print(self.sender,"\t",self.receiver,"\t\t\t",self.test,"\t",self.key,"\t",
				self.mailTime,"\t",self.validateTime,"\t",self.dmarcTime,"\t",self.l2Time,"\t",self.l3Time,
				"\t",self.rcptTime,"\t",self.dataTime)
		else:
			print(self.sender,"\t",self.receiver,"\t\t\t",self.test,"\t",self.key,"\t",
				self.mailTime,"\t",self.validateTime,"\t",self.dmarcTime,"\t",self.l2Time,"\t",self.l3Time,
				"\t",self.rcptTime,"\t",self.dataTime,file=writeFile)