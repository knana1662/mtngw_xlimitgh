
from datetime import datetime, timedelta
import sched
from threading import Thread
from time import sleep,time
from os import remove,getenv
from requests import post,exceptions
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


UNIFI_USERNAME=getenv("UNIFI_USERNAME")
UNIFI_PASSWORD=getenv("UNIFI_PASSWORD")



def write(write):
    def txt_file(*args,**kwargs):

        data=write(*args,*kwargs)
        if Path(f".\{write.__name__}.txt").exists() ==True:
            remove(f".\{write.__name__}.txt")

        if type(data) == dict:
            keys=data.keys()
            values=data.values()

            with open(f".\{write.__name__}.txt","a+",encoding="utf-8") as file:

                for idx,data in enumerate(zip(keys,values)):
                    KEYS,VALUES=data
                    # file.write(f"{data}\n\n")
                    print(f"dict: {KEYS}--{VALUES}")
                    file.write(f"{KEYS}--{VALUES}\n\n")
                return data
            
        elif type(data) == str:
            print(f"str: {data}")
            ...

            with open(f".\{write.__name__}.txt","a+",encoding="utf-8") as file:
                file.write(f"{data}\n\n")
                return data    

        elif type(data) == int:
            print(f"int: {data}")
            ...

            with open(f".\{write.__name__}.txt","a+",encoding="utf-8") as file:
                file.write(f"{data}\n\n")
                return data    

        elif type(data) == list:
            print(f"list: {data}")

            ...

            with open(f".\{write.__name__}.txt","a+",encoding="utf-8") as file:
                for idx,data in enumerate(data):
                    file.write(f"{data}\n\n")
                return data    



    return txt_file


def login(data):
    from core import timeout

    @write
    def wrapper(*args, **kwargs):
        LOGIN_KEYS = data(*args, **kwargs)

        username=LOGIN_KEYS["username"]
        password=LOGIN_KEYS["password"]

        if type(LOGIN_KEYS)==dict:
            
            if LOGIN_KEYS["login"].lower() == "unifi":
                try:
                    with post(url="http://127.0.0.1:8080/api/login",json ={"username": username,"password": password,"remember": True,"strict": True},timeout=timeout) as unifiAPI:
                        if unifiAPI.status_code != 200:
                            print(f" Unifi Login Failed 🔴 \t{unifiAPI.text}")
                        else:
                            # GENERATE VOUCHER CODES
                            configure_unifiAPI=unifiAPI.headers["Set-Cookie"].split(";")
                            unifises=configure_unifiAPI[0]
                            csrf_token=configure_unifiAPI[2].split(",")[1]
                            set_cookie=(f"{unifises}; {csrf_token}")

                            unifiAPI.headers.pop("Set-Cookie")

                            unifiAPI.headers.update({"Cookie":set_cookie,"X-Csrf-Token":(csrf_token).replace("csrf_token=","").strip()})

                            LOGIN_KEYS.update({"headers":unifiAPI.headers})
                            return LOGIN_KEYS

                except exceptions.ConnectionError:
                    ...
                    print("Connection Error!")


            elif  LOGIN_KEYS["login"].lower() == "cambium":
                try:
                    print()
                except exceptions.ConnectionError:
                    ...
         
    return wrapper

