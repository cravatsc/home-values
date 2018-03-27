import boto3
from config_management import config_manager


config = config_manager.ConfigManager('app.config')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                          aws_access_key_id=config.get('aws_pub_key'), aws_secret_access_key=config.get('aws_sec_key'))


table = dynamodb.create_table(
    TableName='valley_forge_zestimate',
    KeySchema=[{
        'AttributeName':'date',
        'KeyType':'HASH'
    }],
    AttributeDefinitions=[{
        'AttributeName':'date',
        'AttributeType':'S'
    }],
    ProvisionedThroughput={
        'ReadCapacityUnits':5,
        'WriteCapacityUnits':5
    }
)

table.wait_until_exists()
print('Table created!')
