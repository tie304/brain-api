import os
import json
import sys
import datetime
import traceback
from pymodm import connect
from redis_conn import RedisConn
from src.trainer import Trainer
from database.training import TrainingInstance, TrainingRun
from database.classification_project import ClassificationProject


# connect to redis and mongo
RedisConn.initialize(os.environ.get('REDIS_HOST'), os.environ.get('REDIS_PORT'))
connect(os.environ.get('MONGO_URI') + os.environ.get("MONGO_DB_NAME"))

# blocking operation until data enters queue
data = RedisConn.CONN.blpop('training-queue')
# load json string from redis
training_data = json.loads(data[1])

# query project
project = ClassificationProject.objects.get({'_id': training_data.get('project_id')})
with open('training_runs.json') as f:
    training_runs = json.loads(f.read())

# find specific training instance from the project object
training_instance = None
for instance in project.training_instances:
    if instance._id == training_data.get('training_instance_id'):
        training_instance = instance

# set the status in the database
training_instance.status = "training"
project.save()


data_path = os.path.join('/', 'data', training_data['username'], training_data['project_name'], 'data')
model_path = os.path.join('/', 'data', training_data['username'], training_data['project_name'], 'models')
log_path = os.path.join('/', 'data', training_data['username'], training_data['project_name'], 'logs')


try:
    for i, run in enumerate(training_runs):
        tr = TrainingRun()
        run_key = training_runs.get(run)
        print(run, "RUN")
        T = Trainer(data_path=data_path, model_path=model_path, log_path=log_path,
                    run_number=i,
                    run_parameters=run_key)
        training_history = T.train()
        tr.epochs = training_history.get('epochs')
        # converts numpy <float32> to python <Float>
        tr.val_accuracy = [val.item() for val in training_history.get('history').get('val_accuracy')]
        tr.training_accuracy = [val.item() for val in training_history.get('history').get('accuracy')]
        tr.val_loss = [val.item() for val in training_history.get('history').get('val_loss')]
        tr.training_loss = [val.item() for val in training_history.get('history').get('loss')]
        tr.training_end_time = datetime.datetime.now()

        training_instance.training_runs.append(tr)
        project.save()

    training_instance.status = "complete"

    project.save()
except Exception as e:
    print("TRAINING FAILED:\n", traceback.format_exc())
    training_instance.status = "training_failed"
    project.save()

sys.exit(0)