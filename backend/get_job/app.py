import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")
TABLE = dynamodb.Table(os.environ["JOBS_TABLE"])
BUCKET = os.environ["DATA_BUCKET"]


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
    job_id = (event.get("pathParameters") or {}).get("jobId")
    if not job_id:
        return response(400, {"error": "jobId is required."})
    try:
        item = TABLE.get_item(Key={"jobId": job_id}).get("Item")
        if not item:
            return response(404, {"error": "Job not found.", "jobId": job_id})
        output = {
            "jobId": item["jobId"], "status": item["status"],
            "createdAt": item.get("createdAt"), "updatedAt": item.get("updatedAt"),
            "recordCount": item.get("recordCount"),
        }
        if item.get("status") == "COMPLETED" and item.get("resultKey"):
            obj = s3.get_object(Bucket=BUCKET, Key=item["resultKey"])
            output["result"] = json.loads(obj["Body"].read().decode("utf-8"))
        if item.get("status") == "FAILED":
            output["error"] = item.get("errorMessage", "Processing failed.")
        return response(200, output)
    except ClientError:
        print("Failed to retrieve job", {"jobId": job_id})
        return response(500, {"error": "Unable to retrieve job status."})
