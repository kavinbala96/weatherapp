import elasticdb
from datetime import datetime,timedelta
import logging
from flask import Flask, request, jsonify


app = Flask(__name__)
elastic_client = elasticdb.configure_client()



@app.route("/query-sensor", methods=['GET'])
def query_specific_sensor():
    try:

        # SET DEFAULT LAST 3 HOUR TIME RANGE IF USER DID NOT PROVIDE TIME RANGE
        from_range = request.headers.get('start',(datetime.now()-timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
        to_range = request.headers.get('end',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        sensor_location = request.headers.get('location','').split(',')

        # CHECK IF USER INCLUDED SENSOR LOCATION
        if (sensor_location[0]) == '':
            return jsonify({"message": "please provide sensor location in the headers"})

        # DOES DATE & TIME VALIDATION FOR US WHICH IS GREAT!!
        if datetime.strptime(from_range, "%Y-%m-%d %H:%M:%S").timestamp() < datetime.strptime(to_range, "%Y-%m-%d %H:%M:%S").timestamp():

                
            custom_query={
                "query": {
                    "bool": {
                        "must": [{
                                "terms": {
                                    "sensor_location": sensor_location
                                }
                            }, {
                                "range": {
                                    "timestamp": {
                                        "gte": from_range,
                                        "lte": to_range
                                    }
                                }
                            }
                        ]
                    }
                }
            }

            result = elastic_client.search(index="weatherdata", body=custom_query)

            return jsonify({ "range":f'{from_range} to {to_range}',"metrics":[entry.get('_source') for entry in result.get('hits',{}).get('hits',{})]})
        else:

            return jsonify({"range":f'{from_range} to {to_range}',"message": "query start time cannot be greater than end time"})
        
    except Exception as e:
    
        logging.error(f"UNABLE TO RETRIEVE CONTENT: {str(e)}")
        return jsonify({"message": str(e)}), 500


@app.route("/aggregate-sensor-data", methods=['GET'])
def aggregate_metrics_from_sensor():
    try:

        # STRPTIME DOES DATE&TIME VALIDATION FOR US WHICH IS GREAT!!
        from_range = request.headers.get('start',(datetime.now()-timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
        to_range = request.headers.get('end',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        sensor_location = request.headers.get('location',None)
        aggregate_type = request.headers.get('type','avg')

        # CHECK IF USER INCLUDED SENSOR LOCATION
        if not sensor_location:
            return jsonify({"message": "please provide sensor location in the headers"})

        # DOES DATE & TIME VALIDATION FOR US WHICH IS GREAT!!
        if datetime.strptime(from_range, "%Y-%m-%d %H:%M:%S").timestamp() < datetime.strptime(to_range, "%Y-%m-%d %H:%M:%S").timestamp():

            custom_query =  {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "range": {
                                    "timestamp": {
                                        "gte": from_range,
                                        "lte": to_range
                                    }
                                }
                            },
                            {
                                "term": {
                                    "sensor_location": sensor_location
                                }
                            }
                        ]
                    }
                },
                "aggs": {
                    f"{aggregate_type}_temperature": {
                        aggregate_type: {
                            "field": "temperature"
                        }
                    
                    },

                    f"{aggregate_type}_humidity": {
                        aggregate_type: {
                            "field": "humidity"
                        }
                    
                    },

                    f"{aggregate_type}_windspeed": {
                        aggregate_type: {
                            "field": "windspeed"
                        }
                    
                    },
                }
            }

            return jsonify({ "range":f'{from_range} to {to_range} ' ,"average_metrics": elastic_client.search(index="weatherdata", body=custom_query).get('aggregations')})
        
        else:

            return jsonify({"range":f'{from_range} to {to_range}',"message": "query start time cannot be greater than end time"})
        
    except Exception as e:
    
        logging.error(f"UNABLE TO RETRIEVE CONTENT: {str(e)}")
        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='localhost',port=5000)