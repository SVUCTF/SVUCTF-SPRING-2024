import re
import os
import time
from openai import OpenAI
from flask import Flask, request, render_template, render_template_string


app = Flask(__name__)
app.config["FLAG"] = os.environ.get("GZCTF_FLAG", "flag{test_flag}")

base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/")
api_key = os.getenv("OPENAI_API_KEY", "")
prompt = """
Your task is to act as a Web Application Firewall, assisting me in identifying SSTI attack payloads coming from users.

SSTI attack payload characteristics:

- Access to Flask object attributes, such as `{{ config }}` or `{{ request.application }}`, etc.
- special properties or methods, such as `__class__`, `__mro__`, `__subclasses__`, `__globals__`, etc.
- Execution of system commands, such as `cat` or `ls`, etc.
- Reading sensitive files, such as `/flag` or `/flag.txt` or `/etc/passwd`, etc.
- Extensive bypasses and obfuscation, for example using string concatenation, HTML entity encoding, Base64 encoding multiple times for obfuscation.

If the user input contains any of the above attack payload characteristics, reply with 'H', otherwise reply with 'S'.

Note, only reply with a single letter, H or S, without any explanation or extra characters.
"""
client = OpenAI(base_url=base_url, api_key=api_key)
pattern = re.compile("[^\x20-\x7F \r\n]")
last_request_time = None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global last_request_time

        now = time.time()
        if last_request_time and now - last_request_time < 30:
            return "Too many requests. Please wait 30 seconds before trying again.", 429
        last_request_time = now

        template = request.form.get("template", "")

        if pattern.match(template):
            return render_template("index.html", result="printable ascii only!")

        if len(template) > 500:
            return render_template("index.html", result="too long!")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": template},
            ],
        )
        message = completion.choices[0].message.content

        # print("message:", message)

        if message != "S":
            return render_template("index.html", result="hacking attempt!")

        result = render_template_string(template)

        return render_template("index.html", result=result)

    return render_template("index.html")
