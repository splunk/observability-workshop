# Agentic AI Demo Application 

## Run Locally 

### Prerequisites

* Python 3.9+ 

### Create Virtual Environment 

Create a virtual environment and then activate it: 

``` bash
python -m venv venv
source venv/bin/activate
```

### Add Packages

``` bash
pip install -r requirements.txt
```
### Define Environment Variables

Add an `.env` file with the following environment variables: 

````
OPENAI_API_KEY=your_key_here
PAYMENT_GATEWAY_API_KEY=replace_me
NOTIFICATION_API_KEY=replace_me
````

> Note: ensure this file isn't added to GitHub 

### Run the Application 

Use the following command to run the application: 

``` bash
python app.py 
```
