# for RITS
import os
import requests
from litellm import completion as litellm_completion

# Headers for REST API request
BASE_HEADERS = {"Content-Type": "application/json", "accept": "application/json"}

## RITS API
RITS_API_KEY = os.environ.get("RITS_API_KEY")
RITS_HEADERS = {"Content-Type": "application/json", "accept": "application/json", "RITS_API_KEY": f"{RITS_API_KEY}"}

def get_all_rits_model_info():
    response = requests.get(url="https://rits.fmaas.res.ibm.com/ritsapi/inferenceinfo", headers=RITS_HEADERS)
    assert response.status_code == 200, f"RITS server is not avaiable, got error: {response.json()}"
    model_list = response.json()
    model_dict = { m["model_name"]: m["endpoint"] for m in model_list }
    return model_dict

all_rits_model_info = None

def completion(kwargs):

    if kwargs['model'].startswith("RITS/"):
        global all_rits_model_info
        #rits_model_name = "openai/gpt-oss-120b"
        #rits_model_name = "ibm-granite/granite-vision-3.3-2b"
        #rits_model_name = "RITS/Qwen/Qwen2-VL-72B-Instruct"
        rits_model_name = kwargs['model'].replace("RITS/", "")
        if all_rits_model_info is None:
            all_rits_model_info = get_all_rits_model_info()
        assert rits_model_name in all_rits_model_info, f"Model {rits_model_name} is not available on RITS, please double check."
        rits_url = all_rits_model_info[rits_model_name] + '/v1'
        kwargs['model'] = 'openai/' + rits_model_name
        kwargs['api_base'] = rits_url
        kwargs['api_key'] = "dummy" # To make LiteLLM happy, it is not used for RITS
        kwargs['extra_headers'] = {"RITS_API_KEY": RITS_API_KEY}
    elif kwargs['model'].startswith("IBM_LITELLM/"): 
        model_name = 'openai/' + kwargs['model'].replace("IBM_LITELLM/", "")
        kwargs['model'] = model_name
        kwargs['api_base'] = "https://ete-litellm.ai-models.vpc-int.res.ibm.com/v1"
        kwargs['api_key'] = os.environ["IBM_LITELLM_API_KEY"]

    return litellm_completion(**kwargs)


