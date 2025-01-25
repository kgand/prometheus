from connect import db
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
parkcams = db.parkcams

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"])


def parse_document(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/allcams")
def read_allcams():
    try:
        print("Finding all cameras...")
        all_documents = parkcams.find({})
        all_parkcams = [parse_document(doc) for doc in all_documents]
        print(f"found {len(all_parkcams)} cameras")

        return all_parkcams
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(status_code=500, detail="failed to retrieve park cams")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
