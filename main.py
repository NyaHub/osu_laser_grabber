import sqlite3
from beatmap import Map, Skin
import os
from tkinter import *

path = '/home/vladimir/.local/share/osu/'
db = 'client.db'
out_skins = './skins/'
out_maps = './maps/'

if not os.path.isdir(out_skins):
    os.mkdir(out_skins)
if not os.path.isdir(out_maps):
    os.mkdir(out_maps)

con = sqlite3.connect(path + db)
cur = con.cursor()

res = cur.execute('select ID from BeatmapSetInfo;').fetchall()  # get all maps ids

maps = []
for i in res:
    maps.append(Map(cur, i[0]))
    # maps[-1]._get(out_maps)
    # maps[-1]._import('./maps')

res = cur.execute('select ID from SkinInfo;').fetchall()  # get all skins ids

skins = []
for i in res:
    skins.append(Skin(cur, i[0]))
    # skins[-1]._get(out_skins)
    # skins[-1]._import('./maps')

window = Tk()
window.title("title")
window.mainloop()
con.close()
