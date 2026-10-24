# CloudScale
## A Serverless Cloud-Based Distributed Data Processing and Workload Management System Using AWS

CloudScale is an educational M.E.-level project demonstrating asynchronous job submission, queue-based workload distribution, serverless processing, status tracking, and result storage. It does not use AI or machine learning.

### AWS services
- Amazon API Gateway: REST endpoints
- AWS Lambda: job submission, worker, and status retrieval
- Amazon SQS: asynchronous job queue and dead-letter queue
- Amazon DynamoDB: job metadata and status
- Amazon S3: input and output JSON
- Amazon CloudWatch: logs and operational troubleshooting
- AWS SAM / CloudFormation: infrastructure as code

### Architecture
```text
Client / Dashboard
       |
       v
API Gateway ---> Submit Lambda ---> S3 (input JSON)
                       |              |
                       v              v
                  DynamoDB         SQS Queue
                                      |
                                      v
                                 Worker Lambda
                                  /          \
                                 v            v
                         DynamoDB status   S3 result JSON

API Gateway ---> Get Job Lambda ---> DynamoDB + S3 result
```

### Features
1. Submit JSON records through `POST /jobs`.
2. Persist the input and create a `QUEUED` job.
3. Process jobs asynchronously from SQS with Lambda.
4. Track `QUEUED`, `PROCESSING`, `COMPLETED`, and `FAILED` states.
5. Calculate record counts, missing values, and numeric min/max/mean summaries.
6. Retrieve job status and results through `GET /jobs/{jobId}`.
7. Includes a simple browser dashboard and unit tests.

### Repository layout
```text
CloudScale/
├── backend/
│   ├── submit_job/app.py
│   ├── worker/app.py
│   ├── get_job/app.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── events/sample-job.json
├── tests/test_processor.py
├── template.yaml
├── samconfig.toml.example
├── .gitignore
└── LICENSE
```

### Requirements
- AWS account and AWS CLI credentials
- Python 3.12
- AWS SAM CLI
- Git

### Deploy
Run these commands from the project root:
```bash
sam validate --lint
sam build
sam deploy --guided
```
Suggested stack name: `cloudscale-dev`. Allow SAM to create IAM roles when prompted. Choose your preferred AWS region and save the deployment configuration.

Copy the `ApiUrl` output after deployment. Open `frontend/index.html` in a browser and paste the base URL. The dashboard is not hosted by the template; you can optionally host it with S3 and CloudFront.

### API examples

Submit:
```http
POST /jobs
Content-Type: application/json
```
```json
{
  "records": [
    {"department": "Sales", "amount": 120},
    {"department": "IT", "amount": 250},
    {"department": null, "amount": 180}
  ]
}
```

Example response (`202 Accepted`):
```json
{
  "jobId": "generated-job-id",
  "status": "QUEUED",
  "message": "Job accepted for asynchronous processing."
}
```

Check status:
```http
GET /jobs/{jobId}
```

### Run tests locally
```bash
python -m unittest discover -s tests -v
```
The processor logic is separated from AWS calls, so the unit tests do not require AWS credentials.

### Security and cost notes
This is a learning scaffold, not a production-ready service. AWS resources may incur charges. Set a budget alert, use a test account, and delete the stack when finished. Empty the S3 bucket before deleting the stack if it contains objects. Before production, add authentication (for example, Cognito), restrict CORS to your frontend origin, set request limits, add idempotency handling, configure alarms and DLQ monitoring, and review IAM permissions.

### GitHub upload
1. Create a GitHub repository named `CloudScale`.
2. Extract this ZIP and open a terminal in the extracted folder.
3. Run:
```bash
git init
git add .
git commit -m "Initial CloudScale serverless project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/CloudScale.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username.

### Resume description
**CloudScale — Serverless Distributed Data Processing and Workload Management System**
- Designed an asynchronous serverless workflow using AWS Lambda, API Gateway, SQS, DynamoDB, and S3.
- Implemented job submission, queue-based worker execution, status tracking, and result retrieval through REST APIs.
- Added unit tests and infrastructure-as-code deployment using AWS SAM.

Only claim cloud deployment or performance results after you have actually deployed and tested the system.
