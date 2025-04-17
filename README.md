# Doccy Backend

A Python backend service built with FastAPI.

## Setup

1. Create a virtual environment
   ```
   python -m venv venv
   ```

2. Activate the virtual environment windows
   ```
   venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip uninstall -r requirements.txt

   pip install -r requirements.txt
   ```

4. Run the application
   ```
   Press F5 in VSCode, this will activate VSCode debugger. If that is not working then enter the following command in terminal -> uvicorn app.main:app --reload
   ```

5. Access the API documentation
   - OpenAPI docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
