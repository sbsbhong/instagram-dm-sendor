import time, dotenv, os, csv
from instagram import Instagram

dotenv.load_dotenv(override=True)

INSTA_ID = os.getenv("INSTA_ID_TEST")
INSTA_PW = os.getenv("INSTA_PW_TEST")

if not INSTA_ID or not INSTA_PW:
    raise ValueError("INSTA_ID_TEST or INSTA_PW_TEST is not defined in .env file")

class InteriorInstagram:
    def __init__(self, row: dict) :
        self.name: str = row["name"]
        self.address: str = row["address"]
        self._link = self._drop_params(row["link"])
        if self._link.endswith("/"):
            self._link = self._link[:-1]
        

    @property
    def instagram_id(self) -> str:
        return self._link.split("/")[-1]
    
    def _drop_params(self, link: str) -> str:
        return link.split("?")[0]
    
    def __str__(self):
        return f"InteriorInstagram({self.name}, {self.address}, {self.instagram_id})"
    

if __name__ == "__main__":
    interior_csv_file = open("data/interior_instas_test.csv", "r", encoding="utf-8")
    interior_csv = csv.DictReader(interior_csv_file)
    insta = Instagram()

    dm = insta.login(INSTA_ID, INSTA_PW).dm
    dm.open()

    for row in interior_csv:
        interior = InteriorInstagram(row)
        try:
            dm.new_message(interior.instagram_id)
            dm.send_messsage(f"안녕하세요, 사장님! 스타트홈 입니다.")
            dm.send_messsage(f"네이버 검색중에 {interior.name}의 블로그를 보게 되어 연락드렸습니다.")
            dm.send_messsage(f"혹시 IoT 기기들을 활용한 스마트홈 구축도 하고 계시는지요?")
            dm.send_files([
                r"/Users/hongseongbin/Desktop/KakaoTalk_Photo_2024-06-16-21-55-21 001.jpeg",
                r"/Users/hongseongbin/Desktop/KakaoTalk_Photo_2024-06-16-21-55-21 002.jpeg",
            ])
            dm.close_room()
        except Exception as e:
            print("Error: ", e, interior)
            continue


    

time.sleep(600)