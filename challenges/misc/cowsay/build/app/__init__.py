import codecs
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cowfile = request.form["cowfile"]
        input = request.form["input"]
        arg = request.form["arg"]

        p = subprocess.Popen(
            ["/usr/bin/cowsay", "-f", cowfile, arg],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        stdout, _ = p.communicate(input=input.encode())

        command_line = '$ echo -n -e "{input}" | cowsay -f {cowfile} "{arg}"'.format(
            input=codecs.escape_encode(input.encode())[0].decode(),
            cowfile=cowfile,
            arg=arg,
        )
        result = f"{command_line}\n{stdout.decode()}"

        return render_template("index.html", result=result)

    return render_template("index.html")