def data_purchasing(data):
    # @write
    def wrapper(*args,**kwargs):
        
        pay=data(*args,**kwargs)
        print({"type":type(pay)})
        default_data_bundle = 340.29
        pay,default_data_bundle = pay.values() if type(pay) == dict else (pay[0],pay[1]) if type(pay) == tuple else (pay,default_data_bundle) if type(pay) == int else (0,0)

        print(pay,default_data_bundle)
        store_data_allocations=[]
        calc=lambda pay,percent: round(pay/3 *default_data_bundle*rate_deductions(percent)*100,2)
        rate_deductions=lambda percent:percent/100
        length_checker = lambda check_value: "MB" if len(f"{int(check_value)}") <= 3 else "GB"


        if type(pay)==list:

            for idx,pay in enumerate(pay):
                ...
                if pay >=3 and pay <=10:
                    ... 
                    # print(calc(pay,1))

                    

                    # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                    # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                    store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    
            
                elif pay >=11 and pay <=20:
                    ...
                    
                    # print(calc(pay,1))

                    # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                    # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                    store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    

                elif pay>20 and pay<=50:
                    ...
                    
                    # print(calc(pay,1))

                    # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                    # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                    store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    

                elif pay >50 and pay <=100:
                    ...
                    
                    # print(calc(pay,1))

                    # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                    # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                    store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    

                elif pay>100 and pay<=200:
                    ...
                    
                    # print(calc(pay,1))

                    # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                    # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                    store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    

                elif pay >200 and pay <=300:
                    ...
                    
                    # print(calc(pay,1))

                    # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                    # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                    store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    
        
                elif pay>300 and pay<500:
                    ...
                    
                    # print(calc(pay,1))

                    # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                    # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                    store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    


            
            return store_data_allocations
        elif type(pay)==int:
            if pay >=3 and pay <=10:
                ...
                
                # print(calc(pay,1))
                # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    
        
            elif pay >=11 and pay <=20:
                ...
                
                # print(calc(pay,1))
                # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    

            elif pay>20 and pay<=50:
                ...
                
                # print(calc(pay,1))
                # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    

            elif pay >50 and pay <=100:
                ...
                
                # print(calc(pay,1))
                # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    

            elif pay>100 and pay<=200:
                ...
                
                # print(calc(pay,1))                
                # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    

            elif pay >200 and pay <=300:
                ...
                
                # print(calc(pay,1))
                # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    

            elif pay>300 and pay<500:
                ...
                
                # print(calc(pay,1))
                # store_data_allocations.append(f"GHC {pay} is equal to {calc(pay,1)} {length_checker(calc(pay,1))}")    
                # store_data_allocations.append(f"{pay}_GHS__{calc(pay,1)}{length_checker(calc(pay,1))}")    
                store_data_allocations.append(f"{pay}_GHS__{round(calc(pay,1)/1000,2) if length_checker(calc(pay,1)) =='GB' else calc(pay,1)}{length_checker(calc(pay,1))}")    
            
            return store_data_allocations


        
        return store_data_allocations
    return wrapper


def optimization_timer(func):
    def start_optimization_timer(*args,**kwargs):
        start_time = time()  # Start timing
        result = func(*args, **kwargs)  # Call the original function
        end_time = time()  # End timing
        execution_time = end_time - start_time

        # output_data = f"\n[{func.__name__}] : [{execution_time:.6f}s]\n"
        output_data = f"\n[{func.__name__}] : [{timedelta(seconds=execution_time)}s]\n"
        print(output_data) #*

        if f"{func.__name__}" == "admin_interface_signal": #*
            ... #*
            with open(f"{BASE_DIR}/optimization_timer.txt","+a") as store: #*
                store.write(output_data) #*
                
        return result
    return start_optimization_timer


def set_background_scheduler(schedule_dictionary:dict)->dict:
    
    """
    -- set the return to a dictionary containing in this format:\n
        1. dict(delay="0",priority="0",data="Hello World")\n.
        Example:\n
            1.   return {"delay":2,"priority":1,"data":(lambda :print(123445))()}

    """

    def get_background_scheduler(*args,**kwargs):
        execute_bg_scheduler = sched.scheduler(time, sleep)
        kwargs=schedule_dictionary(*args,**kwargs)
        print(kwargs)

        try:
            execute_bg_scheduler.enter(delay=kwargs["delay"],priority=kwargs["priority"],action=kwargs["data"] if callable(kwargs["data"])==True else (lambda :print(kwargs["data"])))
            T=Thread(target=execute_bg_scheduler.run,name="fourminutescountdowntimer",daemon=True) #*
            T.start() #*        
        
        except TypeError: 
            ...
        except RecursionError:
            ...
            print("RecursionError :( Limit Exceeded!!! ) - Please Try Again")
            execute_bg_scheduler.enter(delay=kwargs["delay"],priority=kwargs["priority"],action=kwargs["data"] if callable(kwargs["data"])==True else (lambda :print(kwargs["data"])))
            T=Thread(target=execute_bg_scheduler.run,name="fourminutescountdowntimer",daemon=True) #*
            T.start() #*
            
    return get_background_scheduler

