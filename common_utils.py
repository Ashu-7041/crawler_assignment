from datetime import datetime
from functools import wraps

from db.mongodb import MongoDB


def log_to_mongo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        job_id = kwargs.get("job_id")
        mongo = MongoDB(db_name="celery_jobs")
        # Insert job document
        insertion_id = mongo.insert_document(
            collection="celery_tasks",
            document={
                "job_id": job_id,
                "status": 'running',
                "created_at": datetime.now(),
                "task_name": func.__name__,
                "error": None,
            },
        )
        # Execute the main function and log the status
        try:
            func(*args, **kwargs)  # Run the decorated function
            status = 'completed'
            error = None
        except Exception as e:
            status = 'failed'
            error = str(e)
        finally:
            # Update the MongoDB document with the final status
            mongo.find_update_document(
                collection="celery_tasks", document_id=insertion_id, update_dict={"status": status, "error": error}
            )
            mongo.close()

    return wrapper