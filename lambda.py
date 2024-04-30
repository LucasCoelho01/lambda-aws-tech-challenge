import json
import re
import boto3

def lambda_handler(event, context):
    # Extract CPF from the request
    cpf = event.get('cpf')
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('users')
    
    # Validate CPF format
    if not cpf:
        return {
            'statusCode': 400,
            'body': 'CPF empty'
        }
        
    if not validate_cpf_format(cpf):
        return {
            'statusCode': 400,
            'body': 'Invalid CPF format'
        }

    response = table.scan(
        FilterExpression='cpf = :val',
        ExpressionAttributeValues={
            ':val': cpf
        }
    )
    
    # Your authorization logic here
    if response['Items']:
        return {
            'statusCode': 200,
            'body': 'CPF Authorized'
        }
    else:
        return {
            'statusCode': 400,
            'body': 'CPF Unauthorized'
        }
    
def validate_cpf_format(cpf):
    # CPF must be in the format XXX.XXX.XXX-XX
    cpf_pattern = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
    return bool(cpf_pattern.match(cpf))
