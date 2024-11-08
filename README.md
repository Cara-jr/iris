# Iris AI Chatbot

An AI chatbot implemented using Python, AWS Lambda, AWS S3, AWS SNS, SMTP, PostgreSQL, and Anthropic's Claude 3 AI model via API. The project includes user interaction via a web interface, feedback collection with ratings and comments, email notifications, daily updates processing local files and AWS S3 feedback, standardized error handling, AWS integration, and unit tests.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Error Codes](#error-codes)
- [Security Considerations](#security-considerations)
- [License](#license)
- [Additional Resources](#additional-resources)
- [Contact Information](#contact-information)

---

## Project Overview

The Iris AI Chatbot is a conversational AI application that leverages Anthropic's Claude 3 model to interact with users, collect feedback, and provide automated email notifications. The project is designed to be scalable and secure, utilizing AWS services such as Lambda, S3, SNS, and IAM roles.

---

## Features

- **Chatbot Interaction**: Users can interact with the AI chatbot via a web interface.
- **Feedback Collection**: After each interaction, users can provide a rating (1-5) and an optional comment.
- **Email Notifications**: Users can opt to receive a copy of the conversation via email.
- **Daily Updates**: A script processes local files and user feedback from AWS S3.
- **Error Handling**: Standardized error responses with appropriate HTTP status codes.
- **AWS Integration**: Utilizes AWS S3, SNS, and IAM roles for resource management and security.
- **Unit Tests**: Comprehensive unit tests for Lambda functions.

---

## Project Structure

project/ ├── lambda_functions/ │ ├── chatbot_function/ │ ├── email_function/ │ └── layers/ ├── database/ ├── front_end/ ├── config/ ├── tests/ └── README.md


- **lambda_functions/**: Contains AWS Lambda functions for the chatbot and email functionalities.
- **database/**: Contains the database initialization script and daily update script.
- **front_end/**: Contains the front-end code (HTML, CSS, JS) for interacting with the chatbot.
- **config/**: Contains configuration files for development and production environments.
- **tests/**: Contains unit tests for the Lambda functions.
- **README.md**: Project documentation.

---

## Prerequisites

- **Python**: Version 3.8 or higher.
- **PostgreSQL**: Installed locally or access to a PostgreSQL server.
- **AWS Account**: With permissions to create Lambda functions, S3 buckets, SNS topics, and IAM roles.
- **AWS CLI**: Installed and configured.
- **Anthropic API Key**: Access to Anthropic's Claude 3 API.
- **SMTP Server Credentials**: For sending emails (e.g., Gmail SMTP).
- **Node.js and npm**: For any front-end package management (optional).

---

## Setup Instructions

1. **AWS Resources**: Create necessary AWS resources (IAM roles, S3 buckets, SNS topics) with appropriate permissions.

2. **Database Setup**: Run the `init_db.sql` script to create the database and tables.

3. **Configuration**: Update configuration files in the `config/` directory with your settings.

4. **Environment Variables**: Set environment variables required by the application.

5. **Install Dependencies**: Install Python dependencies for the Lambda functions and any front-end dependencies if necessary.

---

## Usage

- **Chatbot Function**: Deploy and invoke the chatbot Lambda function via AWS API Gateway or test locally using provided scripts.

- **Email Function**: Ensure the email Lambda function is subscribed to the SNS topic to handle email notifications.

- **Front-End**: Open `index.html` in a web browser to interact with the chatbot. Update API endpoints in `app.js` if necessary.

- **Daily Update Script**: Run `daily_update.py` to process local files and user feedback from AWS S3.

- **Unit Tests**: Run unit tests in the `tests/` directory to verify functionality.

---

## Error Codes

The application uses standard HTTP status codes:

- **200 OK**: The request was successful.
- **400 Bad Request**: The request was invalid or missing parameters.
- **500 Internal Server Error**: An error occurred on the server side.

---

## Security Considerations

- **Credentials Management**: Do not hard-code sensitive credentials. Use environment variables or AWS Secrets Manager.

- **AWS IAM Roles**: Grant minimal required permissions and regularly review IAM policies.

- **Database Security**: Use strong passwords and limit user permissions.

- **Data Protection**: Encrypt sensitive data and be cautious with logging.

---

## License

This project is licensed under the MIT License.

---

## Additional Resources

- **Anthropic API Documentation**: [Anthropic API Docs](https://www.anthropic.com/)
- **AWS Lambda Documentation**: [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/)
- **AWS S3 Documentation**: [AWS S3 Docs](https://docs.aws.amazon.com/s3/)
- **AWS SNS Documentation**: [AWS SNS Docs](https://docs.aws.amazon.com/sns/)
- **PostgreSQL Documentation**: [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## Contact Information

For any questions or issues, please contact the project maintainer.

---

**Note**: Replace placeholder values in configuration files with your actual settings.

