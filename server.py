from flask import Flask, request, Response, jsonify
from flask.templating import render_template
import docker
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="views", static_folder="static")
client = docker.DockerClient(base_url=os.environ.get("DOCKER_URL"))

def get_all_containers():
  containers = []
  for container in client.containers.list(all=True):
    containers.append({
      "id": container.short_id,
      "name": container.name,
      "status": container.status,
      "image": container.image.tags[0]
    })
  return containers

@app.route("/")
def index():
  return render_template("index.html", containers=get_all_containers())

@app.route("/commands", methods=["POST"])
async def commands():
  type = request.get_json()["type"]
  container_id = request.get_json()["id"]
  container = client.containers.get(container_id)
  if type == "pause":
    container.pause()
  elif type == "stop":
    container.stop()
  elif type == "restart":
    container.restart()
  elif type == "start":
    if container.status == "paused":
      container.unpause()
    else:
      container.start()

  return Response(status=200)


app.run(host="0.0.0.0")