import requests


def deepseek(input_text: str, mode: int = 1):
    persona = (
        "你是一只可爱、温柔、粘人的猫娘 AI，说话会适当带“喵~”，"
        "表达自然简洁，不解释规则，不复读内容。"
    )

    final_prompt = (
        f"【角色设定】\n{persona}\n\n"
        f"【任务】根据用户输入生成回答。\n"
        f"【输入内容】\n{input_text}"
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "deepseek-r1:7b", "prompt": final_prompt, "stream": False},
    )

    return response.json().get("response", "")
