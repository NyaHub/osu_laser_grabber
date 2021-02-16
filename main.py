import sqlite3
from beatmap import Map
import os

path = '/home/vladimir/.local/share/osu/'

db = 'client.db'

con = sqlite3.connect(path+db)
cur = con.cursor()

maps = []

res = cur.execute('select ID, MetadataID from BeatmapSetInfo;').fetchall()
# res = cur.execute('select ID, MetadataID from BeatmapSetInfo where ID=9;').fetchall()

if not os.path.isdir('./tmp'):
    os.mkdir('./tmp')
if not os.path.isdir('./maps'):
    os.mkdir('./maps')

ok = False
for i in res:
    # if ok or i[0]==116:
    #     ok = True
    # else:
    #     continue
    maps.append(Map(con, path, i[0], i[1]))
    maps[-1].importMap("maps/")
    
    progress = cur.execute('select count(*) from BeatmapSetInfo where ID<='+str(i[0])).fetchall()[0][0]/cur.execute('select count(*) from BeatmapSetInfo').fetchall()[0][0] * 100
    print("%.0f" % progress)

con.close()
