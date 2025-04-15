import requests, random, json, base64, os

#+------------------------------------------------------+
#| Author : L7N                                       |
#| Telegram : t.me/PyL7N                     |
#| Github : https://github.com/is-L7N  |
#+------------------------------------------------------+

class Instagram:
    def __init__(self, token: str):
        self.token = token        
        self.base_url = "https://i.instagram.com"
        self.headers = {
            'User-Agent': self.user_agent(),
            'Authorization': self.token,
        }
        
    def get_following(self) -> list:
        self.id = self.get_info()
        url = self.base_url + "/graphql/query"
        payload = {
            'client_doc_id': "161046392816161230466227559622",
            'enable_canonical_naming': "true",
            'variables': f"{{\"query\":\"\",\"request_data\":{{\"includes_hashtags\":true,\"rank_token\":\"caa21f1d-4acb-466b-8a86-ae8df5b5f3d6\",\"search_surface\":\"follow_list_page\"}},\"user_id\":\"{self.id}\",\"include_friendship_status\":false,\"enable_groups\":true}}"
        }
        
        response = requests.post(url, data=payload, headers=self.headers).json()
        
        users = response.get('data', {}).get('1$xdt_api__v1__friendships__following(_request_data:$request_data,enable_groups:$enable_groups,include_friendship_status:$include_friendship_status,max_id:$max_id,order:$order,query:$query,user_id:$user_id)', {}).get('users', [])
        return [user.get('pk_id') for user in users], [user.get('username') for user in users]
           
    def get_info(self) ->int:
        url = self.base_url + "/api/v1/accounts/current_user/?edit=true"
        try:
            response = requests.get(url, headers=self.headers).json()
            return response['user']['pk_id']
        except Exception as e:
            print(e)
            return None
    
    def unfollow(self, iD: int) -> bool:        
        url = self.base_url + f"/api/v1/friendships/destroy/{iD}/"
                
        payload = {
            'signed_body': f"SIGNATURE.{{\"user_id\":\"{iD}\",\"nav_chain\":\"SelfFragment:self_profile:2:main_profile:1744719122.322::,FollowListFragment:self_following:4:button:1744719137.13::\",\"container_module\":\"self_following\"}}"
        }
        try:
            response = requests.post(url, data=payload, headers=self.headers).json()
            if response["status"]== "ok":
                return True
            else:
                return False
        except Exception:
            return False
        
    def work(self):      
        ids, usernams = self.get_following()
        print(f"[※] All Following : {len(ids)}\n")
        for id, user in zip(ids, usernams):
            res = self.unfollow(id)
            if res:
                print(f"[✓] Done UnFollow : {user}   ~ id : {id}")
            else:
                print(f"[×] Not UnFollowing  : {user}   ~ id : {id}")

    def user_agent(self) -> str:
        rnd = str(random.randint(150, 999))
        agent = "Instagram 311.0.0.32.118 Android (" + ["23/6.0", "24/7.0", "25/7.1.1", "26/8.0", "27/8.1", "28/9.0"][random.randint(0, 5)] + "; " + str(random.randint(100, 1300)) + "dpi; " + str(random.randint(200, 2000)) + "x" + str(random.randint(200, 2000)) + "; " + ["SAMSUNG", "HUAWEI", "LGE/lge", "HTC", "ASUS", "ZTE", "ONEPLUS", "XIAOMI", "OPPO", "VIVO", "SONY", "REALME"][random.randint(0, 11)] + "; SM-T" + rnd + "; SM-T" + rnd + "; qcom; en_US; 545986" + str(random.randint(111, 999)) + ")"
        return agent

class Fun:
    @staticmethod
    def trans_sessionid(ses):
        try:
            inp = ses.strip()
            if inp.startswith("Bearer IGT:2:"):
                b64 = inp.split("Bearer IGT:2:")[1]
                data = json.loads(base64.b64decode(b64).decode())
                return "[+] SessionID:\n" + data["sessionid"]
            else:
                uid = inp.split(":")[0]
                payload = json.dumps({"ds_user_id": uid, "sessionid": inp})
                token = base64.b64encode(payload.encode()).decode()
                return "[+] Bearer Token:\nBearer IGT:2:" + token
        except Exception:
            return {"status": False, "message": "Fuck!"}
            
if __name__ == "__main__":
    info = [
    "Author : L7N 🇮🇶",
    "Telegram : t.me/PyL7N",
    "Github : https://github.com/is-L7N"
]
    width = max(len(line) for line in info) + 4
    border = "+" + "-" * (width - 2) + "+"
    
    print(border)
    for line in info:
        print("| " + line.ljust(width - 3) + " |") 
    print(border)
    print("\n[1] Trans Sessionid To Token (Bearer) or opposite !\n[2] Start UnFollowing !\n")
    cho = input("[*] Choose : ")
    if cho == 1 or cho == "1":
        inp = input("[※] Your Sessiond or Token : ")
        print(Fun.trans_sessionid(inp))
    elif cho == 2 or cho == "2":
        token = input("\n[※] Your Token (Instagram) : ")
        os.system('clear')
        ig = Instagram(token)
        ig.work()
    else:
        print("Fk !")
