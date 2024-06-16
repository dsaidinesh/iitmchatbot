# Streamlit Application with Hugging Face Integration

This repository contains a Streamlit application integrated with Hugging Face, running inside a Docker container. The application demonstrates how to securely manage and use environment variables like the Hugging Face token.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Python 3.9](https://www.python.org/downloads/) (optional, for local development)

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

git clone https://github.com/yourusername/your-repo.git
cd your-repo

### 2. Clone the Repository
add your huggingface access token in .env file
## 3.Build the Docker Image
Build the Docker image using the following command:
docker build -t my-streamlit-app .
### Run the Docker Container
Run the Docker container, passing the environment variables from the .env file:
docker run -it -p 8501:8501 --env-file .env my-streamlit-app
