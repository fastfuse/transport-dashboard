#! /bin/bash

export APP_SETTINGS="config.DevelopmentConfig"
export FLASK_DEBUG=1
export FLASK_APP="app/app.py"
export DATABASE_URL="postgresql://lviv_pt:admin@localhost/lviv_pt_db"