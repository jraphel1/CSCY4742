from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("cybersec_chat_format_cleaned_train.jsonl", "rb") as train_file:
    training_file = client.files.create(
        file=train_file,
        purpose="fine-tune"
    )
    
with open("cybersec_chat_format_cleaned_val.jsonl", "rb") as val_file:
    validation_file = client.files.create(
        file=val_file,
        purpose="fine-tune"
    )
    
fine_tuning_job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    validation_file=validation_file.id,
    model="gpt-3.5-turbo",
    hyperparameters={
        "n_epochs": 3
    }
)

print(f"Fine-tuning job created: {fine_tuning_job.id}")

def check_status(job_id):
    job = client.fine_tuning.jobs.retrieve(job_id)
    print(f"Status: {job.status}")
    return job

def list_events(job_id):
    events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id)
    for event in events.data:
        print(f"{event.created_at}: {event.message}")
        
def use_fine_tuned_model(model_id):
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "user", "content": "Identify cybersecurity tactics and techniques in the following text:\n\nThe attackers first performed reconnaissance on the network before use process injection to evade detection."}
        ]
    )
    print(response.choices[0].message.content)
    
job = check_status(fine_tuning_job.id)

print("\nShowing how to check events (you can run this periodically):")
list_events(fine_tuning_job.id)


