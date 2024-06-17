import dotenv, os, csv
from instagram import Instagram

dotenv.load_dotenv(override=True)

INSTA_ID = os.getenv("INSTA_ID")
INSTA_PW = os.getenv("INSTA_PW")

if not INSTA_ID or not INSTA_PW:
    raise ValueError("INSTA_ID or INSTA_PW is not defined in .env file")

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
    interior_csv_file = open("data/interior_instas.csv", "r", encoding="utf-8")
    interior_csv = csv.DictReader(interior_csv_file)
    insta = Instagram()

    dm = insta.login(INSTA_ID, INSTA_PW).dm
    dm.open()
    errors: list[str] = []

    for row in interior_csv:
        interior = InteriorInstagram(row)
        try:
            dm.wait_random_time()
            dm.new_message(interior.instagram_id)

            if not dm.room:
                continue

            if dm.room.is_refusing_stranger:
                dm.send_messsage(
f"""
안녕하세요, 사장님! 스타트홈 입니다. 네이버 검색중에 '{interior.name}' 블로그를 보게 되어 연락드렸습니다. 혹시 IoT 기기들을 활용한 스마트홈 구축도 하고 계시는지요?
"""
                ).close_room()
            else:
                dm.send_messsage(f"안녕하세요, 사장님! 스타트홈 입니다.")\
                    .send_messsage(f"네이버 검색중에 {interior.name}의 블로그를 보게 되어 연락드렸습니다.")\
                    .send_messsage(f"혹시 IoT 기기들을 활용한 스마트홈 구축도 하고 계시는지요?")\
                    .close_room()
                
            dm.wait_random_time()
        except Exception as e:
            print("Error: ", e, interior)
            errors.append(str(e) + " " + str(interior))
            continue

    for error in errors:
        print(error)

