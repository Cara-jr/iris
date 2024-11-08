import unittest
from unittest.mock import patch, MagicMock
import os
from lambda_function import lambda_handler

class TestChatbotFunction(unittest.TestCase):

    @patch('lambda_function.boto3.client')
    @patch('lambda_function.psycopg2.connect')
    @patch('lambda_function.get_claude_response')
    def test_lambda_handler_success(self, mock_get_claude_response, mock_psycopg2_connect, mock_boto3_client):
        # Mock database connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_psycopg2_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]

        # Mock Claude response
        mock_get_claude_response.return_value = "You can improve time management by prioritizing tasks."

        # Mock SNS client
        mock_sns_client = MagicMock()
        mock_boto3_client.return_value = mock_sns_client

        # Set environment variables
        os.environ['ENV'] = 'dev'
        os.environ['ANTHROPIC_API_KEY'] = 'test_key'
        os.environ['SNS_TOPIC_ARN'] = 'test_sns_topic_arn'

        event = {
            'user_input': 'Test input',
            'user_id': 'user_123',
            'user_email': 'user@example.com',
            'feedback_rating': 5,
            'feedback_comment': 'Excellent!'
        }
        context = {}

        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertIn('response', body)
        self.assertEqual(body['response'], "You can improve time management by prioritizing tasks.")

    @patch('lambda_function.psycopg2.connect')
    def test_lambda_handler_no_input(self, mock_psycopg2_connect):
        # Set environment variables
        os.environ['ENV'] = 'dev'
        os.environ['ANTHROPIC_API_KEY'] = 'test_key'
        os.environ['SNS_TOPIC_ARN'] = 'test_sns_topic_arn'

        event = {
            'user_id': 'user_123',
            'user_email': 'user@example.com',
            'feedback_rating': 4,
            'feedback_comment': 'Good'
        }
        context = {}

        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 400)
        body = json.loads(response['body'])
        self.assertIn('error', body)
        self.assertEqual(body['error'], "user_input is required")

if __name__ == '__main__':
    unittest.main()
