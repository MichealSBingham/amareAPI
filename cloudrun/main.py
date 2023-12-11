from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    # Your existing function code here
    # You can access parameters using request.query_params
    return {"message": "Hello from Cloud Run!"}