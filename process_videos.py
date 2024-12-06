# Standard imports
import sys
import os
import argparse
import time
import json
from concurrent.futures import ThreadPoolExecutor

# Load the custom modules
sys.path.append("code")
from utils.content_understanding_client import AzureContentUnderstandingClient

# Load credentials
from dotenv import load_dotenv
load_dotenv()

# Define the template directory
template_directory = os.path.dirname(os.path.abspath("__file__")) + "/templates"

def process_video(file, cu_client, data_path, analyzerId):
    """
    Process a video file using the Content Understanding client

    :param file: The video file to process
    :param cu_client: The Content Understanding client
    :param data_path: The path to the data files
    :param analyzerId: The custom analyzer ID
    
    :return: The file name and the elapsed time
    """
    
    # Record the start time
    start_time = time.time()

    print(f"Processing {file}...")

    # Submit the video for content analysis
    response = cu_client.begin_analyze(analyzer_id = analyzerId, file_location = f"{data_path}/{file}")

    # Wait for the analysis to complete and get the content analysis result
    video_cu_result = cu_client.poll_result(response, timeout_seconds = 3600)  # 1 hour timeout for long videos

    # Save the result to a file
    result_file = f"{data_path}/{analyzerId}/{os.path.splitext(file)[0]}.json"
    
    with open(result_file, "w") as f:
        json.dump(video_cu_result, f, indent=2)

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    return [file, elapsed_time]

def parallel_process_videos(files, cu_client, data_path, analyzerId, max_workers=4):
    """
    Process multiple video files in parallel

    :param files: The list of video files to process
    :param cu_client: The Content Understanding client
    :param data_path: The path to the data files
    :param analyzerId: The custom analyzer ID
    :param max_workers: The maximum number of workers
    
    :return: The list of results
    """
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_video, file, cu_client, data_path, analyzerId): file for file in files}
        for future in futures:
            try:
                result = future.result()  # Collect the result
                results.append(result)
            except Exception as e:
                pass
    return results

def create_or_load_analyzer(cu_client, analyzerId, data_path):
    """
    Create or load a custom analyzer

    :param cu_client: The Content Understanding client
    :param analyzerId: The custom analyzer ID
    :param data_path: The path to the data files
    """
    analyzer_list = [analyzer["analyzerId"] for analyzer in cu_client.get_all_analyzers()["value"]]

    # Check if the custom analyzer exists
    if analyzerId not in analyzer_list:
        # Use the client to create an analyzer
        cu_client.begin_create_analyzer(analyzerId, analyzer_schema_path=f"{template_directory}/{analyzerId}.json")

        print(f"Analyzer {analyzerId} created successfully.")
    else:
        print(f"Analyzer {analyzerId} already exists.")

    # Create a folder to sort the results
    if not os.path.exists(f"{data_path}/{analyzerId}"):
        os.makedirs(f"{data_path}/{analyzerId}")

def load_files(data_path):
    """
    Load the video files from the data path

    :param data_path: The path to the data files
    
    :return: The list of video files
    """
    files = []
    # Loop through the files in the data path
    for file in os.listdir(data_path):

        video_extensions = [".mp4", ".m4v", ".flv", ".wmv", ".asf", ".avi", ".mkv", ".mov"]
        file_extension = os.path.splitext(file)[1]

        if file_extension in video_extensions:
            files.append(file)

    return files

def main():

    # Set the maximum number of workers
    max_workers = 4

    # Record the start time
    start_time = time.time()

    # Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", type=str, help="Path to the data files")
    parser.add_argument("analyzer_id", type=str, help="Name of the custom analyzer for Content Understanding")
    
    args = parser.parse_args()
    data_path = args.data_path
    analyzerId = args.analyzer_id

    # Load the credentials present in environment variables
    endpoint = os.getenv("AZURE_AI_CONTENT_UNDERSTANDING_ENDPOINT")
    api_key = os.getenv("AZURE_AI_CONTENT_UNDERSTANDING_KEY")
    api_version = os.getenv("AZURE_AI_CONTENT_UNDERSTANDING_API_VERSION")

    # Create the Content Understanding (CU) client
    cu_client = AzureContentUnderstandingClient(endpoint = endpoint, api_version = api_version, subscription_key = api_key)

    # Create or load the custom analyzer
    create_or_load_analyzer(cu_client, analyzerId, data_path)

    # Load the video files
    files = load_files(data_path)

    # Process the videos in parallel
    results = parallel_process_videos(files, cu_client, data_path, analyzerId, max_workers)

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print ("Finished in {:.2f} seconds".format(elapsed_time))

if __name__ == "__main__":
    main()