from flask import Flask, request
import requests
import json

# -------------------- 配置区域 --------------------
# NapCat HTTP 服务器地址（HTTP 客户端监听地址）
NAPCAT_HTTP_API = "http://127.0.0.1:10280"

# NapCat HTTP 客户端 Token（必须和 NapCat 配置里的一致）
TOKEN = "dC3aU4hB3c"

# 保护的目标账号（可以是多个大号）
PROTECTED_UIDS = [2939194063, 1234567890]  # 可以根据需求添加多个QQ号
# ---------------------------------------------------

app = Flask(__name__)


@app.route("/receive_event", methods=["POST"])
def receive_event():
    data = request.json
    # print("收到事件:", json.dumps(data, ensure_ascii=False, indent=2))

    # 判断是否为戳一戳事件
    if data.get("post_type") == "notice" and data.get("sub_type") == "poke":
        # 只处理戳保护号的事件
        if data.get("target_id") in PROTECTED_UIDS:
            user_id = int(data.get("user_id"))
            group_id = data.get("group_id")

            payload = {"user_id": user_id}

            if group_id:
                payload["group_id"] = int(group_id)
                url = f"{NAPCAT_HTTP_API}/group_poke?access_token={TOKEN}"
            else:
                url = f"{NAPCAT_HTTP_API}/send_poke?access_token={TOKEN}"

            # 输出调试信息：请求体和目标URL
            print("回戳请求体:", json.dumps(payload, ensure_ascii=False))
            print("请求URL:", url)

            try:
                resp = requests.post(url, json=payload)
                print("已回戳:", resp.json())
            except Exception as e:
                print("回戳失败:", e)

    else:
        print("收到其他事件:", data.get("post_type"))

    return {"status": "ok"}


if __name__ == "__main__":
    # Flask 运行在本地 8080 端口，可通过 NapCat HTTP 客户端上报事件
    app.run(host="127.0.0.1", port=8080)
