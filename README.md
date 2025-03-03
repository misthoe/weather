A simple FastAPI application that gets weather information from the yr.no REST API

To run application:

Clone repository with
git clone https://github.com/misthoe/weather.git

Run following command following commands to create a python virutal environment for the project:

cd path/to/your/project-directory
Check that python is installed by running:
python --version or python3 --version
which should give you an output similar to:
Python 3.x.x if python is installed

To create virutal environment:

python3 -m venv myenv

To activate venv:
On macOS/Linux: source myenv/bin/activate
On Windows command prompt: myenv\Scripts\activate 
On Windows Powershell:.\myenv\Scripts\Activate.ps1

After activation of venv the cmd prompt should look like this:

(myenv) user@hostname:~/path/to/your/project-directory$ (linux/macOS) after activation

(myenv) PS C:\Users\YourName\path\to\your\project-directory> (Powershell after venv activation)

To install the project requirements once a venv is up:
(myenv) user@hostname:~/path/to/your/project-directory$ pip install -r requirements.txt

To run application: 
(myenv) user@hostname:~/path/to/your/project-directory$ uvicorn main:app --reload

You can test the API either by using curl:
curl -X 'GET' 'http://127.0.0.1:8000/weather?city_name=Stockholm'  -H 'accept: application/json'

Or directly from browser:
http://127.0.0.1:8000/weather?city_name=Stockholm

Docs can be found at:http://127.0.0.1:8000/docs

