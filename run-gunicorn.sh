#!/bin/bash

gunicorn -b 0.0.0.0:5555 -k flask_sockets.worker run:app
