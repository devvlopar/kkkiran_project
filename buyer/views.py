import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail
from random import randrange
from django.conf import settings
from seller.models import *
# Create your views here.

def index(request):
    all_pros = Product.objects.all()
    try:
        #jyare login karel hoy
        buyer_row = Buyer.objects.get(email = request.session['email'])
        return render(request, 'index.html', {'user_data':buyer_row, 'all_products':all_pros})
    except:
        #jyare login nathi karyu
        return render(request, 'index.html', {'all_products': all_pros})

def about(request):
    try:
        buyer_row = Buyer.objects.get(email = request.session['email'])
        return render(request, 'about.html', {'user_data': buyer_row})
    except:
        return render(request, 'about.html')

def faqs(request):
    return render(request, 'faqs.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def add_row(request):
    Buyer.objects.create(
        first_name = 'kiran',
        last_name = 'patel',
        email = 'kiran@gmail.com',
        password = 'tops@123',
        address = '201,society, road, surat',
        mobile = '9089786756',
        gender = 'male'
    )
    return HttpResponse('row create thai gai')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        try:
            # Buyer.objects.get(email = request.POST['email'])
            return render(request, 'register.html', {'msg': 'Email Is Already registered!!'})
        except:
            if request.POST['password'] == request.POST['repassword']:
                s = "Ecommerce Registration!!"
                global user_data
                user_data = [request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password']]
                global c_otp
                c_otp = randrange(1000,9999)
                m = f'Hello User!!\nYour OTP is {c_otp}'
                f = settings.EMAIL_HOST_USER
                r = [request.POST['email']]
                send_mail(s, m, f, r)
                return render(request, 'otp.html', {'msg': 'Check Your MailBox'})
            else:
                return render(request, 'register.html', {'msg': 'Both Passwords do not match!!'})


def otp(request):
   
    if str(c_otp) == request.POST['u_otp']:
        Buyer.objects.create(
            first_name = user_data[0],
            last_name = user_data[1],
            email = user_data[2],
            password = user_data[3]
        )
        return render(request, 'register.html', {'msg': 'Account created successfully!!'})
    else:
        return render(request, 'otp.html', {'msg': 'Wrong OTP enter again!!'})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            #email check thay che
            buyer_row = Buyer.objects.get(email = request.POST['email'])
            
            #password check thay chhe
            # request.POST['password'] ###aa password tame login page ma enter karyo hase
            # buyer_row.password ###aa password database wado chhe
            if request.POST['password'] == buyer_row.password:
                #password sacho enter karyo chhe
                request.session['email'] = request.POST['email'] #login thai gayu/ session naam na glass ma email(je login na page par enter karyo hato e) mukaai gayo
                return redirect('index')
            else:
                return render(request, 'login.html', {'msg': 'Wrong Password!!'})
            
        except:
            #jyare email madyo nathi
            return render(request, 'login.html',{'msg':'email is not registered!!'})


def logout(request):
    # session mathi email kadhvano code 
    del request.session['email']

    # ab yahan se index funciton ki jawab daari hai
    return redirect('index')




def add_to_cart(request, pk):
    p_obj = Product.objects.get(id = pk)
    b1 = Buyer.objects.get(email = request.session['email'])
    Cart.objects.create(
        product_name = p_obj.product_name,
        price = p_obj.price,
        pic = p_obj.pic,
        buyer = b1
    )
    return redirect('index')


def del_cart_item(request, c_item):
    c_obj = Cart.objects.get(id = c_item)
    c_obj.delete()
    return redirect('cart')





# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))





@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = t_amount * 100 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
                    # 1. cart na rows delete
                    # for i in c_list:
                        # i.delete()

                    # 2. products na stock -1

					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()



def cart(request):
    u1 = Buyer.objects.get(email = request.session['email'])
    global c_list
    c_list = Cart.objects.filter(buyer = u1)
    global t_amount
    t_amount = 0
    for i in c_list:
        t_amount += i.price
    
    #Payment Nu button Jivit karva mate no code 
    currency = 'INR'
    # print(t_amount * 100)
    amount = t_amount * 100 # total amount nu paisa wadu version accept kare chhe

	# Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context.update( {'user_data':u1, 'my_cart_data': c_list, 'total_amount':t_amount})


    return render(request, 'cart.html' ,context=context)