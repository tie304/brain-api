# brain-api
Distributed web application for training and deploying neural networks. Currently offers a bare bones way of collecting image data from Google Images and training a classifer on those images. This project uses [FastAPI](https://fastapi.tiangolo.com/), [Tensorflow](https://www.tensorflow.org/) and [MongoDB](https://www.mongodb.com/)

## Getting Started
1. Install [Docker](https://www.docker.com/)
2. Clone Repo
```
git clone https://github.com/tie304/brain-api.git
```
3. Create .env file with following parameters
```
AUTH_SECRET_KEY=secret
AUTH_ALGORITHM=HS256
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES=120
```
NOTE: Do not commit these values and change key to a more secure string

4. Run
- Development: this will serve the app on http://localhost:8000 and restart the server when changes are made
```
sudo docker-compose up
```


- Production: This will serve the app on port 80 and when changes are made will not restart server
```
sudo docker-compose -f docker-compose.prod.yml up
```

## Usage
A full API refrence is available at http://{{YOUR_URL_OR_IP}}/docs
### Authentication
1. Sign up
```
var settings = {
  "url": "http://{{YOUR_IP_HERE}}/sign-up",
  "method": "POST",
  "timeout": 0,
  "headers": {
    "Content-Type": "application/json"
  },
  "data": JSON.stringify({"email":"foo@bar.com","name":"Foo","password":"1234"}),
};

$.ajax(settings).done(function (response) {
  console.log(response);
});
```

2. Login 
```
var settings = {
  "url": "http://{{YOUR_IP_HERE}}/login",
  "method": "POST",
  "timeout": 0,
  "headers": {
    "Content-Type": "application/json"
  },
  "data": JSON.stringify({"email":"foo@bar.com","password":"1234"}),
};

$.ajax(settings).done(function (response) {
  console.log(response);
});
```

### Train Neural Network
1. Create project
```
var settings = {
  "url": "http://{{YOUR_IP_HERE}}/projects/classification_project",
  "method": "POST",
  "timeout": 0,
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer {{YOUR_TOKEN_HERE}}"
  },
  "data": JSON.stringify({"name":"cats v dogs","description":"Tells the difference between cats and dogs","classes":[{"label":"cat","search_term":"cat","max_images":1000},{"label":"dog","search_term":"dog","max_images":1000}]}),
};

$.ajax(settings).done(function (response) {
  console.log(response);
});
```
2. Collect Data
```
var settings = {
  "url": "http://{{YOUR_IP_HERE}}/projects/classification_project/collect_google_images?_id={{PROJECT_ID_HERE}}",
  "method": "POST",
  "timeout": 0,
  "headers": {
    "Authorization": "Bearer {{YOUR_TOKEN_HERE}}"
  },
};

$.ajax(settings).done(function (response) {
  console.log(response);
});
```
3. Train: Specify your run parameters and the ID of the project you want to train. NOTE: Make sure data collection is finished.
```
var settings = {
  "url": "http://{{YOUR_IP_HERE}}/train?_id={{YOUR_PROJECT_ID_HERE}}",
  "method": "POST",
  "timeout": 0,
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer {{YOUR_TOKEN_HERE}}"
  },
  "data": JSON.stringify({"run_parameters":{"run_1":{"network":{"model":"base_cnn","activation":"softmax"},"test_size":0.2,"shuffle":true,"batch_size":32,"epochs":50}}}),
};

$.ajax(settings).done(function (response) {
  console.log(response);
});
```

4. Your model is available.
```
/{{PROECT_ROOT}}/data/{{EAMIL}}/{{PROJECT_NAME}}/{{MODELS}}
```
