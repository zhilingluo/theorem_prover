from datetime import datetime
import json
import atexit
from pathlib import Path


class DataCollector():
    def __init__(self):
        self.ls = []
        current_time = datetime.now()

        # 格式化时间字符串，例如：2025-01-14_16-14-30
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

        # 创建文件名

        file_name = f"collects/report_{formatted_time}.txt"
        self.file_name =  Path.cwd().joinpath(file_name)
        print(f"Generated file name: {file_name}")
        self.counter=0
        atexit.register(self.flush)
    def log(self,**kwargs):
        self.ls.append(dict(kwargs))
        self.counter+=1
        if self.counter%100==0:
            self.flush()

    def flush(self):
        with open(self.file_name,'w') as file:
            json.dump(self.ls,file,indent=4)

    #def __del__(self):
    #    self.flush()
if __name__=='__main__':
    dc = DataCollector()
    dc.log(aa=123,bb="a",cc=True)
    #dc.flush()
