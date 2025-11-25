import requests
from config import bot_config


def send_group_poke(group_id: int, user_id: int):
    url = f"{bot_config['napcat_http_api']}/group_poke"
    headers = {"Authorization": f"Token {bot_config['token']}"}
    payload = {"group_id": int(group_id), "user_id": int(user_id)}
    requests.post(url, json=payload, headers=headers)


def send_private_poke(user_id: int):
    url = f"{bot_config['napcat_http_api']}/send_poke"
    headers = {"Authorization": f"Token {bot_config['token']}"}
    payload = {"user_id": int(user_id)}
    requests.post(url, json=payload, headers=headers)


def send_group_msg(group_id: int, text: str):
    url = f"{bot_config['napcat_http_api']}/send_group_msg"
    headers = {"Authorization": f"Token {bot_config['token']}"}
    payload = {"group_id": group_id, "message": text}
    requests.post(url, json=payload, headers=headers)
