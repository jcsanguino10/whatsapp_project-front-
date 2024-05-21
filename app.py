import requests
from unidecode import unidecode
# from sistema_logico import *

URL = "http://localhost:4000/question"

def post_request(url, headers=None, data=None, json=None):
    response = requests.post(url, headers=headers, data=data, json=json)
    return response

def create_answer(list_server_aws):
    anws = "" 
    for index, elem in enumerate(list_server_aws):
        anws += f'{index}.. {elem} \n'
    anws += "9.. Inicio \n" 
    return anws

def parse_body_request(index, options):
    text_raw = options[int(index)]
    return unidecode(text_raw).lower().strip()
# import requests
def main():
    # hello = 0
    # sistema= SistemaLogico()

    current_state = ""
    options= []
    while True:
        url_msg = "https://gate.whapi.cloud/messages/list/120363224308027086%40g.us?count=2&token=MI_TOKEN"

        headers = {"accept": "application/json"}

        response = requests.get(url_msg, headers=headers)

        print("-------------------")

        aux = response.json().get("messages")[0].get("text").get("body")

        # Deciding the reply based on the command
        if current_state=="":
            response_server = post_request(URL,json={"question":"start chat"})
            response_text = response_server.json().get("message")
            response_text += "\n"
            options = response_server.json().get("options")
            response_text += create_answer(options)
            current_state="Inicio"
        
        else:
            if aux.isdigit():
                if int(aux) == 9:
                    response_server = post_request(URL,json={"question":"start chat"})
                    response_text = response_server.json().get("message")
                    response_text += "\n"
                    options = response_server.json().get("options")
                    response_text += create_answer(options)
                    current_state="Inicio"
                else:
                    response_server = post_request(URL,json={"question":parse_body_request(aux,options)})
                    response_text = response_server.json().get("message")
                    response_text += "\n"
                    options = response_server.json().get("options")
                    response_text += create_answer(options)
                    current_state="Inicio"

        responder = response.json().get("messages")[0].get("from") != "573017113430"
        if responder:
            url = "https://gate.whapi.cloud/messages/text?token=MI_TOKEN"

            payload = {
                "typing_time": 2,
                "to": "120363224308027086@g.us",
                "body": response_text
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers)

            print(response.text)

if __name__ == "__main__":
    main()
