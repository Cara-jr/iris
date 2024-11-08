import unittest
from unittest.mock import patch, MagicMock
import os
from lambda_function import lambda_handler

class TestEmailFunction(unittest.TestCase):

    @patch('lambda_function.smtplib.SMTP')
    def test_lambda_handler_success(self, mock_smtp):
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Set environment variables
        os.environ['SMTP_SERVER'] = 'smtp.test.com'
        os.environ['SMTP_PORT'] = '587'
        os.environ['SMTP_USERNAME'] = 'test_user'
        os.environ['SMTP_PASSWORD'] = 'test_pass'

        event = {
            'Records': [
                {
                    'Sns': {
                        'Message': 'Test message',
                        'Subject': 'Test subject',
                        'MessageAttributes': {
                            'Recipient': {
                                'Type': 'String',
                                'Value': 'recipient@test.com'
                            }
                        }
                    }
                }
            ]
        }
        context = {}

        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Email(s) processed successfully')

    @patch('lambda_function.smtplib.SMTP')
    def test_lambda_handler_error(self, mock_smtp):
        # Mock SMTP server to raise exception
        mock_smtp.side_effect = Exception("SMTP server error")

        # Set environment variables
        os.environ['SMTP_SERVER'] = 'smtp.test.com'
        os.environ['SMTP_PORT'] = '587'
        os.environ['SMTP_USERNAME'] = 'test_user'
        os.environ['SMTP_PASSWORD'] = 'test_pass'

        event = {
            'Records': [
                {
                    'Sns': {
                        'Message': 'Test message',
                        'Subject': 'Test subject',
                        'MessageAttributes': {
                            'Recipient': {
                                'Type': 'String',
                                'Value': 'recipient@test.com'
                            }
                        }
                    }
                }
            ]
        }
        context = {}

        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 500)
        body = json.loads(response['body'])
        self.assertEqual(body['error'], 'Internal server error')

if __name__ == '__main__':
    unittest.main()
