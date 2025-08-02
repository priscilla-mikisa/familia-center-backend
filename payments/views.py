from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .mpesa_utils import mpesa
from django.views.decorators.csrf import csrf_exempt
import json



def initiate_payment(request):
    phone = request.POST.get('phone')  # Format: 2547XXXXXXXX
    amount = request.POST.get('amount')
    
    response = mpesa.stk_push(
        phone_number=phone,
        amount=amount,
        account_reference='ORDER_123',
        transaction_desc='Payment for services',
        callback_url=settings.MPESA_CONFIG['CALLBACK_URL']
    )
    
    return JsonResponse({
        'response': response,
        'checkout_request_id': response['CheckoutRequestID']
    })
    
@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        result_code = data['Body']['stkCallback']['ResultCode']
        
        if result_code == 0:
            # Successful payment
            return JsonResponse({'status': 'success'})
        else:
            # Failed payment
            return JsonResponse({'status': 'failed'}, status=400)
    
    return JsonResponse({'status': 'invalid request'}, status=400)