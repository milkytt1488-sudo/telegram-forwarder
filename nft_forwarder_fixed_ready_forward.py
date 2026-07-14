from telethon import TelegramClient, events, functions

api_id = 39561884
api_hash = "e888e4cad4455fb2706d20ecf40acc08"

SOURCE_CHAT = -1004310502256
TARGET_CHAT = -1003608802119

IGNORE_TOPIC_IDS = {1,8}
seen=set()
TOPIC_MAP = {
    4: 2,  
    7544: 9,  
    7: 13,  
    5: 14,
    6: 4,
    8:17,
}

client=TelegramClient("session",api_id,api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def handler(event):
    topic_id = None

    if event.message.reply_to:
        topic_id = getattr(event.message.reply_to, "reply_to_top_id", None)
        if topic_id is None:
            topic_id = getattr(event.message.reply_to, "reply_to_msg_id", None)

    print(f"Сообщение {event.message.id}, topic={topic_id}")

    if topic_id in IGNORE_TOPIC_IDS:
        return

    target_topic = TOPIC_MAP.get(topic_id)
    if target_topic is None:
        print("Нет соответствия для темы")
        return

    try:
        source=await client.get_input_entity(SOURCE_CHAT)
        target=await client.get_input_entity(TARGET_CHAT)
        await client(functions.messages.ForwardMessagesRequest(from_peer=source,id=[event.message.id],to_peer=target,top_msg_id=target_topic,drop_author=False,drop_media_captions=False,noforwards=False,with_my_score=False))
        print("Переслано")
    except Exception as e:
        print("Ошибка:",repr(e))

client.start()
print("Started")
client.run_until_disconnected()