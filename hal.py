import slack
import os
_ = os.system("clear")
print(" ----------")
print("| HAL-9000 |")
print(" ----------")
with open("appscrt.txt","r") as f:
	secret = f.readlines()[0].replace("\n","")

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
	data = payload['data']
	#user = data['user']
	web_client = payload['web_client']
	rtm_client = payload['rtm_client']
	msg = data.get('text', [])
	conversation_dict = {"hello":"Hello !",
			     "status":"Can't get the status",
			     "open the hatch":"I'm sorry Dave, I'm afraid I can't do that for you :(",
			     "plots":"wait I will send them",
			     "single plot" : "which plot? \n available plots are:\n",
			     ".png" : "Sending:"
				}
	print("Received: "+msg)
	for message in conversation_dict:
		if message.lower() in msg.lower():
			channel_id = data['channel']
			thread_ts = data['ts']
			txt = conversation_dict[message]
			if message == "status":
				try:
					f = open("bot.txt")
					txt = f.readlines()
					f.close()
				except:
					txt = "Cant open file"
			print(txt)
			if message == ".png":
				txt = txt+msg
				if msg in os.listidr("plots"):
					web_client.files_upload(
						channels=channel_id,
						file="plots/"+msg
					)
				else:
					txt = "File not found!"
			web_client.chat_postMessage(
				channel=channel_id,
				text=txt,
				as_user=True
				)
			if message == "plots":
				for plot in os.listdir("plots"):
					if "." not in plot:
						continue
					web_client.files_upload(
						channels=channel_id,
						file="plots/"+plot
						)
				break
			if message == "single plot":
				plots = os.listdir("plots")
				plots = zip(range(len(plots)),plots)
				web_client.chat_postMessage(
					channel=channel_id,
					text=str(plots),
					as_user=True)
				break

rtm_client = slack.RTMClient(token=secret)
rtm_client.start()
