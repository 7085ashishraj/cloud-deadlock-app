#!/bin/bash

# Cloud Deadlock Detector - AWS EC2 Deployment Script (Ubuntu)
# This script installs requirements, sets up the backend with systemd/uvicorn, 
# and configures the frontend with PM2 and Nginx as a reverse proxy.

echo "Starting Deployment process..."

# 1. Update system & install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx mysql-server npm curl

# 2. Setup Node environment (for building react and PM2)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-install -y nodejs
sudo npm install -g pm2

# 3. Setup Python Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Backend using PM2 (or you could use systemd)
pm2 start "python -m uvicorn main:app --host 0.0.0.0 --port 8000" --name deadlock-backend

# 4. Setup React Frontend
cd ../frontend
npm install
npm run build

# Serve Frontend using PM2
pm2 serve dist 5000 --name deadlock-frontend --spa

pm2 save
pm2 startup

# 5. Configure Nginx
sudo cp ../nginx.conf /etc/nginx/sites-available/default
sudo systemctl restart nginx

echo "Deployment finished! Your app is now running."
