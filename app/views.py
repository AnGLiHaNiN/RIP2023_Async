from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import time
import random
import requests

from concurrent import futures

CALLBACK_URL = "http://localhost:8000/api/medicines/"

executor = futures.ThreadPoolExecutor(max_workers=1)
TOKEN = '123456789'


def get_random_status(medicine_id):
    # time.sleep(6) ## Время проверки 6 секунд
    return {
        "medicine_id": medicine_id,
        # "status": bool(random.randint(0, 3)), ## Шанс провала 25%
        "status": True, ## Шанс провала 25%
    }


def status_callback(task):
    try:
        result = task.result()
        print(result)
    except futures._base.CancelledError:
        return

    url = str(CALLBACK_URL+str(result["medicine_id"])+'/verification/')
    requests.put(url, data={"verification_status": result['status'], "token": TOKEN}, timeout=3)


@api_view(['POST'])
def set_status(request):
    if "medicine_id" in request.data.keys():
        medicine_id = request.data["medicine_id"]

        task = executor.submit(get_random_status, medicine_id)
        task.add_done_callback(status_callback)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
