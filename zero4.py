import csv
import requests
from collections import defaultdict


def get_unique_values(csv_file, column_name):
    unique_values = set()
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            unique_values.add(row[column_name])
    return list(unique_values)


def get_api_data(address):
    method = "get"
    apiUrl = f"https://api.1inch.dev/history/v2.0/history/{address}/events"
    requestOptions = {
        "headers": {
            "Authorization": "Bearer 80q7zTgWitvOsPU8pVDq3gTX5ift2iEh"
        },
        "params": {
            "limit": "10000",
            "chainId": "1"
        }
    }

    response = requests.get(apiUrl, headers=requestOptions["headers"], params=requestOptions["params"])
    return response.json()


def extract_addresses(api_data):
    addresses = set()
    for item in api_data.get('items', []):
        details = item.get('details', {})
        addresses.add(details.get('fromAddress'))import csv
import requests
from collections import defaultdict

def get_unique_values(csv_file, column_name):
    unique_values = set()
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            unique_values.add(row[column_name])
    return list(unique_values)

def get_api_data(address):
    method = "get"
    apiUrl = f"https://api.1inch.dev/history/v2.0/history/{address}/events"
    requestOptions = {
        "headers": {
            "Authorization": "Bearer 80q7zTgWitvOsPU8pVDq3gTX5ift2iEh"
        },
        "params": {
            "limit": "10000",
            "chainId": "1"
        }
    }

    response = requests.get(apiUrl, headers=requestOptions["headers"], params=requestOptions["params"])
    return response.json()

def extract_addresses(api_data):
    addresses = set()
    for item in api_data.get('items', []):
        details = item.get('details', {})
        addresses.add(details.get('fromAddress'))
        addresses.add(details.get('toAddress'))
    return addresses

def find_address_clusters(csv_file):
    unique_from_addresses = get_unique_values(csv_file, 'from_address')

    address_interactions = defaultdict(set)

    for address in unique_from_addresses:
        api_data = get_api_data(address)
        related_addresses = extract_addresses(api_data)

        for related_address in related_addresses:
            if related_address and related_address != address:
                address_interactions[address].add(related_address)
                address_interactions[related_address].add(address)

    clusters = []
    processed = set()

    for address in address_interactions:
        if address not in processed:
            cluster = set([address])
            to_process = list(address_interactions[address])

            while to_process:
                current = to_process.pop(0)
                if current not in processed:
                    cluster.add(current)
                    processed.add(current)
                    to_process.extend(address_interactions[current])

            clusters.append(list(cluster))

    return clusters

# Usage
csv_file = 'your_csv_file.csv'
address_clusters = find_address_clusters(csv_file)

print("Address Clusters:")
for i, cluster in enumerate(address_clusters, 1):
    print(f"Cluster {i}: {cluster}")

        addresses.add(details.get('toAddress'))
    return addresses


def find_address_clusters(csv_file):
    unique_from_addresses = get_unique_values(csv_file, 'from_address')

    address_interactions = defaultdict(set)

    for address in unique_from_addresses:
        api_data = get_api_data(address)
        related_addresses = extract_addresses(api_data)

        for related_address in related_addresses:
            if related_address and related_address != address:
                address_interactions[address].add(related_address)
                address_interactions[related_address].add(address)

    clusters = []
    processed = set()

    for address in address_interactions:
        if address not in processed:
            cluster = set([address])
            to_process = list(address_interactions[address])

            while to_process:
                current = to_process.pop(0)
                if current not in processed:
                    cluster.add(current)
                    processed.add(current)
                    to_process.extend(address_interactions[current])

            clusters.append(list(cluster))

    return clusters


# Usage
csv_file = "/Users/anteroeloranta/PycharmProjects/lvr_grant/abis/morpho.json"

address_clusters = find_address_clusters(csv_file)

print("Address Clusters:")
for i, cluster in enumerate(address_clusters, 1):
    print(f"Cluster {i}: {cluster}")