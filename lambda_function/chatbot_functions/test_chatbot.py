import json
import os
from lambda_function import lambda_handler

# Set environment variables for testing
os.environ['ENV'] = 'dev'
os.environ['ANTHROPIC_API_KEY'] = 'your_anthropic_api_key'
os.environ['SNS_TOPIC_ARN'] = 'your_sns_topic_arn'

event = {
    'user_input': 'How can I improve my time management skills?',
    'user_id': 'user_123',
    'user_email': 'user@example.com',
    'feedback_rating': 5,
    'feedback_comment': 'Very helpful!'
}

context = {}

response = lambda_handler(event, context)
print(response)
print(json.loads(response['body']))
