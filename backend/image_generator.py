from generator.settings import WOMBOHEADER
import requests
import json
import time

WOMBOHEADER = {        
    'Authorization': 'bearer uovjcmHMu4iibJEcG7DSTTgTDNBUcjMp',        
    'Content-Type': 'application/json'
}

def get_wombo(self, spec):
    post_payload = json.dumps({
        "use_target_image": False
    })
    
    post_response = requests.request(
        "POST", "https://api.luan.tools/api/tasks/",
        headers = WOMBOHEADER, data = post_payload
    )
    print(post_response.json())
    task_id = post_response.json()['id']
    task_id_url = f"https://api.luan.tools/api/tasks/{task_id}"
    put_payload = json.dumps(
        spec
    )
    
    requests.request("PUT", task_id_url, headers = WOMBOHEADER, data = put_payload)
    while True:            
        response_json = requests.request(                    
            "GET", task_id_url, headers=WOMBOHEADER).json()     
        
        state = response_json["state"]    
    
        if state == "completed":                    
            r = requests.request("GET", response_json["result"])                    
            with open("image.jpg", "wb") as image_file:                            
                image_file.write(r.content)                        
            print("image saved successfully :)")                    
            break 
        
        elif state =="failed":                    
            print("generation failed :(")                    
            break            
        time.sleep(3)
    
    
    
def input_spec(self, style_id, prompt, spec = None):
    data = {
        'style': style_id,
        'prompt': prompt
    }
    
    if spec:
        for x in spec.keys():
            data[x] = spec[x]    
    
    return {
        'input_spec': data
    }
        
    
    
def image_spec(self, weight, width, height):
    return {
        'target_image_weight': weight,
        'width': width,
        'height': height
    }