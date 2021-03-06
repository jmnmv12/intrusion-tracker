import random
from datetime import datetime
import pika
import requests
from requests.auth import HTTPBasicAuth

import json
import time


def main():

    credentials = pika.PlainCredentials('intrusion_tracker', '123')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.160.220',
                                   5672,
                                   '/',
                                   credentials))
    channel = connection.channel()
    channel.queue_declare(queue="access")
    user_ids, room_numbers = [], []
    url = "http://192.168.160.220:8080/api/v1/"
    black_list_users=["j.vasconcelos99@ua.pt","vascoalramos@ua.pt","antonio99@ua.pt","bs@ua.pt","tomas99@ua.pt","tiagocmendes@ua.pt","maria99@ua.pt","mario99@ua.pt","sofia99@ua.pt","helder@ua.pt","diogo04@ua.pt","nc@ua.pt",]
    
    # users
    response = requests.get(url+"persons/",auth=HTTPBasicAuth("j.vasconcelos99@ua.pt", "pwd"))
    if response.status_code == 200:
        print("Success!")
        user_ids = [ (u["id"], u["accessLevel"],u["email"]) for u in response.json() ]

    elif response.status_code == 404:
        print("Not Found!")
    # rooms
    response = requests.get(url+"rooms/",auth=HTTPBasicAuth("j.vasconcelos99@ua.pt", "pwd"))
    if response.status_code == 200:
        print("Success!")
        room_numbers = [ (r["roomNumber"], r["accessLevel"]) for r in response.json() ]

    elif response.status_code == 404:
        print("Not Found!")

    types = ["ENTRY", "EXIT"]
    
    message = {"message_type": "ACCESS"}
    bad_choices = [
        (user[0], room[0])
        for user in user_ids
        for room in room_numbers
        if user[1] < room[1] and user[2] not in black_list_users
    ]
    random.shuffle(bad_choices)
    small_bad_choices=bad_choices[:50]
    good_choices = [
        (user[0], room[0])
        for user in user_ids
        for room in room_numbers
        if user[1] >= room[1]
    ]

    random.shuffle(good_choices)

    good_counter=0
    bad_counter=0
    good_flag=True
    while True:

        if good_counter>=20:
            good_counter=0
            bad_counter=0
            good_flag=False
        
        if bad_counter>=2:
            bad_counter=0
            good_counter=0
            good_flag=True
        
        if good_flag:
            
            # Choose random user_id and room_number
            final_user_id, final_room_number = random.choice(good_choices)

            # Choose random type
            final_type = random.choice(types)

            # Generate timestamp
            datetime_obj = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%Z")


            message["person"] ={"id": final_user_id}
            message["room"] ={"roomNumber": final_room_number}
            message["accessType"] =final_type
            message["timestamp"] =datetime_obj

            channel.basic_publish(
                exchange="",
                routing_key="access",
                body=json.dumps(message, indent=4, sort_keys=True, default=str),
            )
            print(f" [x] Sent GOOD {message}")
            good_counter+=1
            time.sleep(2)
        else:
            # Choose random user_id and room_number
            final_user_id, final_room_number = random.choice(bad_choices)

            # Choose random type
            final_type = random.choice(types)

            # Generate timestamp
            datetime_obj = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%Z")


            message["person"] ={"id": final_user_id}
            message["room"] ={"roomNumber": final_room_number}
            message["accessType"] =final_type
            message["timestamp"] =datetime_obj

            channel.basic_publish(
                exchange="",
                routing_key="access",
                body=json.dumps(message, indent=4, sort_keys=True, default=str),
            )
            print(f" [x] Sent BAD {message}")
            bad_counter+=1
            time.sleep(2)


    connection.close()


if __name__ == "__main__":
    main()
