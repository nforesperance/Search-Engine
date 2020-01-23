# Search-Engine
A custom search engine built with python (Django) and google api client
## Installation and Set Up
#### Creating a Virtual Environment 
**Intallation**
```bash
pip install virtualenvwrapper-win
```
**creating**
on the command line (example for creating a virtual environment named **search**)
```bash
> mkvirtualenv search
```
This should activate the Environment by default. If not you can activate it with the command 
```bash
> workon search
```
### Installing Dependecies
In the virtual env write the command
```bash
> pip install -r requirements.txt
```
### Running the App
While in the virtual env and in the root of the project, write the following command:
```bash
> python manage.py runserver
```
You can see the project by going to **localhost:8000/search** on the browser.
