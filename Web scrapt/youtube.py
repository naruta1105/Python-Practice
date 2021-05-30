from pytube import YouTube

link = "https://www.youtube.com/watch?v=Mgn5vGo8-6s&list=RDMgn5vGo8-6s&start_radio=1"
yt = YouTube(link)

# To print title
print("Title :", yt.title)
# To get number of views
print("Views :", yt.views)
# To get the length of video
print("Duration :", yt.length)
# To get description
print("Description :", yt.description)
# To get ratings
print("Ratings :", yt.rating)

stream = yt.streams.get_highest_resolution()
stream.download()
print("Download completed!!")