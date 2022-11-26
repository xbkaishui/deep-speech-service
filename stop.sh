# clean data
rm -rf *.wav
rm -rf *.mp3
# stop gunicorn
ps -ef | grep gunicorn
ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -9