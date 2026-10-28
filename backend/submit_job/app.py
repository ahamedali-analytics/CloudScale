import json
import os
import uuid
from datetime import datetime, timezone
import boto3

s3 = boto3.client("s3")
sqs = boto3.client("sqs")
dynamodb = boto3.resource("dynamodb")
TABLE = dynamodb.Table(os.environ["JOBS_TABLE"])
BUCKET = os.environ["DATA_BUCKET"]
QUEUE_URL = os.environ["JOB_QUEUE_URL"]
MAX_RECORDS = 10000


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        if not isinstance(body, dict):
                return response(400, {"error": "Request body must be a JSON object."})
        records = body.get("records")
        if not isinstance(records, list) or not records:
            return response(400, {"error": "'records' must be a non-empty JSON array."})
        if len(records) > MAX_RECORDS:
            return response(413, {"error": f"Maximum records per job is {MAX_RECORDS}."})
        if not all(isinstance(row, dict) for row in records):
            return response(400, {"error": "Every record must be a JSON object."})

        job_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        input_key = f"jobs/{job_id}/input.json"
        s3.put_object(
            Bucket=BUCKET, Key=input_key,
            Body=json.dumps(records).encode("utf-8"),
            ContentType="application/json",
        )
        TABLE.put_item(Item={
            "jobId": job_id, "status": "QUEUED", "inputKey": input_key,
            "recordCount": len(records), "createdAt": now, "updatedAt": now,
        })
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({"jobId": job_id, "inputKey": input_key}),
        )
        return response(202, {
            "jobId": job_id, "status": "QUEUED",
            "message": "Job accepted for asynchronous processing.",
        })
    except (json.JSONDecodeError, TypeError):
        return response(400, {"error": "Request body must be valid JSON."})
    except Exception:
        print("Failed to submit job", {"requestId": getattr(context, "aws_request_id", "local")})
        return response(500, {"error": "Unable to submit job. Check CloudWatch logs."})
