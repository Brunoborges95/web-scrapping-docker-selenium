docker build -t lambda-selenium:v1 .
docker tag lambda-selenium:v1 324430962407.dkr.ecr.us-east-1.amazonaws.com/lambda-selenium
docker push 24430962407.dkr.ecr.us-east-1.amazonaws.com/lambda-selenium:latest 