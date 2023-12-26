ps  -ef | grep python |grep monitor.py| grep -v grep | awk '{print $2}' | xargs kill -9
nohup /opt/anaconda3/envs/py39/bin/python monitor.py >> ./monitor.log 2>&1 &


#/etc/init.d/redis-server restart
#/etc/redis/redis.conf