from subprocess import call
for i in range(1, 20):
    call(["ffmpeg", "-f", "image2", "-r", "24", "-i", "{}frame%d.jpg".format(i), "-vcodec", "mpeg4", "-y", "{}movie.mp4".format(i)])

