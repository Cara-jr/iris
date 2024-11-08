import os
import psycopg2
import logging
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration based on environment
try:
    ENV = os.environ.get('ENV', 'dev')
    if ENV == 'prod':
        from config.prod_config import (
            DB_HOST, DB_NAME, DB_USER, DB_PASSWORD,
            S3_BUCKET_NAME, IAM_ROLE_ARN
        )
        LOCAL_FILES_DIRECTORY = '/path/to/prod/local_files'
        S3_FEEDBACK_PREFIX = 'prod/feedback/'
    else:
        from config.dev_config import (
            DB_HOST, DB_NAME, DB_USER, DB_PASSWORD,
            S3_BUCKET_NAME, IAM_ROLE_ARN
        )
        LOCAL_FILES_DIRECTORY = './local_files'
        S3_FEEDBACK_PREFIX = 'dev/feedback/'
except ImportError as e:
    logger.error(f"Configuration import error: {e}")
    raise

# Reusable error response function
def create_error_response(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps({'error': message})
    }

def read_local_files(directory_path):
    """
    Reads all files in the specified directory and returns a list of dictionaries
    containing filename and content.
    """
    files_data = []
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    files_data.append({'filename': filename, 'content': content})
        logger.info(f"Read {len(files_data)} files from {directory_path}.")
    except Exception as e:
        logger.error(f"Error reading files from {directory_path}: {e}")
    return files_data

def chunk_data(data_list, chunk_size):
    """
    Yields successive chunks from data_list.
    """
    for i in range(0, len(data_list), chunk_size):
        yield data_list[i:i + chunk_size]

def update_database_with_files(files_data):
    """
    Updates the 'iris' table in the database using filenames as primary keys
    and replacing content.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Process data in chunks to optimize memory usage
        chunk_size = 100  # Adjust based on your needs
        for data_chunk in chunk_data(files_data, chunk_size):
            args_str = ','.join(cursor.mogrify("(%s, %s)", (file['filename'], file['content'])).decode('utf-8') for file in data_chunk)
            query = f"""
                INSERT INTO iris (filename, content)
                VALUES {args_str}
                ON CONFLICT (filename)
                DO UPDATE SET content = EXCLUDED.content;
            """
            cursor.execute(query)
            conn.commit()
        cursor.close()
        conn.close()
        logger.info("Database updated with local file data.")
    except Exception as e:
        logger.error(f"Error updating database: {e}")

def read_user_feedback_from_s3(bucket_name, prefix):
    """
    Connects to AWS S3 and reads user feedback files from a specified bucket and prefix.
    """
    s3_client = boto3.client('s3')
    feedback_data = []
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    # Get the object
                    feedback_object = s3_client.get_object(Bucket=bucket_name, Key=key)
                    content = feedback_object['Body'].read().decode('utf-8')
                    feedback_data.append({'key': key, 'content': content})
        logger.info(f"Retrieved {len(feedback_data)} feedback files from S3.")
    except NoCredentialsError:
        logger.error("AWS credentials not available.")
    except ClientError as e:
        logger.error(f"AWS ClientError: {e}")
    except Exception as e:
        logger.error(f"Error reading from S3: {e}")
    return feedback_data

def process_feedback(feedback_data):
    """
    Processes user feedback to update the database or improve prompts.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Example: Update a 'user_feedback' table with the feedback data
        for feedback in feedback_data:
            # Parse the content if it's JSON or structured data
            feedback_content = feedback['content']
            try:
                feedback_json = json.loads(feedback_content)
                user_id = feedback_json.get('user_id', 'anonymous')
                feedback_text = feedback_json.get('feedback_text', '')
            except json.JSONDecodeError:
                # If content is plain text
                user_id = 'anonymous'
                feedback_text = feedback_content

            cursor.execute("""
                INSERT INTO user_feedback (user_id, feedback_text)
                VALUES (%s, %s)
            """, (user_id, feedback_text))
            conn.commit()
        cursor.close()
        conn.close()
        logger.info("Processed and stored user feedback from S3.")
    except Exception as e:
        logger.error(f"Error processing feedback data: {e}")

def main():
    # Read local files
    files_data = read_local_files(LOCAL_FILES_DIRECTORY)

    # Update the database with file data
    if files_data:
        update_database_with_files(files_data)
    else:
        logger.info("No local files to process.")

    # Read user feedback from S3
    feedback_data = read_user_feedback_from_s3(S3_BUCKET_NAME, S3_FEEDBACK_PREFIX)

    # Process feedback data
    if feedback_data:
        process_feedback(feedback_data)
    else:
        logger.info("No feedback data to process from S3.")

if __name__ == "__main__":
    main()
