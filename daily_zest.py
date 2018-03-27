import requests
import xml.etree.ElementTree as etree
from config_management import config_manager
import boto3

config = config_manager.ConfigManager('app.config')

url = 'http://www.zillow.com/webservice/GetZestimate.htm'
params = {'zws-id':config.get('ZWSID'), 'zpid':config.get('home_zpid')}
data = (requests.get(url, params)).content.decode()
tree = etree.fromstring(data)
zest_tree = tree.find('response').find('zestimate')
date = zest_tree.find('last-updated').text
zestimate = int(zest_tree.find('amount').text)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                          aws_access_key_id=config.get('aws_pub_key'), aws_secret_access_key=config.get('aws_sec_key'))
table = dynamodb.Table('valley_forge_zestimate')
val=table.get_item(Key={
    'date':date
})
if 'Item' not in val:
    table.put_item(
        Item={
            'date':date,
            'zestimate':zestimate
        }
    )
    print('New Zestimate added for {}: {}'.format(date, zestimate))
else:
    print('No new Zestimate available, latest Zestimate is from {} with a value of {}'.format(date, zestimate))
