import time, dotenv, os
from instagram import Instagram

dotenv.load_dotenv(override=True)

INSTA_ID = os.getenv("INSTA_ID")
INSTA_PW = os.getenv("INSTA_PW")

if not INSTA_ID or not INSTA_PW:
    raise ValueError("INSTA_ID or INSTA_PW is not defined in .env file")

recipients = [
    "jjun____ho",
    #"openmat24",
    #"starthome_iot"
]

insta = Instagram()

dm = insta.login(INSTA_ID, INSTA_PW).dm

dm.open()

for recipient in recipients:
    dm.new_message(recipient)
    dm.send_messsage("안녕? 나는 홍성빈이야.")
    dm.send_files([
        r"/Users/hongseongbin/Desktop/KakaoTalk_Photo_2024-06-16-21-55-21 001.jpeg",
        r"/Users/hongseongbin/Desktop/KakaoTalk_Photo_2024-06-16-21-55-21 002.jpeg"
    ])
    dm.close_room()



    

time.sleep(600)