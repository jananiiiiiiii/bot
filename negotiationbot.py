from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import numpy as np
app = FastAPI()
openai.api_key = "sk-SQtRCop-IRvcpw_nUIABkyAd91yD4lxCVt8Kc5IpUjT3BlbkFJT4XDwqBLUHjGjMPYfC6m-G81s-aTunv-Vc1njFQ1QA"
price_range = (100, 200)
class NegotiationRequest(BaseModel):
    price: int

class NegotiationResponse(BaseModel):
    response: str
def negotiate_price(user_input: int):
    if user_input < price_range[0]:
        return f"Sorry, our minimum price is ${price_range[0]}"
    elif user_input > price_range[1]:
        return f"Sorry, our maximum price is ${price_range[1]}"
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant for price negotiation."},
                {"role": "user", "content": f"Negotiate a price for the product. The user has proposed {user_input} dollars."}
            ],
            max_tokens=100
        )
        response_text = response.choices[0].message['content'].strip()

        discount = np.random.uniform(0, 0.2)
        counteroffer = user_input * (1 - discount)
        return f"{response_text}. We can offer you a discount of ${counteroffer:.2f}"

@app.post("/negotiate", response_model=NegotiationResponse)
async def negotiate(request: NegotiationRequest):
    user_price = request.price
    response_text = negotiate_price(user_price)
    return NegotiationResponse(response=response_text)

@app.post("/accept", response_model=NegotiationResponse)
async def accept(request: NegotiationRequest):
    user_price = request.price
    return NegotiationResponse(response=f"Congratulations, you've accepted our offer of ${user_price}!")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
