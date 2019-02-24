# Generic Receipt Parser Service

Source code for creating a generic receipt parser service using Flair

## Step 1: Create and activate a Python 3.6 virtualenv

Create a Python 3.6 virtualenv

    $ python3.6 -m venv flair-venv

 Activate the virtualenv

    $ source flair-venv/bin/activate

Verify the installation

    (flair-venv) $ python --version

Output:

    Python 3.6.x


## Step 2: Install requirements

    $ pip install flair flask 


## Step 3: Start service

    $ export FLASK_ENV=development
    $ export FLASK_APP=app.py
    $ flask run


## Step 4: Send a request

```
curl --request POST \
  --url http://localhost:5000/api/v1/parseReceipt \
  --header 'content-type: application/json' \
  --data '{
    "receipt": "123 My Street\nSpringfield, CA 12345\nStore #888 02/25/19 10:10am\n"
}'
```

Output:

```
[
  {
    "LINE_0": {
      "entities": [
        {
          "confidence": 0.9999480247497559, 
          "end_pos": 13, 
          "start_pos": 0, 
          "text": "123 My Street", 
          "type": "ADD"
        }
      ], 
      "labels": [], 
      "text": "123 My Street"
    }
  }, 
  {
    "LINE_1": {
      "entities": [
        {
          "confidence": 0.9999769926071167, 
          "end_pos": 12, 
          "start_pos": 0, 
          "text": "Springfield,", 
          "type": "CIT"
        }, 
        {
          "confidence": 0.9950789213180542, 
          "end_pos": 15, 
          "start_pos": 13, 
          "text": "CA", 
          "type": "STA"
        }, 
        {
          "confidence": 0.9999833106994629, 
          "end_pos": 21, 
          "start_pos": 16, 
          "text": "12345", 
          "type": "POS"
        }
      ], 
      "labels": [], 
      "text": "Springfield, CA 12345"
    }
  }, 
  {
    "LINE_2": {
      "entities": [
        {
          "confidence": 0.9999828338623047, 
          "end_pos": 19, 
          "start_pos": 11, 
          "text": "02/25/19", 
          "type": "DAT"
        }, 
        {
          "confidence": 1.0, 
          "end_pos": 27, 
          "start_pos": 20, 
          "text": "10:10am", 
          "type": "TIM"
        }
      ], 
      "labels": [], 
      "text": "Store #888 02/25/19 10:10am"
    }
  }
]

```
