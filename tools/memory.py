import os
import json
from collections import deque
from tools.deepseek import deepseek

MEMORY_DIR = "config/memory"
os.makedirs(MEMORY_DIR, exist_ok=True)


class GroupMemory:
    def __init__(self, group_id, max_len=10):
        self.group_id = str(group_id)
        self.path = os.path.join(MEMORY_DIR, f"group_{self.group_id}.json")
        self.max_len = max_len

        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"summary": "", "messages": []}

        self.summary = data.get("summary", "")
        self.messages = deque(data.get("messages", []), maxlen=max_len)

    def save(self):
        data = {"summary": self.summary, "messages": list(self.messages)}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add(self, role, text):
        self.messages.append({"role": role, "text": text})
        self.save()

    def get_context(self):
        msg_text = "\n".join([f"{m['role']}: {m['text']}" for m in self.messages])
        context = ""

        if self.summary:
            context += f"【上次总结】\n{self.summary}\n\n"

        context += f"【最近十条消息】\n{msg_text}"
        return context

    def update_summary(self):
        prompt = (
            "请根据以下对话内容生成一个不超过500字的总结，"
            "重点提炼人物、主题、观点，不要流水账，不要逐句复述。\n\n"
            f"{self.get_context()}"
        )

        self.summary = deepseek(prompt, mode=1)
        self.save()


def get_memory(group_id):
    return GroupMemory(group_id)
