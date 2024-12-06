# Standard imports
import sys
sys.path.append("code")

import argparse
import os
import json
import pandas as pd

template_directory = os.path.dirname(os.path.abspath("__file__")) + "/templates"

def main():

    # Parse the arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", type=str, help = "Path to the data files")
    parser.add_argument("analyzer_id", type=str, help="Name of the custom analyzer for Content Understanding")

    args = parser.parse_args()
    data_path = args.data_path
    analyzerId = args.analyzer_id

    combined_result = []
    combined_result2 = []
    col_names = ["file", "nothing", "accident", "roadsideFire", "objectsRoad", "laneClosure", "trafficJam", "roadConstruction", "stoppedVehicle"]

    # Loop through the files in the data path
    for json_result in os.listdir(f"{data_path}/{analyzerId}"):
        
        # Check if the file is a json file
        if json_result.endswith(".json"):

            # load the json file containing the results per video
            json_result_data = json.load(open(f"{data_path}/{analyzerId}/" + json_result))

            # create a list to store the results
            result = []
            result2 = []
            
            result.append(json_result.replace(".json", ".mp4"))
            result2.append(json_result.replace(".json", ".mp4"))

            # If the content filter flags the video as inappropriate, the structure is compromised. Set all the flags to False
            try:
                # get the binary predictions for all the events
                accident = json_result_data["result"]["contents"][0]["fields"]["accident"]["valueBoolean"]
                roadsideFire = json_result_data["result"]["contents"][0]["fields"]["roadsideFire"]["valueBoolean"]
                objectsRoad = json_result_data["result"]["contents"][0]["fields"]["objectsRoad"]["valueBoolean"]
                laneClosure = json_result_data["result"]["contents"][0]["fields"]["laneClosure"]["valueBoolean"]
                trafficJam = json_result_data["result"]["contents"][0]["fields"]["trafficJam"]["valueBoolean"]
                roadConstruction = json_result_data["result"]["contents"][0]["fields"]["roadConstruction"]["valueBoolean"]
                stoppedVehicle = json_result_data["result"]["contents"][0]["fields"]["stoppedVehicle"]["valueBoolean"]
                
                # If no event occurs, than it is nothing
                if accident or roadsideFire or objectsRoad or laneClosure or trafficJam or roadConstruction or stoppedVehicle:
                    nothing = False
                else:
                    nothing = True

                result.append(nothing)
                result.append(accident)
                result.append(roadsideFire)
                result.append(objectsRoad)
                result.append(laneClosure)
                result.append(trafficJam)
                result.append(roadConstruction)
                result.append(stoppedVehicle)
            
                classes = ""
                if nothing:
                    classes += "nothing;"
                if accident:
                    classes += "accident;"
                if roadsideFire:
                    classes += "roadsideFire;"
                if objectsRoad:
                    classes += "objectsRoad;"
                if laneClosure:
                    classes += "laneClosure;"
                if trafficJam:
                    classes += "trafficJam;"
                if roadConstruction:
                    classes += "roadConstruction;"
                if stoppedVehicle:
                    classes += "stoppedVehicle;"

                # if the last character is a semicolon, remove it
                if classes[-1] == ";":
                    classes = classes[:-1]

                result2.append(classes)

            except Exception as e:
                result.extend([False, False, False, False, False, False, False, False])

            combined_result.append(result)
            combined_result2.append(result2)
    
    # Save the results to a csv file in the folder containing the jsons
    df_results = pd.DataFrame(combined_result, columns = col_names)
    df_results.to_csv(f"{data_path}/{analyzerId}/results.csv", index = False)

    df_results2 = pd.DataFrame(combined_result2, columns = ["file", "classes"])
    df_results2.to_csv(f"{data_path}/{analyzerId}/results2.csv", index = False)

if __name__ == "__main__":
    main()