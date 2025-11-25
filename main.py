from flask import Flask, request
from handlers.message_handler import handle_message
from handlers.poke_handler import handle_poke

app = Flask(__name__)


@app.post("/")
def receive():
    data = request.json
    post_type = data.get("post_type")

    if post_type == "message":
        handle_message(data)

    elif post_type == "notice" and data.get("sub_type") == "poke":
        handle_poke(data)

    return "ok"


if __name__ == "__main__":
    import config.bot_config as cfg

    app.run(host="0.0.0.0", port=cfg.bot_config["listen_port"])
