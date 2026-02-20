import http.client
import json
import time

# Configuration

# Configuration
API_HOST = "api.trustin-webui-dev.com"

# API Key provided by the user
API_KEY = "ce02a019-722b-48ba-864d-71071c2c0ebd"

def _make_request(method, endpoint, payload):
    """Helper to make HTTP requests."""
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'Content-Type': 'text/plain'
    }
    
    # Append API Key to the endpoint URL
    if "?" in endpoint:
        endpoint += f"&apikey={API_KEY}"
    else:
        endpoint += f"?apikey={API_KEY}"
    
    try:
        json_payload = json.dumps(payload)
        conn.request(method, endpoint, json_payload, headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def submit_investigation(chain_name, address, inflow_hops=5, outflow_hops=5, max_nodes_per_hop=100):
   """Submits a new investigation task."""
   payload = {
       "chain_name": chain_name,
       "address": address,
       "inflow_hops": inflow_hops,
       "outflow_hops": outflow_hops,
       "max_nodes_per_hop": max_nodes_per_hop
   }
   # Updated to v2 endpoint as per user request
   return _make_request("POST", "/api/v2/investigate/submit_task", payload)

def get_investigation_status(task_id):
   """Checks the status of an investigation task."""
   payload = {
       "task_id": task_id
   }
   return _make_request("POST", "/api/v2/investigate/get_status", payload)

def get_investigation_result(task_id, token="usdt"):
   """Retrieves the result of a completed investigation task."""
   payload = {
       "task_id": task_id,
       "token": token
   }
   return _make_request("POST", "/api/v2/investigate/get_result", payload)

def fetch_full_graph(chain_name, address, token="usdt"):
    """
    Orchestrates the full flow: Submit -> Poll -> Get Result.
    """
    print(f"Submitting investigation for {address} on {chain_name}...")
    submit_res = submit_investigation(chain_name, address)
    
    # Assuming successful submission returns a 'data' field with task_id based on user description
    # Adjust error handling based on actual API response
    if "data" not in submit_res:
        print(f"Submission failed: {submit_res}")
        return submit_res
        
    task_id = submit_res["data"]
    print(f"Task submitted. Task ID: {task_id}")
    
    # Polling
    max_retries = 30
    for i in range(max_retries):
        status_res = get_investigation_status(task_id)
        print(f"Polling status ({i+1}/{max_retries})... Response: {status_res}")
        
        # Check condition based on typical API patterns, willing to adjust if user provides specific status structure
        # If the status returns the result directly or indicates success
        status_data = status_res.get("data")
        
        # flexible check
        if status_data in ["success", "finished"] or (isinstance(status_data, dict) and status_data.get("status") in ["success", "finished"]):
             print("Task completed successfully.")
             break
        elif status_data == "failed" or (isinstance(status_data, dict) and status_data.get("status") == "failed"):
             print("Task failed.")
             return {"error": "Task failed", "details": status_res}
             
        time.sleep(2)
    else:
        return {"error": "Timeout waiting for task completion"}

    print("Fetching results...")
    result_res = get_investigation_result(task_id, token)
    return result_res

if __name__ == "__main__":
    # Test execution
    chain = "Tron"
    addr = "THaUdoNaeL7FEHFGpzEktHiJPsDctc6C6o"
    result = fetch_full_graph(chain, addr)
    print(json.dumps(result, indent=2))
