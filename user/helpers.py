from kavenegar import *

def send_sms(code,phone):
    api = KavenegarAPI('')
    params = { 
        'receptor': phone,
        'message' :f"""
                            سلام کد ورود شما جهت اعتبار سنجی

                            {code}
        """}
    response = api.sms_send( params)
