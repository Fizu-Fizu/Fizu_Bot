from utils.logger import logger
from services.api import send_group_msg
from tools.deepseek import deepseek
from tools.memory import get_memory

BOT_QQ = 534362816
AI_GROUPS = [836713483]


def handle_message(event: dict):
    message = event.get("message", [])
    raw_text = event.get("raw_message", "").strip()
    group_id = event.get("group_id")

    if group_id not in AI_GROUPS:
        return

    # 是否 @bot
    at_me = any(
        m["type"] == "at" and str(m["data"]["qq"]) == str(BOT_QQ) for m in message
    )

    if not at_me:
        return

    # 去掉 @bot
    cleaned = raw_text.replace(f"[CQ:at,qq={BOT_QQ}]", "").strip()

    # 读取群记忆
    mem = get_memory(group_id)

    # 写入用户内容
    mem.add("user", cleaned)

    # 构建 DeepSeek 输入
    context = mem.get_context()
    full_prompt = f"【对话上下文】\n{context}\n\n【用户最新问题】{cleaned}"

    # AI 回复
    reply = deepseek(full_prompt, mode=1)

    # 写入 bot 回复
    mem.add("bot", reply)

    # 自动更新话题总结
    if len(mem.messages) >= 10:
        mem.update_summary()

    send_group_msg(group_id, reply)
    logger.info(f"[AI 回复] {reply}")
