from openai import OpenAI
import os
import openai

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

job_id = input("input job id:\n")

def check_status(job_id):
    job = client.fine_tuning.jobs.retrieve(job_id)
    print(f"Status: {job.status}")
    return job

def list_events(job_id):
    events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id)
    for event in events.data:
        print(f"{event.created_at}: {event.message}")
        
job = check_status(job_id)
list_events(job_id)
jobs = client.fine_tuning.jobs.list(limit=5)

for job in jobs.data:
    if job.status == "succeeded":
        print("Model ID:", job.fine_tuned_model)