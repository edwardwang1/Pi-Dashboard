from mycroft_bus_client import MessageBusClient, Message
import Pyro4

def sendUtterance(message):
    with open("uri.txt", 'r') as myfile:
        uri = myfile.read()
    try:
        with Pyro4.Proxy(uri) as app:
            print(message.data.get('utterances')[0])
            #app.updateCommandDisplay(message.data.get('utterances')[0])
            try:
                app.updateCommandDisplay(message.data.get('utterances')[0])
                #app.showHideWeather(0)
                print("success")
            except Exception as ex:
                print("can't execute command", ex)
    except:
        print("Pyro could not create connection")

client = MessageBusClient()
client.on('recognizer_loop:utterance', sendUtterance)
client.run_forever()