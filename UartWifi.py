from machine import UART, Pin
import time

class UartWifi(UART):
    def __init__(self,id,baudrate,ssid,password,connectId,addr,port):
        super().__init__(id,baudrate)
        self.ssid=ssid
        self.password=password
        self.connectId=connectId
        self.addr=addr
        self.port=port
        self.CRLF='\r\n'
    
    def apConnect(self):
        while True:
            #보내기전에 와이파이연결되어있나 확인
            isConnect=self.apConnectCheck()
            
            if isConnect==False:
                print("No connection")
                connectCommand='AT+CWJAP="'+self.ssid+'","'+self.password+'"'+self.CRLF
                print(self.uartCommunication(connectCommand,5))
                time.sleep(10)
            else:
                print("Connection success")
                break
                
            
    def apConnectCheck(self):
        connectCheckCommand="AT+CWJAP?"+self.CRLF
        response=self.uartCommunication(connectCheckCommand,2)
        print(response)
        return b''+self.ssid in response
        
        
    def uartCommunication(self,command,sleepTime):
        recv=bytes()
        self.write(command)
        time.sleep(sleepTime)
    
        while self.any()>0:
            recv+=self.read(1)
        return recv
    
    def sendDataByTCP(self,sendData,Mode="TCP"):
        self.apConnect()
        
        #멀티 모드
        command=bytes()
        command="AT+CIPMUX=1"+self.CRLF
        res=self.uartCommunication(command,0.1)
        print(res)
        

        #tcp socket 연결
        command='AT+CIPSTART='+str(self.connectId)+',"'+Mode+'","'+self.addr+'",'+str(self.port)+self.CRLF
        res=self.uartCommunication(command,3)
        print(res)
        if "CONNECT" not in res:
            return False
        

        #send할 길이 정하기
        command="AT+CIPSEND=0,"+str(len(sendData))+self.CRLF
        res=self.uartCommunication(command,0.1)
        print(res)
        

        #send데이터 입력
        command=sendData
        print(sendData)
        res=self.uartCommunication(command,0.1)
        print(res)
        
        #연결종료
        command="AT+CIPCLOSE"+self.CRLF
        res=self.uartCommunication(command,0.1)
        print(res)
        
        return True

