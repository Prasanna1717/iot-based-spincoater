[Unit]
Description=Spin Coater Service
After=network.target

[Service]
ExecStartPre=/bin/sleep 10
ExecStart=/usr/bin/python3 /home/prasa/lcd/spincoater.py
WorkingDirectory=/home/prasa/lcd
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
