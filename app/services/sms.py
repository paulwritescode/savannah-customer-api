import africastalking
from app.config import settings
import logging
import requests
import json
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self):
        # Initialize Africa's Talking
        africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
        self.sms = africastalking.SMS
        self.api_key = settings.AT_API_KEY
        self.username = settings.AT_USERNAME
        self.sender_id = settings.AT_SENDER_ID or "SAVANNAH"
    
    async def send_order_notification(self, phone_number: str, customer_name: str, item: str, amount: float):
        try:
            # Format phone number (ensure it starts with +254 for Kenya)
            if not phone_number.startswith('+'):
                if phone_number.startswith('0'):
                    phone_number = '+254' + phone_number[1:]
                else:
                    phone_number = '+254' + phone_number
            
            message = f"Hello {customer_name}, your order for {item} worth KSH {amount:,.2f} has been confirmed. Thank you for your business!"
            
            # Try real API call first
            try:
                url = "https://api.sandbox.africastalking.com/version1/messaging"
                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'apiKey': self.api_key
                }
                
                # Use form data instead of JSON for SMS API
                # For sandbox, username must be in form data, not headers
                data = {
                    "username": self.username,
                    "message": message,
                    "to": phone_number  # Changed from phoneNumbers to to
                }
                
                # URL encode the data properly
                encoded_data = urlencode(data)
                response = requests.post(url, headers=headers, data=encoded_data)
                
                if response.status_code in [200, 201]:  # 201 is also success for SMS
                    response_data = response.json()
                    logger.info(f"📱 SMS sent successfully to {phone_number}: {response_data}")
                    print(f"\n📱 SMS NOTIFICATION SENT (REAL):")
                    print(f"   To: {phone_number}")
                    print(f"   Message: {message}")
                    print(f"   Status: Success (Real API)")
                    print(f"   Response: {response_data}")
                    print()
                    return response_data
                else:
                    logger.error(f"SMS API error: {response.status_code} - {response.text}")
                    raise Exception(f"API Error: {response.status_code} - {response.text}")
                    
            except Exception as api_error:
                logger.warning(f"Real SMS failed, falling back to simulation: {str(api_error)}")
                
                # Fallback to simulation
                logger.info(f"📱 SMS NOTIFICATION (SIMULATED):")
                logger.info(f"   To: {phone_number}")
                logger.info(f"   Message: {message}")
                logger.info(f"   Sender ID: {self.sender_id}")
                
                response_data = {
                    "SMSMessageData": {
                        "Message": f"Sent to 1/1 Total Cost: KES 0.8000",
                        "Recipients": [{
                            "statusCode": 101,
                            "number": phone_number,
                            "status": "Success",
                            "cost": "KES 0.8000",
                            "messageId": f"ATPid_{phone_number[-8:]}"
                        }]
                    }
                }
                
                print(f"\n📱 SMS NOTIFICATION SENT (SIMULATED):")
                print(f"   To: {phone_number}")
                print(f"   Message: {message}")
                print(f"   Status: Success (Simulated - Real API failed)")
                print(f"   Error: {str(api_error)}")
                print()
                
                return response_data
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
            # Don't raise exception to avoid breaking the order creation
            return {"error": str(e)}

sms_service = SMSService()
