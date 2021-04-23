import os
import discord
import boto3
from botocore.exceptions import ClientError
import random
import time

from dotenv import load_dotenv

load_dotenv()
bottoken = os.getenv('BOT_TOKEN')
active_server_var = 0;

discordclient = discord.Client()
awssession = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def check_running():
    ec2 = awssession.resource('ec2')
    for instance in ec2.instances.filter():
        if instance.state['Code']==16:
            return 1
    else: return 0

@discordclient.event
async def on_ready():
    print("connected to server\n")

@discordclient.event
async def on_message(message):
    if message.author == discordclient.user:
        return

    parts = message.content.split(' ')

    if parts[0] == '!awsbot':
        if parts[1] == 'help':
            print("help requested by "+message.author.display_name+" ("+str(message.author.id)+")\n")
            await message.channel.send("commands: ```help: show commands \nbotstatus: check if bot is running```  ")
        if parts[1] == 'botstatus':
            print("botstatus requested by "+message.author.display_name+" ("+str(message.author.id)+")\n")
            await message.channel.send('awsbot is running')

        if parts[1] == 's3test':
            print("s3test requested by "+message.author.display_name+" ("+str(message.author.id)+")\n")
            s3 = awssession.resource('s3')
            for bucket in s3.buckets.all():
                print(bucket.name)

        if parts[1] == 'ec2test':
            print("s3test requested by "+message.author.display_name+" ("+str(message.author.id)+")\n")
            ec2 = awssession.resource('ec2')
            for instances in ec2.instances.all():
                print(instances.tags[0]['Value'])

        if parts[1] == 'launchmc':
            print("launchmc requested by "+message.author.display_name+" ("+str(message.author.id)+")\n")
            if check_running():
                await message.channel.send('A server is already active, shut it down and try starting one again')
                return

            ec2 = awssession.resource('ec2')
            await message.channel.send('Starting a Minecraft server...')

            #allocate ip addr
            try:
                classicaddress = ec2.ClassicAddress(os.getenv('IP_ADDR'))
                response = classicaddress.associate(InstanceId=os.getenv('MINECRAFT_INSTANCE'), AllowReassociation=True)
                print(response)
            except ClientError as e:
                print(e)
                await message.channel.send('an error happened during ip address allocation ```'+str(e)+'```')
                return

            #try:
                #instance = ec2.instance('0b3db6f17303693a2')



        if parts[1] == 'launcharma':
            print("launcharma requested by "+message.author.display_name+" ("+str(message.author.id)+")\n")
            if check_running():
                await message.channel.send('A server is already active, shut it down and try starting one again')
                return

            ec2 = awssession.resource('ec2')
            await message.channel.send('Starting an Arma 3 server...')

            #allocate ip addr
            try:
                classicaddress = ec2.ClassicAddress(os.getenv('IP_ADDR'))
                response = classicaddress.associate(InstanceId=os.getenv('ARMA_INSTANCE'), AllowReassociation=True)
                print(response)
            except ClientError as e:
                print(e)
                await message.channel.send('an error happened during ip address allocation ```'+str(e)+'```')
                return


    else:
        if str(message.channel.type) == "private":
            time.sleep(random.randint(3,5))
            rand = random.randint(0,100)
            if rand < 33:
                await message.channel.send("haha lmao")
            if rand >= 33 and rand < 66:
                await message.channel.send("bro lmao good post")
            else: await message.channel.send("lol")
            return
        else:
            return

discordclient.run(bottoken)
