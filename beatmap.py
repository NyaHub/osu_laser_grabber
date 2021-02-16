import sqlite3
import shutil
import os

class Map:
    
    BeatmapSetInfoID = 0
    BeatmapMetadataID = 0
    FileInfo = []
    MapName = ''
    
    cur = None
    
    def __init__(self, con: sqlite3.Connection, path, id, metaID):
        self.cur = con.cursor()
        self.BeatmapSetInfoID = id
        self.osuPath = os.path.join(path,'files/')
        self.BeatmapMetadataID = metaID
        
        res = self.cur.execute('select ArtistUnicode, TitleUnicode from BeatmapMetadata where ID='+str(self.BeatmapMetadataID)).fetchall()[0]
        if res[0]==None or res[1]==None:
            res = self.cur.execute('select Artist, Title from BeatmapMetadata where ID='+str(self.BeatmapMetadataID)).fetchall()[0]
        
        self.MapName = ' - '.join(res)
        print(metaID, self.MapName)
        self.getMap()
        
    def getMap(self):
        self.FileInfo.clear()
        filesOrigin = self.cur.execute('select FileInfoID, Filename from BeatmapSetFileInfo where BeatmapSetInfoID='+str(self.BeatmapSetInfoID)).fetchall()
        
        for i in filesOrigin:
            FileHash = self.cur.execute('select Hash from FileInfo where ID='+str(i[0])).fetchall()
            self.FileInfo.append([i[0], i[1], FileHash[0][0]])
    
    def importMap(self, path):
        tempDir = './tmp/'+str(self.BeatmapSetInfoID)
        os.mkdir(tempDir)
        folgers = []
        for i in self.FileInfo:
            filePath = self.osuPath+i[2][0]+'/'+i[2][0:2]+'/'+i[2]
            f = i[1].split('/')
            if len(f)>1:
                fl = ''
                for j in f:
                    fl += j
                    # print(fl, i[1])
                    if (not (fl in folgers)) and (fl != i[1]):
                        folgers.append(fl)
                        os.mkdir(os.path.join(tempDir, fl))
                    fl += "/"
            
            if not os.path.isdir(os.path.join(tempDir, i[1])):
                shutil.copyfile(filePath, os.path.join(tempDir, i[1]))
        
        shutil.make_archive(os.path.join(path,self.MapName), "zip", tempDir)
        os.rename(os.path.join(path,self.MapName+".zip"), os.path.join(path,self.MapName+".osz"))
        
        shutil.rmtree(tempDir)