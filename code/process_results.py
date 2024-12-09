# Standard imports
import sys
sys.path.append("code")

import argparse
import os
import json
import pandas as pd

# Define the analyzer directory
analyzer_directory = os.path.dirname(os.path.abspath("__file__")) + "/analyzer"

def main():

    # Parse the arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("file_type", type=str, help="Type of the files to process (video, image, audio, document)")
    parser.add_argument("data_path", type=str, help = "Path to the data files")
    parser.add_argument("analyzer_id", type=str, help="Name of the custom analyzer for Content Understanding")

    args = parser.parse_args()
    file_type = args.file_type
    data_path = args.data_path
    analyzerId = args.analyzer_id

    combined_result = []

    # Loop through the files in the data path
    for json_result in os.listdir(f"{data_path}/{analyzerId}"):
        
        # Check if the file is a json file
        if json_result.endswith(".json"):

            # load the json file containing the results per video
            json_result_data = json.load(open(f"{data_path}/{analyzerId}/" + json_result))

            # create a list to store the results
            result = []
            
            result.append(json_result.replace(".json", ""))

            # Parse the json depending on the file type
            if file_type == "video":
                col_names = ["file_name", "productBrand", "productType", "productName", "description"]
                # If the content filter flags the video as inappropriate, the structure is compromised. Set all the flags to False
                try:
                    # get the binary predictions for all the events
                    productBrand = json_result_data["result"]["contents"][0]["fields"]["productBrand"]["valueString"]
                    productType = json_result_data["result"]["contents"][0]["fields"]["productType"]["valueString"]
                    productName = json_result_data["result"]["contents"][0]["fields"]["productName"]["valueString"]
                    description = ""
                    for i in range(len(json_result_data["result"]["contents"])):
                        description += json_result_data["result"]["contents"][i]["fields"]["description"]["valueString"] + "/n"

                    result.append(productBrand)
                    result.append(productType)
                    result.append(productName)
                    result.append(description)
                    
                except:
                    result.append("")
                    result.append("")
                    result.append("")
                    result.append("")
                    
                # Append the results to the list
                combined_result.append(result)

            elif file_type == "image":
                col_names = ["file_name", "Title", "AnimalSpecies", "NumberOfIndividuals",]
                # If the content filter flags the video as inappropriate, the structure is compromised. Set all the flags to False
                try:
                    # get the binary predictions for all the events
                    Title = json_result_data["result"]["contents"][0]["fields"]["Title"]["valueString"]
                    AnimalSpecies = json_result_data["result"]["contents"][0]["fields"]["AnimalSpecies"]["valueString"]
                    NumberOfIndividuals = json_result_data["result"]["contents"][0]["fields"]["NumberOfIndividuals"]["valueInteger"]

                    result.append(Title)
                    result.append(AnimalSpecies)
                    result.append(NumberOfIndividuals)
                    
                except:
                    result.append("")
                    result.append("")
                    result.append("")
                    
                # Append the results to the list
                combined_result.append(result)

            elif file_type == "audio":
                col_names = ["file_name", "Sentiment", "Companies", "People", "Topics"]
                # If the content filter flags the video as inappropriate, the structure is compromised. Set all the flags to False
                try:
                    # get the binary predictions for all the events
                    Sentiment = json_result_data["result"]["contents"][0]["fields"]["Sentiment"]["valueString"]

                    Companies = ""
                    for i in range(len(json_result_data["result"]["contents"][0]["fields"]["Companies"]["valueArray"])):
                        Companies += json_result_data["result"]["contents"][0]["fields"]["Companies"]["valueArray"][i]["valueObject"]["Name"]["valueString"] + ";"

                    People = ""
                    for i in range(len(json_result_data["result"]["contents"][0]["fields"]["People"]["valueArray"])):
                        Name = json_result_data["result"]["contents"][0]["fields"]["People"]["valueArray"][i]["valueObject"]["Name"]["valueString"]
                        Role = json_result_data["result"]["contents"][0]["fields"]["People"]["valueArray"][i]["valueObject"]["Role"]["valueString"]
                        People += f"{Name}({Role})" + ";"
                    
                    Topics = ""
                    for i in range(len(json_result_data["result"]["contents"][0]["fields"]["Topics"]["valueArray"])):
                        Topics += json_result_data["result"]["contents"][0]["fields"]["Topics"]["valueArray"][i]["valueString"] + ";"

                    result.append(Sentiment)
                    result.append(Companies)
                    result.append(People)
                    result.append(Topics)
                    
                except:
                    result.append("")
                    result.append("")
                    result.append("")
                    result.append("")

                # Append the results to the list
                combined_result.append(result)

            elif file_type == "document":
                col_names = ["file_name", "VendorName", "Description", "Amount"]
                # If the content filter flags the video as inappropriate, the structure is compromised. Set all the flags to False
                try:
                    # get the binary predictions for all the events
                    VendorName = json_result_data["result"]["contents"][0]["fields"]["VendorName"]["valueString"]

                    for i in range(len(json_result_data["result"]["contents"][0]["fields"]["Items"]["valueArray"])):
                        Description = json_result_data["result"]["contents"][0]["fields"]["Items"]["valueArray"][i]["valueObject"]["Description"]["valueString"]
                        Amount = json_result_data["result"]["contents"][0]["fields"]["Items"]["valueArray"][i]["valueObject"]["Amount"]["valueNumber"]

                        result.append(VendorName)
                        result.append(Description)
                        result.append(Amount)

                        # Append the results to the list
                        combined_result.append(result)

                        result = []
                        result.append(json_result.replace(".json", ""))

                except:
                    result.append("")
                    result.append("")
                    result.append("")

                    # Append the results to the list
                    combined_result.append(result)
                    result.append(json_result.replace(".json", ""))
                    
                    result = []
            else:
                col_names = ["file_name"]

    
    # Save the results to a csv file in the folder containing the jsons
    df_results = pd.DataFrame(combined_result, columns = col_names)
    df_results.to_csv(f"{data_path}/{analyzerId}/results.csv", index = False)

if __name__ == "__main__":
    main()