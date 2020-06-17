import datetime
def TryParse(value):
    try:
        value = float(value)
        if str(value).endswith('.0'):
            return int(value)
        else:
            return float(value)
    except ValueError:
        return str(value)
class redis:
    def __init__(self):
        self.dict_redis={}
        self.flag=True

    def RPUSH(self,*args):
        if not self.EXISTS(args[0]):
            valList=[]
            self.SET(args[0],valList)
        valList=self.GET(args[0])
        valList.append(args[1])
        self.SET(args[0],valList)
        return "OK"

    def RPOP(self,*args):
        if not self.EXISTS(args[0]):
            return None
        valList=self.GET(args[0])
        if len(valList) > 0:
            val=valList.pop()
        return val
    
    def LPUSH(self,*args):
        if not self.EXISTS(args[0]):
            valList=[]
            self.SET(args[0],valList)
        valList=self.GET(args[0])
        valList.insert(0,args[1])
        self.SET(args[0],valList)
        return "OK"

    def LRANGE(self,*args):
        if not self.EXISTS(args[0]):
            return None
        valList=self.GET(args[0])
        return valList[args[1]:args[2]]
        
    def LLEN(self,*args):
        if not self.EXISTS(args[0]):
            return None
        valList=self.GET(args[0])
        return len(valList)
        
    def LPOP(self,*args):
        if not self.EXISTS(args[0]):
            return None
        valList=self.GET(args[0])
        if len(valList) > 0:
            val=valList.pop(0)
        return val
    
    def SET(self,*args):
        if not self.dict_redis.get(args[0],None):
            self.dict_redis[args[0]]={}
        self.dict_redis[args[0]]["value"]=args[1]
        self.PERSIST(args[0])
        if len(args) > 2 and args[2] == "EX":
            self.EXPIRE(args[0],args[3])
        return "OK"

    def GET(self,*args):
        rec= self.dict_redis.get(args[0],None)
        if rec != None:
            self.TTL(args[0])
        rec= self.dict_redis.get(args[0],None)
        if not rec:
            return None
        else:
            return rec.get("value",None)
        
    def EXISTS(self,*args):
        rec= self.dict_redis.get(args[0],None)
        if rec == None:
            return False
        else:
            return True
        
    def DEL(self,*args):
        self.dict_redis.pop(args[0])
        return "OK"

    def INCR(self,*args):
        return self.INCRBY(args[0],1)
            

    def DECR(self,*args):
        return self.DECRBY(args[0],1)
        
    def INCRBY(self,*args):
        val= self.GET(args[0])
        if isinstance(val, (float, int)):
            self.SET(args[0],val+args[1])
            return self.GET(args[0])
        return "ERROR"
        
    def DECRBY(self,*args):
        val= self.GET(args[0])
        if isinstance(val, (float, int)):
            self.SET(args[0],val-args[1])
            return self.GET(args[0])
        return "ERROR"

    def TTL(self,*args):
        rec=self.dict_redis.get(args[0],None)
        if not rec :
            return -2
        ttl=rec["ttl"]
        if ttl == -1:
            return -1
        validTo = rec["validTo"]
        if datetime.datetime.now() > validTo:
            self.DEL(args[0])
            return -2
        return (validTo - datetime.datetime.now()).total_seconds() * 1000
        

    def EXPIRE(self,*args):
        self.dict_redis[args[0]]["validTo"] = datetime.datetime.now() +  datetime.timedelta(milliseconds=args[1])
        self.dict_redis[args[0]]["ttl"]=args[1]
        return "OK"
        
    def PERSIST(self,*args):
        self.dict_redis[args[0]]["validTo"]=datetime.datetime.now()
        self.dict_redis[args[0]]["ttl"]=-1
        return "OK"
        
    def QUIT(self,*args):
        self.flag = False

redis_obj=redis()
while redis_obj.flag==True:
    instr=raw_input()
    tokens=instr.split(' ')
    cmd=tokens[0]
    for i,token in enumerate(tokens):
        tokens[i]=TryParse(token)
    args=tokens[1:]
    try:
        print eval('redis_obj.'+cmd)(*args)
    except:
        print redis_obj.QUIT()
