from __future__ import print_function
import re
import datetime
import boto3
from boto3.dynamodb.conditions import Key

carDict = {1: 700,2: 600,3: 530,4: 450,5: 390,6: 330,7: 300,8: 260,9: 230,10: 200}
def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    
    print("Received event: " + str(event))
    if 'Body' in event: method = event['Body']
    else: return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response><Message>Sorry, there was an error.  Try again late. Part 1 failr</Message></Response>'
    method = method.strip()
    wordSet = set(re.split('\+| ', re.sub('[^A-Za-z0-9\+ ]+', '', method.lower())))
    now = datetime.datetime.now()
    
    idVal = event['AccountSid']
    epochVal = str(int(datetime.datetime.now().timestamp()))
    
    if 'start' in wordSet and len(wordSet) > 1:
        start = True
        client.put_item(TableName = 'tripLogs', Item={'id': {"S":idVal},'epoch': {"N": epochVal}})
        return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response><Message>Ride started at ' + str(now.hour) + ':' + str(now.minute) + 'UTC' + '</Message></Response>'
          
    elif ('stop' in wordSet or 'end' in wordSet) and len(wordSet) > 1:
        start = False
    
        output = client.query(TableName = 'tripLogs', KeyConditionExpression = 'id = :X', ExpressionAttributeValues={":X" : {"S" : idVal}}, ScanIndexForward = False, Limit = 1)
        ems = client.query(TableName = 'tripLogs', KeyConditionExpression = 'id = :X', ExpressionAttributeValues={":X" : {"S" : idVal}})
        carType = 6
        for item in ems['Items']:
            if 'emissions_class' in item:
                carType = item['emissions_class']['S']
                break
        print(output['Items'])
        print(epochVal)
        timeElapsed = int((int(epochVal) - int(output['Items'][0]['epoch']['N'])) / 60)
        co2 = int(timeElapsed * .7 * carDict[int(carType)])
        
        client.put_item(TableName = 'tripLogs', Item={'id': {"S":idVal},'epoch': {"N": epochVal}})
        return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response><Message>Ride end at ' + str(now.hour) + ':' + str(now.minute) + 'UTC' + '. Trip time - ' + str(timeElapsed) + ' minutes and emissions - ' + str(co2) + ' g of CO2 </Message></Response>'
    
    elif ('type' in wordSet or 'info' in wordSet) and len(wordSet) > 1:
        carNum = 6
        for i in wordSet:
            try: 
                carNum = int(i)
            except ValueError:
                continue
        
        client.put_item(TableName = 'tripLogs', Item={'id': {"S":idVal}, 'epoch': {"N": "0"}, 'emissions_class': {"S":str(carNum)}})
        return '<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>Type ' + str(carNum) + ' cars produce ' + str(carDict[carNum]) + 'g of CO2 per mile </Message></Response>'
        
    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response><Message>Sorry, please either send info, start car, or stop car</Message></Response>'
