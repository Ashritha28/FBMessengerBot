import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

def post_facebook_message(fbid, recevied_message): 
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAJAri76HK8BABIjqBtJ9GCwNFYq6pLatFQ2vPCEJo6oK97BmxmWoSTOPY6GgWAWkfKC3IidJV8g4JOvFF6aiOttiZBkPYH9YSILscHTUxkQJ9zUCnAirIc8ntZCgDaC8kpHivEGR3LKY9XwA63ZBhZCcZAP2lW1D5sioYFRGSgZDZD'
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class MyChatBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '9493145057':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
    	return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
    	# Converts the text payload into a python dictionary
    	incoming_message = json.loads(self.request.body.decode('utf-8'))
    	# Facebook recommends going through every entry since they might send multiple messages in a single call during high load
    	for entry in incoming_message['entry']:
    		for message in entry['messaging']:
    			# Check to make sure the received call is a message call
    			# This might be delivery, optin, postback for other events 
    		    if 'message' in message:
    		    	# Print the message to the terminal
    		    	#pprint(message)
    		    	post_facebook_message(message['sender']['id'], message['message']['text'])  
    	return HttpResponse()

