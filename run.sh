echo "start speech_service flask app"
flask --app speech_service.app --debug run -p 9090 -h 0.0.0.0