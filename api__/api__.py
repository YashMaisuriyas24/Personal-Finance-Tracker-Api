from fastapi import FastAPI, HTTPException
from bson import ObjectId
from db__.db1__ import DB
from models.transaction import TransactionCreate
from models.category import CategoryCreate, CategoryUpdate

app = FastAPI()
db = DB()

@app.post("/transactions")
def create_transaction(transaction: TransactionCreate):
    data = transaction.model_dump()
    result = db.create_transaction(data)
    return {"message": result}


@app.get("/transactions")
def get_all_transactions():
    data = db.get_all_transactions()

    result = []
    for item in data:
        item["_id"] = str(item["_id"])
        result.append(item)

    return result


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):
    data = db.transactions.find_one({"_id": ObjectId(transaction_id)})

    if not data:
        raise HTTPException(status_code=404, detail="Transaction not found")

    data["_id"] = str(data["_id"])
    return data


@app.patch("/transactions/{transaction_id}")
def update_transaction(transaction_id: str, transaction: TransactionCreate):
    data = transaction.model_dump()

    db.update_transaction(ObjectId(transaction_id), data)

    return {"message": "Transaction Updated"}


@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: str):
    db.delete_transaction(ObjectId(transaction_id))
    return {"message": "Transaction Deleted"}



@app.post("/categories")
def create_category(category: CategoryCreate):
    data = category.model_dump()
    result = db.create_category(data)
    return {"message": result}


@app.get("/categories")
def get_categories():
    data = db.get_all_categories()

    for item in data:
        item["_id"] = str(item["_id"])

    return data


@app.patch("/categories/{name}")
def update_category(name: str, category: CategoryUpdate):
    data = category.model_dump(exclude_none=True)

    db.update_category(name, data)

    return {"message": "Category Updated"}


@app.delete("/categories/{name}")
def delete_category(name: str):
    db.delete_category(name)
    return {"message": "Category Deleted"}


