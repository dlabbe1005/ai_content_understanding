## 1. Create conda env

```bash
conda create -n ai_content_understanding python=3.10
conda activate ai_content_understanding
```

## 2. pip install requirements
```bash
pip install -r requirements.txt
```

## 3. clone .env.sample and rename it to .env and change the following entries:
 - AZURE_AI_CONTENT_UNDERSTANDING_ENDPOINT
 - AZURE_AI_CONTENT_UNDERSTANDING_KEY

## 4. To run the analyzer use the folloing example
execute ´process_videos.py´ passing the path with videos and the name of the analyzer. The analyzer name must match the json name in the templates folder
```python
>> python process_videos.py [path to folder containing videos] [name of the custom analyzer]
```

## 5. To consolidate all the jsons into a single csv use the folloing example
execute ´process_videos.py´ passing the path with videos and the name of the analyzer. 
```python
>> python process_jsons.py [path to folder containing videos] [name of the custom analyzer]
```