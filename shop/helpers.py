import json
import requests
from decouple import config
from .models import Order

def pay_with_idpay(user):
    headers = {
        "X-API-KEY":config("IDPAY_APIKEY"),
        "X-SANDBOX":"true"
        }
    order = Order.objects.get(user=user,is_ordered=False)
    data = {
        "order_id": order.id,
        "amount":order.total_order_price,
        "phone":user.phone,
        "callback":"http://127.0.0.1:8000/api/checkout/"
    }
    response = requests.post("https://api.idpay.ir/v1.1/payment",json=data,headers=headers)
    print(response)
    dic = json.loads(response.content)
    return dic