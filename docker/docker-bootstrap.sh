#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  echo "Starting Celery worker..."
  celery --app=app.api.endpoints.tasks.tasks:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  echo "Starting Flower..."
  celery --app=app.api.endpoints.tasks.tasks:celery flower
 fi