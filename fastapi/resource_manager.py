''' 모듈 1. 자원 모니터링
1) CPU 사용량 (%)
2) GPU 사용량 (%)
3) 메모리 사용량 (MB)
'''
import datetime
import psutil
import GPUtil
import pandas as pd

class resourceManager:
    def __init__(self):
        self.cpu_list = []
        self.gpu_list = []
        self.timestamp = ''

    def cpu_usg(self):
        self.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # CPU 사용량
        cpu_percent = psutil.cpu_percent()

        # 메모리 사용량 MB
        memory = psutil.virtual_memory()
        used_memory = memory.used / (1024 * 1024)

        value = {
            'timestamps' : self.timestamp,
             'cpu_percentages': cpu_percent,
             'used_memory': used_memory
             }
        
        self.cpu_list.append(value)
        df = pd.DataFrame(self.cpu_list)
        if len(self.cpu_list)> 15:
            self.cpu_list.pop(0) 
        return df
    
    # GPU 사용량
    def gpu_usg(self):
        def add_unit(mem: float) -> str:
            if mem > 1024:
                mem = round(mem / 1024, 2)
                mem = f"{mem}GiB"
            else:
                mem = round(mem, 2)
                mem = f"{mem}MiB"
            return mem
        
        for gpu in GPUtil.getGPUs():
            gpu_id = gpu.id
            gpu_util = gpu.load
            # mem_used = add_unit(gpu.memoryUsed)

        value = {
            'timestamps' : self.timestamp,
            'gpuID' : gpu_id,
            'gpu_percentages' : gpu_util
            }

        self.gpu_list.append(value)
        df = pd.DataFrame(self.gpu_list)
        if len(self.gpu_list)> 15:
            self.gpu_list.pop(0)
        return df