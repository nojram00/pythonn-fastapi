# Here are the steps on running this server
- Create a virtual environment by running `python -m venv .venv` or `python3 -m venv .venv` for linux.
- Run the virtual environment by one of these commands:
    - `.venv\scripts\activate` if you are using windows
    -  `source .venv/bin/activate` if you are on linux
- Install dependecies by running `pip install -r requirements.txt`
- Run the server by using `uvicorn app:app --host 0.0.0.0 --port 8000` or `fastapi run app.py` 