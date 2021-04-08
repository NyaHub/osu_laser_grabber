import sqlite3
import shutil
import os


class Map:
    FileInfo = []

    def __init__(self, con: sqlite3.Cursor, id):
        self.cur = con
        self.SetInfoID = id
        self.SetFileInfoTable = 'BeatmapSetFileInfo'
        self.SetInfoTable = 'BeatmapSetInfo'
        self.ext = '.osz'

        self.BeatmapMetadataID = self.cur.execute('select MetadataID from BeatmapSetInfo where ID='+str(self.SetInfoID)).fetchone()[0]

        res = self.cur.execute(
            'select OnlineBeatmapSetID from BeatmapSetInfo where MetadataID=' + str(self.BeatmapMetadataID)).fetchone()
        res = res[0] and [str(res[0])] or []
        res += self.cur.execute(
            'select Artist, Title from BeatmapMetadata where ID=' + str(self.BeatmapMetadataID)).fetchone()

        self.Artist = len(res) > 2 and res[1] or res[0]
        self.MapName = len(res) > 2 and res[2] or res[1]

        print(res)  # debug

        self.FileName = ' - '.join(res)
        print([self.MapName, self.Artist], self.FileName)  # debug

    def _get(self, path):
        self.get = FileGetter(self.cur, path, self.SetInfoTable, self.SetFileInfoTable, self.SetInfoID)
        self.get.getFiles()

    def _import(self, path):
        if(self.get is None):
            return
        self.get.importFile(path, self.FileName, self.ext)


class Skin:  # get info about skin by id
    FileInfo = []

    cur = None

    def __init__(self, con: sqlite3.Cursor, id):
        self.cur = con
        self.SetInfoID = id
        self.SetFileInfoTable = 'SkinFileInfo'
        self.SetInfoTable = 'SkinInfo'
        self.ext = '.osk'

        res = self.cur.execute(
            'select Creator, Name from ' + self.SetInfoTable + ' where ID=' + str(self.SetInfoID)).fetchone()

        self.Creator = res[0]
        self.SkinName = res[1]

        print(res)  # debug

        self.FileName = self.SkinName
        print([self.Creator, self.SkinName], self.FileName)  # debug

    def _get(self, path):
        self.get = FileGetter(self.cur, path, self.SetInfoTable, self.SetFileInfoTable, self.SetInfoID)
        self.get.getFiles()

    def _import(self, path):
        if (self.get is None):
            return
        self.get.importFile(path, self.FileName, self.ext)


class FileGetter:  # get and pack files
    FileInfo = []

    def __init__(self, con: sqlite3.Cursor,
                 path,  # path to osu files
                 SetInfoTable,  # name of table with info of map or skin
                 SetFileInfoTable,  # name of table with info of file
                 SetInfoID  # id entity in info table
                 ):
        self.SetFileInfoTable = SetFileInfoTable
        self.SetInfoTable = SetInfoTable
        self.SetInfoID = SetInfoID
        self.cur = con
        self.osuPath = os.path.join(path, 'files/')

    # get list of files
    def getFiles(self):
        self.FileInfo.clear()
        filesOrigin = self.cur.execute(
            'select FileInfoID, Filename from ' + self.SetFileInfoTable + ' where ' + self.SetInfoTable + 'ID=' + str(
                self.SetInfoID)).fetchall()

        for i in filesOrigin:
            FileHash = self.cur.execute('select Hash from FileInfo where ID=' + str(i[0])).fetchall()
            self.FileInfo.append([i[0], i[1], FileHash[0][0]])

    # pack files
    def importFile(self, path,  # path for packed files
                   file_name,  # out file name
                   ext  # extension out file
                   ):
        if not os.path.isdir('./tmp/'):
            os.mkdir('./tmp')
        tempDir = './tmp/' + str(self.SetInfoID)
        os.mkdir(tempDir)

        folgers = []
        for i in self.FileInfo:
            filePath = self.osuPath + i[2][0] + '/' + i[2][0:2] + '/' + i[2]
            f = i[1].split('/')
            if len(f) > 1:
                fl = ''
                for j in f:
                    fl += j
                    if (not (fl in folgers)) and (fl != i[1]):
                        folgers.append(fl)
                        os.mkdir(os.path.join(tempDir, fl))
                    fl += "/"

            if not os.path.isdir(os.path.join(tempDir, i[1])):
                shutil.copyfile(filePath, os.path.join(tempDir, i[1]))

        shutil.make_archive(os.path.join(path, file_name), "zip", tempDir)
        os.rename(os.path.join(path, file_name + ".zip"), os.path.join(path, file_name + ext))

        shutil.rmtree(tempDir)
