
streamlink --loglevel error  --player-fifo --force --ffmpeg-video-transcode h264 "https://www.twitch.tv/[STREAMERHERE]" best -o /tmp/outpipe &
python3 main.py
