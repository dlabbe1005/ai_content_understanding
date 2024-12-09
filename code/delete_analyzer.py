import sys
sys.path.append("code")

import argparse
import os

from utils.content_understanding_client import AzureContentUnderstandingClient

from dotenv import load_dotenv

load_dotenv()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("analyzer_id", type=str, help="Name of the custom analyzer for Content Understanding")

    args = parser.parse_args()
    analyzerId = args.analyzer_id

    endpoint = os.getenv("AZURE_AI_CONTENT_UNDERSTANDING_ENDPOINT")
    api_key = os.getenv("AZURE_AI_CONTENT_UNDERSTANDING_KEY")
    api_version = os.getenv("AZURE_AI_CONTENT_UNDERSTANDING_API_VERSION")

    # Create the Content Understanding (CU) client
    cu_client = AzureContentUnderstandingClient(endpoint = endpoint, api_version = api_version, subscription_key = api_key)

    cu_client.delete_analyzer(analyzerId)

    print(f"Analyzer {analyzerId} deleted successfully.")

if __name__ == "__main__":
    main()