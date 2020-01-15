import os
import json
from redis_conn import RedisConn
from src.trainer import Trainer


RedisConn.initialize('redis', 6379)

data = RedisConn.CONN.blpop('training-queue') # blocking operation until data enters queue
training_data = json.loads(data[1]) # load json string from redis

data_path = os.path.join('/', 'data', training_data['username'], training_data['project'], 'data')
model_path = os.path.join('/', 'data', training_data['username'], training_data['project'], 'models')
log_path = os.path.join('/', 'data', training_data['username'], training_data['project'], 'logs')

training_runs = {
    "run_1": {
        "pre-trained": True,

        "augmentation": {

        },
        "test_size": .20,
        "batch_size": 32, # batch size needs to be divisible by (batch_offset + 1)
        "epochs": 50
    },
    "run_2": {
        "pre-trained": True,
        "greyscale": False,
        "augmentation": {
            "flip_left_right": True,
            "blur": 2, # creates n blured images increasing in fuzzyness,
            "rotate_random_25": 2,
        },
        "test_size": .20,
        "batch_size": 32, # batch size needs to be divisible by (batch_offset + 1)
        "epochs": 50
    }
}

for i, run in enumerate(training_runs):
    run_key = training_runs.get(run)
    T = Trainer(data_path=data_path, model_path=model_path, log_path=log_path, batch_size=run_key.get('batch_size'),
                epochs=run_key.get('epochs'),
                test_size=run_key.get('test_size'),
                run_number=i,
                run_parameters=run_key)
    T.train()

