import os
from lambda_function import lambda_handler

# Set environment variables for testing
os.environ['SMTP_SERVER'] = 'smtp.gmail.com'
os.environ['SMTP_PORT'] = '587'
os.environ['SMTP_USERNAME'] = 'your_email@gmail.com'
os.environ['SMTP_PASSWORD'] = 'your_email_password'

event = {
    'Records': [
        {
            'Sns': {
                'Message': 'Your performance report is ready.',
                'Subject': 'Performance Report',
                'MessageAttributes': {
                    'Recipient': {
                        'Type': 'String',
                        'Value': 'recipient@example.com'
                    }
                }
            }
        }
    ]
}

context = {}

response = lambda_handler(event, context)
print(response)
