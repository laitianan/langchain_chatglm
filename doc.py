class Doc():
    def __init__(self,funtion_id,name,score=0.0,fro="SEARCH"):

        self.funtion_id=funtion_id
        self.name=name
        self.score=score
        self.fro=fro
    def __eq__(self, other):
        h1 =self.__str__()
        h2 = other.__str__()
        return h1 == h2
    def __hash__(self):
        h=self.__str__()
        return hash(h)  # 如果直接写为hash(self)则会导致递归
    def __str__(self):
        h = f"name:{self.name},funtion_id:{self.funtion_id}"
        return h