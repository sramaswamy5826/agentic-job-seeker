import boto3
import logging
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, RESUME_TABLE_NAME

logger = logging.getLogger(__name__)

class DynamoDBService:
    """Service to interact with AWS DynamoDB."""
    
    def __init__(self, 
                table_name: str = RESUME_TABLE_NAME, 
                region: str = AWS_REGION,
                access_key: str = AWS_ACCESS_KEY_ID,
                secret_key: str = AWS_SECRET_ACCESS_KEY):
        """
        Initialize the DynamoDB service.
        
        Args:
            table_name: Name of the DynamoDB table
            region: AWS region
            access_key: AWS access key ID
            secret_key: AWS secret access key
        """
        self.table_name = table_name
        
        if not access_key or not secret_key:
            # Use IAM role or credentials from ~/.aws/credentials
            session = boto3.Session(region_name=region)
        else:
            # Use provided credentials
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
        
        self.dynamodb = session.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def get_resume(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve resume data from DynamoDB by ID.
        
        Args:
            resume_id: Unique identifier for the resume
            
        Returns:
            Resume data dictionary or None if not found
        """
        try:
            response = self.table.get_item(Key={'id': resume_id})
            
            if 'Item' in response:
                return response['Item']
            else:
                logger.warning(f"Resume with ID {resume_id} not found")
                return None
                
        except ClientError as e:
            logger.error(f"Error retrieving resume from DynamoDB: {e}")
            return None
    
    def list_resumes(self, limit: int = 10) -> list:
        """
        List available resumes in the DynamoDB table.
        
        Args:
            limit: Maximum number of resumes to return
            
        Returns:
            List of resume IDs
        """
        try:
            response = self.table.scan(
                ProjectionExpression="id, contact_info.name",
                Limit=limit
            )
            
            items = response.get('Items', [])
            return [{'id': item.get('id'), 'name': item.get('contact_info', {}).get('name')} 
                   for item in items if 'id' in item]
                
        except ClientError as e:
            logger.error(f"Error listing resumes from DynamoDB: {e}")
            return []