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

## 4. To run the analyzer use the following example
execute ´process_files.py´ passing the path with videos and the name of the analyzer. The analyzer name must match the json name in the templates folder
```python
>> python process_files.py [content_type] [path to folder containing videos] [name of the custom analyzer]
```
for example:
```python
>> cd code
>> python process_files.py video ../data/videos cu_video_analyzer_ads
>> python process_files.py audio ../data/audios cu_audio_analyzer_callcenter
>> python process_files.py document ../data/documents cu_document_analyzer_invoice
>> python process_files.py image ../data/images cu_image_analyzer_animals
```

## 5. To consolidate all the jsons into a single csv use the following example
execute process_results.py´ passing the path with videos and the name of the analyzer. 
```python
>> python process_results.py [content_type] [path to folder containing videos] [name of the custom analyzer]
```
for example:
```python
>> cd code
>> python process_results.py video ../data/videos cu_video_analyzer_ads
>> python process_results.py audio ../data/audios cu_audio_analyzer_callcenter
>> python process_results.py document ../data/documents cu_document_analyzer_invoice
>> python process_results.py image ../data/images cu_image_analyzer_animals
```

## 6. To exclude an analyzer
```python
>> cd code
>> python process_jsons.py [name of the custom analyzer]
```
for example:
```python
>> cd code
>> python delete_analyzer.py cu_video_analyzer_ads
>> python delete_analyzer.py cu_audio_analyzer_callcenter
>> python delete_analyzer.py cu_document_analyzer_invoice
>> python delete_analyzer.py cu_image_analyzer_animals
```