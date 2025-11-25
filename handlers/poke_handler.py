from utils.logger import logger
from services.api import send_group_poke, send_private_poke

PROTECTED_UIDS = [2939194063]
BOT_UID = 534362816


def handle_poke(event: dict):
    sub_type = event.get("sub_type")
    if sub_type != "poke":
        return

    user_id = event.get("user_id")
    target_id = event.get("target_id")
    group_id = event.get("group_id")

    # 1. 戳大号
    if target_id in PROTECTED_UIDS:
        logger.info(f"[戳保护号] {user_id} 戳了 {target_id} → 自动回戳")

        if group_id:
            send_group_poke(group_id, user_id)
        else:
            send_private_poke(user_id)
        return

    # 2. 戳机器人
    if target_id == BOT_UID:
        logger.info(f"[戳BOT] {user_id} 戳了机器人 → 自动反戳")

        if group_id:
            send_group_poke(group_id, user_id)
        else:
            send_private_poke(user_id)
        return
