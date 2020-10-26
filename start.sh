#!/usr/bin/env bash
waitress-serve --port $PORT --call "fxprofile:create_app"
