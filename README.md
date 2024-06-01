# Shoppin Cart Python Api

1. Create virtual environment  
virtualenv venvFastAPI
source venvFastAPI/bin/activate

pip install fastapi uvicorn[standard]

2. Run application using uvicorn tool
uvicorn main:app --port 8085  --reload

3. In browser, run the url http://localhost:8085/docs# to launch swagger UI    