def execute_task_within_this_period(function_to_execute,days: float = 1,seconds: float = 0,microseconds: float = 0,milliseconds: float = 0,minutes: float = 0,hours: float = 0,weeks: float = 0):
    ...
    futureDate = datetime.now() + timedelta(days,seconds,microseconds,milliseconds,minutes,hours,weeks)

    while 1:
        try:
            currentDate = datetime.now()
            remaining_time = futureDate - currentDate
            delta = remaining_time
            total_seconds = remaining_time.total_seconds()
            seconds = remaining_time.seconds

            if int(total_seconds) == 0 :
                ...
                function_to_execute()
                execute_task_within_this_period(function_to_execute = function_to_execute ,days = days ,seconds = seconds ,microseconds = microseconds ,milliseconds = milliseconds ,minutes = minutes ,hours = hours ,weeks = weeks )
            else:
                ...
                print(total_seconds,function_to_execute.__dict__)

        except RecursionError:
            ...
            execute_task_within_this_period(function_to_execute = function_to_execute ,days = days ,seconds = seconds ,microseconds = microseconds ,milliseconds = milliseconds ,minutes = minutes ,hours = hours ,weeks = weeks )
        sleep(1)

if __name__=="__main__":



    # def set_background_test_scheduler(schedule_dictionary:dict)->dict:
        
    #     """
    #     -- set the return to a dictionary containing in this format:\n
    #         1. dict(delay="0",priority="0",data="Hello World")\n.
    #         Example:\n
    #             1.   return {"delay":2,"priority":1,"data":(lambda :print(123445))()}

    #     """

    #     def get_background_test_scheduler(**kwargs):
    #         execute_bg_scheduler = sched.scheduler(time, sleep)
    #         kwargs=schedule_dictionary(**kwargs)
    #         print(kwargs["data"].__name__)
    #         try:
    #             execute_bg_scheduler.enter(delay=kwargs["delay"],priority=kwargs["priority"],action=kwargs["data"] if callable(kwargs["data"])==True else (lambda :print(kwargs["data"])))
    #             execute_bg_scheduler.run() #*
    #         except RecursionError:
    #             print("RecursionError :( Limit Exceeded!!! ) - Please Try Again")
    #             # execute_bg_scheduler.enter(delay=kwargs["delay"],priority=kwargs["priority"],action=kwargs["data"] if callable(kwargs["data"])==True else (lambda :print(kwargs["data"])))
    #             execute_bg_scheduler.enter(delay=60,priority=kwargs["priority"],action=kwargs["data"] if callable(kwargs["data"])==True else (lambda :print(kwargs["data"])))
    #             execute_bg_scheduler.run() #*
    #         except TypeError:
    #             ...
    #     return get_background_test_scheduler



    # @set_background_test_scheduler
    # def test():
    #     ...
    #     if 11==1:
    #         ...
    #         print(123)
    #     else:
    #         return {"delay":1,"priority":1,"data":test}

    # test()


    # @write
    # @data_purchasing
    # def data():
    #     ...
    #     # return ([3,5,10,15,20,30,50],7.29)
    #     # return {"price":[3,5,10,15,20,30,50],"base_price":500}

    #     return ([3,5,10,15,20,30,50],600)
    #     # return ([3,5,10,15,20,30,50],340.29)
    #     # return {"price":[3,5,10,15,20,30,50],"base_price":500}

    # # data()
    # # print(data())
    # # print(type(" ".join([y for x,y in enumerate(data())])))
    # print(" ".join([y for x,y in enumerate(data())]))




    
    @data_purchasing
    def data():
        ...
        return {"x":[300],"y":340}
    print(data())

    @data_purchasing
    def data():
        ...
        return ([3,6,9,67],340)
    print(data())

    @data_purchasing
    def data():
        ...
        return 300
    print(data())


    @data_purchasing
    def data():
        ...
        return ([3,5,10,15,30],2000)
    print(data())
