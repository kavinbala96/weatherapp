# WEATHER METRICS APPLICATION
## Tech Stack




- Python
- Flask
- Elasticsearch

## Why Elasticsearch ?

- NoSQL DBs are the obvious choice for time-series data
- It has native AWS support i.e. AWS OpenSearch Service 
- Sensors can directly POST their data to the Elasticsearch DB without having to go thourgh a middleware REST app.
- It has support for aggregation unlike DynamoDB
- MongoDB was a strong contender and has similar features to elasticsearch

## Instructions to run & test the application


- [Download elasticsearch for Windows] - Use the hyperlink
- Extract the zip and navigate to the config folder and open the elasticsearch.yml file
and add "xpack.security.enabled: false" without quotes at the end of the file and save it.
- Run **elasticsearch.bat** from the bin folder to start the DB. Default port is 9200.
- After cloning the repo, go to the directory where the app.py is located and run: "pip install -r requirements.txt" from the cmd without quotes. Make sure python is installed in the machine.
-  Run "python app.py" without quotes from cmd to start the application. Default port is 5000
-  Use the Postman collection provided to aggregate weather data and query specific metric
-  The Postman collection contains 4 endpoints in total:
    -  2 endpoints that point to the python app (query sensor data and aggregate metrics (max & min types supported as well)) 
    -  2 endpoints that point to elasticsearch DB ( POST sensor data to DB and delete the index).

## Things to Note
- **Use the headers in the postman requests to change the query parameters like sensor location and time range**
- The elasticsearch DB will be pre-populated with sensor data for last 24 hours for 5 different cities when the python app loads. This is for your convenience so you are not required to insert test data. But **you can add your own custom location & metrics through the postman endpoint**
- If no time span is specified when querying the db, the results would be returned for last 3 hours.



[//]: # (Reference links)

   [Download elasticsearch for Windows]: <https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.9.0-windows-x86_64.zip>
