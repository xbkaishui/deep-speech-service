echo "start speech_service flask app"
#nohup flask --app speech_service.app --debug run -p 9090 -h 0.0.0.0 &
nohup gunicorn speech_service.app:app -w 8 -b 0.0.0.0:9090 --timeout 3600 &