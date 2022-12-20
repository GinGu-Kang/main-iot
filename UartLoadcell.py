from machine import UART, Pin
import time


class UartLoadcell(UART):
    
    def getLoadcellData(self):
        command="Q\r\n"
        while True:
            result=self.uartCommunication(command,2)
        
            print(result)
        
            #숫자가 아닐때 다시함수 호출
            if len(result)==9:
                if(result[1:6].isdigit()):
                    return int(result[1:6])
                else:
                    continue
                
            else:
                continue
        
        
    def uartCommunication(self,command,sleepTime):
        recv=bytes()
        self.write(command)
        time.sleep(sleepTime)
        
        while self.any()>0:
            recv+=self.read(1)
        return recv
    


