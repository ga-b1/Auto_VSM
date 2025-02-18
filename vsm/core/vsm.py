from process import Process 


class vsm:
    def __init__(self):
        self.process_list: list[Process]
        
    def add_process(self,process: Process):
        
        #TODO add test
        print("process ajouter")
        
        self.process_list.append(process)