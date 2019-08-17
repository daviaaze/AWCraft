import asyncio
import boto3
import mcrcon
import base64
import json
from mcstatus import MinecraftServer


with open('config.json', 'r+') as config_file:
    data = json.load(config_file)

modes = data['modes']

credentials = data['credentials']

resource = boto3.resource('ec2', aws_access_key_id=credentials["aws_access_key_id"],
                          aws_secret_access_key=credentials["aws_secret_access_key"],
                          region_name=credentials["region_name"])

ec2 = boto3.client('ec2', aws_access_key_id=credentials["aws_access_key_id"],
                   aws_secret_access_key=credentials["aws_secret_access_key"],
                   region_name=credentials["region_name"])

instance = resource.Instance(credentials["Instance"])
instanceId = credentials["Instance"]

def minecraftStop():
    from mcrcon import MCRcon
    mcr = MCRcon(credentials["serverIP"],
                 credentials["rconpassword"], credentials["rconport"])
    mcr.connect()
    mcr.command("stop")


def stop():
    try:
        if credentials["rcon"] == "yes":
          minecraftStop()
          instance.stop(False, False)
        else:
          instance.stop(False, False)
        return True
    except:
        return False


def forceturnOffInstance():
    try:
        instance.stop(False, False)
        return True
    except:
        return False

def newUserData(mode):
  return base64.b64encode('''Content-Type: multipart/mixed; boundary = "//"


MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset = "us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename = "cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset = "us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename = "userdata.txt"

#!/bin/bash
cd / home/ec2-user/{}
screen - dmS minecraft ./server.sh
--//'''.format(mode))
  
  
def start(mode):
  if mode in modes:
    ec2.modify_instance_attribute(Attribute='userData', Value=newUserData(mode), InstanceId=instanceId)
    instance.start()
    return True
  else:
    return False



def status():
  server = MinecraftServer.lookup(credentials["serverIP"])
  status = server.status()
  return instance.state['Name'] +"/n" + "The server has {0} players and replied in {1} ms".format(status.players.online, status.latency)


def restart():
    try:
        minecraftStop()
        instance.reboot()
        return True
    except:
        return False
