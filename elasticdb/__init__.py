import logging
import json
import pandas as pd
import random
from elasticsearch import Elasticsearch
from datetime import datetime,timedelta
elastic_client = Elasticsearch("http://localhost:9200",timeout=5)


def configure_client():

    try:
        if not (elastic_client.indices.exists(index="weatherdata")):
            
            # Create index with schema/mappings
            with open("elasticdb/index.json") as index_file:  
                elastic_client.indices.create(index="weatherdata",body=json.load(index_file))

            # Populate/seed dummy sensor data, we had assumed the sensors will POST the weather data to the server
            sensor_location=["raleigh","orlando","seattle","houston","boston"]
            start = (datetime.now()-timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
            end =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for time_stamp in pd.date_range(start, end, freq='30T'):
                for sensor in sensor_location:
                    data={

                    "temperature" : "%.2f" % random.uniform(90,100),
                    "humidity" :  "%.2f" % random.uniform(70,100),
                    "windspeed":  "%.2f" % random.uniform(70,100),
                    "timestamp":  str(time_stamp),#time_stamp.timestamp(),
                    "sensor_location": sensor
                    }
                    elastic_client.index(index="weatherdata",body=data)
        else:
            logging.info(f"Index already exist!")                        

    except Exception as e:
        logging.error(f"Exception occured while creating search index : {e}")                        
    
    finally:
        return elastic_client