#! /bin/bash

if ! command -v pip &>/dev/null; then
    echo "pip is not installed, installing..."
    sudo apt-get update
    sudo apt-get install python3-pip -y
else
    echo "pip is installed"
fi

# Check if Daphne and channels are installed
if ! pip list | grep daphne | awk '{print $1}' &>/dev/null; then
    echo "daphne is not installed"
    echo "Installing daphne"
    /usr/bin/pip install -U channels["daphne"]
else
    echo "daphne is installed"
fi

# Check if python-dotenv are installed
if ! pip list | grep python-dotenv | awk '{print $1}' &>/dev/null; then
    echo "python-dotenv is not installed"
    echo "Installing python-dotenv"
    /usr/bin/pip install -U channels["daphne"]
else
    echo "python-dotenv is installed"
fi

# Check if channels-redis are installed
if ! pip list | grep channels-redis | awk '{print $1}' &>/dev/null; then
    echo "channels_redis is not installed"
    echo "Installing channels-redis"
    /usr/bin/pip install channels_redis
else
    echo "channels_redis is installed"
fi

# Check if pymongo are installed
if ! pip list | grep pymongo | awk '{print $1}' &>/dev/null; then
    echo "pymongo is not installed"
    echo "Installing pymongo"
    /usr/bin/pip install pymongo[snappy,gssapi,srv,tls]
else
    echo "pymongo is installed"
fi

#/usr/bin/python3 manage.py runserver