# -*- coding: utf-8 -*-

import vk_api
import requests
import apiai, json
from vk_api.longpoll import VkLongPoll, VkEventType



vk_session = vk_api.VkApi(token='13fa4c2b324c1cf902fb41aea73e009749c4c465e448ab0d8bd4a240d68ef9dec30b1ff89286ecf5bdb09') # Токен для доступа к группе
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
quit = False

while quit == False:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.from_user:
                request = apiai.ApiAI('63a1aa64d90046beb8a6087038816881').text_request() # Токен API к DialogFlow
                request.lang = 'ru' # Язык
                request.query = event.text # Посылаем сообщение в DialogFlow                    
                responseJson = json.loads(request.getresponse().read().decode('utf-8'))
                response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON
                if response:
                    vk.messages.send(
                        user_id = event.user_id,
                        random_id = event.random_id,
                        message = response
                    )
                else:
                    vk.messages.send(
                        user_id = event.user_id,
                        random_id = event.random_id,
                        message = 'Я Вас не понял'
                    )






