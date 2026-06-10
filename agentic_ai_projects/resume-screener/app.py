from fastapi import FastAPI

app = FastAPI()

@app.post("/screen")
def screen_resume():
    pass
