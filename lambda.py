import boto3
import json
import copy

def lambda_handler(event, context):
    
    client = boto3.client('apigateway')
    stage = "dev"
    # Retrieve information about all the REST APIs in the account
    response = client.get_rest_apis()

    # Loop through each REST API and retrieve its OpenAPI JSON definition
    openapi_json = {}
    for item in response['items']:
        rest_api_id = item['id']
        rest_api_name = item['name']
        rest_api_export = client.get_export(
            restApiId=rest_api_id,
            stageName=stage,
            exportType='oas30',
            accepts='application/json'
        )
        openapi_json_part = json.loads(rest_api_export['body'].read())
    
        print("data",openapi_json_part)
        openapi_json_part['info']['title'] = 'My API'
        
        client.put_rest_api(restApiId=rest_api_id, mode='overwrite', 
        body=json.dumps(openapi_json_part))
        
        

    # Return the combined OpenAPI JSON definition for all REST APIs in the account
    return {
        'statusCode': 200,
        'body': json.dumps(openapi_json, indent=4)
    }
