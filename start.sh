#!/usr/bin/env bash
waitress-serve --port $PORT --call "profileapp:create_app"
