from kavenegar import *
import string
import random


KEY = "YOUR API KEY"

def random_code():
    
    code = ''.join(random.choice(string.digits) for x in range(6))
    
    return code



def send_code(phone_number):
    
    randomCode = random_code()
    
    api = KavenegarAPI(KEY)
    params = { 'sender' : '10008663', 'receptor': str(phone_number), 'message' :'سرویس پیامکی  \n کد 6 رقمی : ' + str(randomCode) }
    response = api.sms_send( params)
    
    
    # ghasedak sms web service ghasedak.me
    
    """
    
    # create an instance:
    sms = ghasedakpack.Ghasedak(KEY)

    # send a single message to a single number:
    sms.send({'message': 'سرویس پیامکی  \n کد 6 رقمی : ' + str(randomCode), 'receptor': phone_number,'linenumber': '10008566', 'senddate': '', 'checkid': ''})
    
    """
    
    return randomCode