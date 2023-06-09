import os

from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float
    quantity: int

class Order(BaseModel):
    customer_name: str
    customer_email: str
    products: list[Product] = Field(..., min_items=1)

@app.post("/buy")
async def buy_product(order: Order):
    # Send a message to Azure Service Bus
    conn_str = os.getenv("SERVICE_BUS_CONNECTION_STRING")
    queue_name = "invoices"
    message = ServiceBusMessage(order.json())

    async with ServiceBusClient.from_connection_string(conn_str) as client:
        async with client.get_queue_sender(queue_name) as sender:
            await sender.send_messages(message)

    return {"message": "Product purchase request sent."}
