# CloudScale
### A Serverless Cloud-Based Distributed Data Processing and Workload Management System Using AWS

CloudScale is an advanced M.E. Software Systems project that demonstrates how to submit, queue, process, and monitor data-processing jobs using AWS serverless services.

## Key Features
- Asynchronous job submission and processing
- Distributed workload management using a message queue
- Real-time job status tracking
- Input and output storage using Amazon S3
- Job metadata management using Amazon DynamoDB
- Error handling and dead-letter queue support
- Automated deployment using AWS SAM

## AWS Services
- **Amazon API Gateway** — Exposes REST API endpoints
- **AWS Lambda** — Executes job submission, processing, and status retrieval
- **Amazon SQS** — Manages asynchronous job queues
- **Amazon DynamoDB** — Stores job metadata and status
- **Amazon S3** — Stores input and output data
- **Amazon CloudWatch** — Supports logging and troubleshooting
- **AWS SAM** — Defines and deploys cloud resources

## Architecture
1. A user submits a processing job through the API.
2. API Gateway routes the request to a Lambda function.
3. The job is added to an SQS queue.
4. A worker processes the job asynchronously.
5. Job status and results are stored in DynamoDB and S3.
6. The user retrieves job status and results through the API.

## Project Structure
- `backend/` — API and worker functions
- `events/` — Sample event payloads
- `frontend/` — User interface
- `tests/` — Unit tests
- `template.yaml` — AWS SAM infrastructure definition

## Getting Started
1. Install Python and the AWS SAM CLI.
2. Configure AWS credentials in your development environment.
3. Review `template.yaml` and `samconfig.toml.example`.
4. Follow the deployment and testing instructions in the project files.

## Project Goals
- Demonstrate serverless application design
- Explore asynchronous processing and workload management
- Practice cloud infrastructure as code
- Build a scalable foundation for distributed data-processing workloads

## Technologies
Python · AWS Lambda · Amazon API Gateway · Amazon SQS · Amazon DynamoDB · Amazon S3 · AWS SAM

## Academic Project
Developed as part of the M.E. Software Systems program.