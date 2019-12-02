import requests

base_url = 'https://api.meraki.com/api/v0'

def create_action_batch(api_key, org_id, confirmed=False, synchronous=False, payload=None):
    post_url = f'{base_url}/organizations/{org_id}/actionBatches'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}
    response = requests.post(post_url, headers=headers, json=payload)
    data = response.json() if response.ok else response.text
    return (response.ok, data)


def get_org_action_batches(api_key, org_id):
    get_url = f'{base_url}/organizations/{org_id}/actionBatches'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}

    response = requests.get(get_url, headers=headers)
    data = response.json() if response.ok else response.text
    return (response.ok, data)


def get_action_batch(api_key, org_id, batch_id):
    get_url = f'{base_url}/organizations/{org_id}/actionBatches/{batch_id}'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}

    response = requests.get(get_url, headers=headers)
    data = response.json() if response.ok else response.text
    return (response.ok, data)

# this function uses response.text instead of response.json()
# the Dashboard API returns nothing (null) when an action batch is successfully deleted
# this causes the json parser in requests response.json to throw errors.
def delete_action_batch(api_key, org_id, batch_id):
    delete_url = f'{base_url}/organizations/{org_id}/actionBatches/{batch_id}'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}
    response = requests.delete(delete_url, headers=headers)
    data = response.text
    return (response.ok, data)

def update_action_batch(api_key, org_id, batch_id, confirmed=False, synchronous=False):
    put_url = f'{base_url}/organizations/{org_id}/actionBatches/{batch_id}'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}
    payload = {
        'confirmed': confirmed,
        'synchronous': synchronous,
    }
    response = requests.put(put_url, headers=headers, json=payload)
    data = response.json() if response.ok else response.text
    return (response.ok, data)