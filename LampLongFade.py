
import asyncio
import json
import time
import copy
import json
import humanize
import datetime as dt
from datetime import datetime

from tapo import ApiClient

def out(text):
    print("%s: %s" %(datetime.now().strftime("%H:%M:%S"), text))

def getValuesSchedule(start_brightness: int, end_brightness: int, time_span: float):
    """ returns tuple with:
            array with sleep times (in seconds) before setting the next brightness value
            array with brightness values for a linear fade/interpolation between "from" and "to" brightness values

    Args:
        start_brightness (int): starting brightness value
        end_brightness (int): final brightness value
        time_span (float): minutes
    """

    #calculate slope
    t0 = 0
    tf = round(time_span * 60)
    
    b0 = start_brightness
    bf = end_brightness    
    
    m = (bf - b0) / (tf - t0)
                
    t_array = list(range(1, tf, 1))
    t_array.append(tf)
    
    b_array = []    
    for t in t_array:
        b = m * t + b0
        b_array.append(round(b))
        
    #avoid sending the same brightness multiple times by removing contiguous values
    prev_value = -1
    index = 0
    while index < len(b_array):
        value = b_array[index]
        
        if value == prev_value:
            b_array.pop(index)
            t_array.pop(index)  
            index = 0  
            prev_value = -1
        else:
            index += 1  
            prev_value = value
                  
    
    #calculate time intervals between each point (time, brightness) into ts_array
    ts_array = copy.deepcopy(t_array)
       
    index = len(ts_array)-1
    while index > 0:
        ts_array[index] = ts_array[index] - ts_array[index-1]
        index -= 1
    
    return (ts_array, b_array)

async def longFade(client:ApiClient, lamp_ip:str, start_brightness:int, end_brightness:int, time_span:float):
    """ creates a fade effect 

    Args:
        client (ApiClient): API client to control the lamp
        client (str): API client to control the lamp
        start_brightness (int): starting brightness value
        end_brightness (int): final brightness value
        time_span (float): minutes
    """
    try:
        device = await client.l510(lamp_ip)
    except Exception:
        out("please check the lamp ip and that the lamp is connected to your home network.")
        return
    
    await device.on()
    
    if start_brightness is None:
        device_info = await device.get_device_info()        
        start_brightness = device_info.to_dict()['brightness']
           
        out("No start brightness provided, assuming current brightness as starting brightness: %d" % start_brightness)
        
    
    schedule = getValuesSchedule(start_brightness, end_brightness, time_span)
    
    delta = dt.timedelta(minutes=time_span)
    humanized_time_span = humanize.precisedelta(delta, minimum_unit="seconds")
    
    out("going from %d to %d brightness in %s" % (start_brightness, end_brightness, humanized_time_span))
        
    time_values = schedule[0]
    brightness_values = schedule[1]
                
    t = 0    
    while t < len(time_values):
        t_val = time_values[t]
        b_val = brightness_values[t]
                
        time.sleep(t_val)
        
        if b_val == 0:
            await device.off()
        else:
            await device.set_brightness(b_val)
        
        out("brightness set to %d" % b_val)
        
        t += 1
    
    out("fade finished.")
    
def main():
    #load credentials
    json_file_path = r"credentials.json"
    with open(json_file_path, "r") as f:
        credentials = json.load(f)
        
    username = credentials["username"]
    password = credentials["password"]
    lamp_ip = credentials["network_address"]
    
    client = ApiClient(username, password)
                
    asyncio.run(longFade(client, lamp_ip, None, 10, 0.2))

if __name__ == "__main__":
    main()
    