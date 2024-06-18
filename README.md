# Gotify to Discord Forwarder Script Usage

This script listens to Gotify messages via WebSocket and forwards them to a Discord webhook.

## Prerequisites

- Python 3.6 or higher installed on your system
- `websockets` library installed (install with `pip install websockets`)

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

### 2. Configuration

#### Gotify Setup

1. **Gotify Application Token:**
   - Replace `your_gotify_token_here` with your Gotify application token in `forward_gotify_to_discord.py`.
   - Example: `GOTIFY_TOKEN = 'your_gotify_token_here'`

2. **Gotify Server URL:**
   - Replace `your_gotify_server_ip` with the IP address or hostname of your Gotify server.
   - Example: `GOTIFY_URL = f'ws://your_gotify_server_ip:3000/stream?token={GOTIFY_TOKEN}'`

#### Discord Setup

1. **Discord Webhook URL:**
   - Replace `your_discord_webhook_here` with your Discord webhook URL in `forward_gotify_to_discord.py`.
   - Example: `DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/your_discord_webhook_here'`

### 3. Install Dependencies

Install the required Python dependencies using pip:

```
pip install -r requirements.txt
```

### 4. Running the Script

Run the script to start forwarding Gotify messages to Discord:

```
python3 forward_gotify_to_discord.py
```

The script will establish a WebSocket connection to your Gotify server and listen for incoming messages. When a message is received, it will be forwarded to the specified Discord webhook.

### 5. Additional Notes

- Ensure that your Gotify server is accessible from the machine where you are running the script.
- Monitor the script output for any errors or messages indicating successful forwarding of messages.

## Troubleshooting

If you encounter any issues while setting up or running the script, consider the following steps:

- **Check Dependencies:** Ensure that Python and the `websockets` library are correctly installed.
- **Verify Configuration:** Double-check the Gotify token, server URL, and Discord webhook URL in `forward_gotify_to_discord.py`.
- **Review Logs:** Check the script output or logs for any error messages or indications of connection issues.


# Running Python Script as a systemd Service on Ubuntu

This guide explains how to set up and run your Python script (`forward_gotify_to_discord.py`) as a systemd service on Ubuntu. This includes creating a new user, placing the script in `/opt/discordforwarder/`, and setting correct permissions.

## 1. Create a New User

Create a new system user (`forwarduser`) to run the service:

```sh
sudo adduser --system --group --disabled-login --home /home/forwarduser forwarduser
```

This command creates a system user named `forwarduser` with a home directory set to `/home/forwarduser`.

## 2. Create Directory and Move Script

Create the directory `/opt/discordforwarder/` and move your Python script (`forward_gotify_to_discord.py`) into it:

```sh
sudo mkdir /opt/discordforwarder
sudo mv forward_gotify_to_discord.py /opt/discordforwarder/
```

## 3. Set Permissions

Set ownership and permissions for the script and its directory:

```sh
sudo chown -R forwarduser:forwarduser /opt/discordforwarder
sudo chmod +x /opt/discordforwarder/forward_gotify_to_discord.py
```

- `chown -R forwarduser:forwarduser /opt/discordforwarder`: Recursively change ownership of all files and directories under `/opt/discordforwarder` to `forwarduser`.
- `chmod +x /opt/discordforwarder/forward_gotify_to_discord.py`: Make the script executable.

## 4. Create Systemd Service File

Create a systemd service file (`forward-gotify-to-discord.service`) in `/etc/systemd/system/`:

```sh
sudo nano /etc/systemd/system/forward-gotify-to-discord.service
```

## 5. Define the Service

Add the following content to `forward-gotify-to-discord.service`:

```ini
[Unit]
Description=Gotify to Discord Forwarder
After=network.target

[Service]
User=forwarduser
Group=forwarduser
WorkingDirectory=/opt/discordforwarder
ExecStart=/usr/bin/python3 /opt/discordforwarder/forward_gotify_to_discord.py
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=forward-gotify-to-discord

[Install]
WantedBy=multi-user.target
```

## 6. Save and Exit

Save the file (`Ctrl + O` in nano, then `Enter`) and exit (`Ctrl + X`).

## 7. Enable and Start the Service

Once the service file is created, enable and start the service:

```sh
sudo systemctl daemon-reload  # Reload systemd to read the new service file
sudo systemctl enable forward-gotify-to-discord  # Enable the service to start on boot
sudo systemctl start forward-gotify-to-discord  # Start the service now
```

## 8. Verify the Service Status

Check the status of your service to ensure it's running without errors:

```sh
sudo systemctl status forward-gotify-to-discord
```

Look for `Active: active (running)` in the output, which indicates that the service is running successfully.

## 9. View Logs (Optional)

To view logs related to your service:

```sh
sudo journalctl -u forward-gotify-to-discord
```

This command displays logs specific to the `forward-gotify-to-discord` service.

### Notes:

- Replace `forward_gotify_to_discord.py` with the actual name of your Python script.
- Adjust paths (`WorkingDirectory` and `ExecStart`) in the `.service` file to match your script's location and environment.
- Ensure your Python script is executable (`chmod +x` if needed).
- This setup ensures that your Python script runs as a service, automatically starting on system boot and managed by `systemd`, providing reliability and ease of management. Adjust configurations as necessary based on specific requirements or system setup.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
