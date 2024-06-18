import asyncio
import websockets
import json
import requests

# Configuration
GOTIFY_TOKEN = 'your_gotify_token_here'  # Replace with your Gotify token
GOTIFY_URL = f'ws://your_gotify_server_ip:3000/stream?token={GOTIFY_TOKEN}'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/your_discord_webhook_here'

# Function to send message to Discord
def send_to_discord(content):
    data = {
        "content": content
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    response.raise_for_status()

async def gotify_listener():
    async with websockets.connect(GOTIFY_URL) as websocket:
        while True:
            try:
                message = await websocket.recv()
                message_data = json.loads(message)
                print(f"Received message: {message_data}")
                send_to_discord(message_data['message'])
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(30)  # Wait for 30 seconds before retrying in case of error

def main():
    asyncio.run(gotify_listener())

if __name__ == "__main__":
    main()
