from subprocess import call
command = "ffmpeg -f image2 -r 24 -i {}frame%d.jpg -vcodec mpeg4 -y {}movie.mp4"
command = command.split(" ")
for range(1, 83):
    command[6] = command[6].format(i)
    command[-1] = command[-1].format(i  j)
    call(command.split(" "))

