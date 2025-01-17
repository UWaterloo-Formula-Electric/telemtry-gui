import influxdb_client, os, datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from config import INFLUX_URL, INFLUX_BUCKET, INFLUX_TOKEN, INFLUX_ORG
from can_data import Signal

token = INFLUX_TOKEN
org = INFLUX_ORG
url = INFLUX_URL
bucket = INFLUX_BUCKET

write_client = InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

def mock_write():
    for value in range(1000):
        point = (
          Point("measurement1")
          .tag("tagname1", "tagvalue1")
          .field("field1", value)
        )
        write_api.write(bucket=bucket, org=INFLUX_ORG, record=point)
        print('wrote: ', value)
        time.sleep(1) # separate points by 1 second

def write_signal(signal: Signal):
    try:
      point = (Point(signal.msg_name)\
        .tag("sender", signal.sender)\
        .tag("signal_name", signal.signal_name)\
        .field("value", float(signal.value)))
       # .time(signal.timestamp)
      write_api.write(bucket=bucket, org=INFLUX_ORG, record=point)
      print(signal)
    except Exception as e:
      print(e)

def write_dtc(code, severity, data, msg):
    try:
      point = (Point("DTC")\
        .tag("code", code)\
        .tag("severity", severity)\
        .tag("data", data)\
        .field("msg", msg))
      write_api.write(bucket=bucket, org=INFLUX_ORG, record=point)
      print(f"{msg}: {code}, {severity}, {data}")
    except Exception as e:
      print(e)