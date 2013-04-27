from lxml import etree
import time

class Library:
    __slots__ = (u'name',u'tracks',u'playlists')
    def listplaylists(self):
        ret = []
        for k,p in self.playlists.iteritems():
            ret.append(u'{0}: {1}'.format(k,p.name))
        return ret
    def gettracksonplaylist(self,key):
        ret = []
        for t in self.playlists[key].tracks:
            ret.append(self.tracks[t])
        return ret
    def tostring(self):
        string = u'Tracks:'
        for t in self.tracks.itervalues():
            string = string + u'\n\t{0}'.format(t.tostring())
        string = string + u'\n\nPlaylists:'
        for p in self.playlists.itervalues():
            string = string + u'\n\t{0}'.format(p.tostring())
    def playlisttostring(self, key):
        s = u'{0}:'.format(self.playlists[key].name)
        for t in self.playlists[key].tracks:
            s = s + u'\n\t{0}'.format(self.tracks[t].tostring())
        return s
    def gettrackswithattribute(self, attr, val):
        if attr == u'album':
            return self.gettracksonalbum(val)
        ret = []
        for t in self.tracks.itervalues():
            try:
                if getattr(t,attr) == val:
                    ret.append(t)
            except AttributeError as e:
                pass
        return ret; # return, for example, list of tracks by artist Norah Jones
    def gettracksonalbum(self,val):
        ret = []
        artist = val[0:val.index(u': ')]
        album = val[val.index(u': ') + 2:]
        try:
            for t in self.tracks.itervalues():
                if t.artist == artist and t.album == album:
                    ret.append(t)
        except AttributeError as e:
            pass
        return ret
    def getattributeunderNinstances(self, attr, n):
        ret = []
        vals = {}; # return list of, for example, artists with <n tracks
        for t in self.tracks.itervalues():
            try:
                if attr == u'album':
                    val = u'{0}: {1}'.format(t.artist, t.album)
                else:
                    val = getattr(t,attr)
            except AttributeError as e:
                val = u''
            if val in vals:
                vals[val] = vals[val] + 1
            else:
                vals[val] = 1
        for k,v in vals.iteritems():
            if v <= n:
                ret.append(k)
        return ret
    def convertplaylist(self,key, form):
        infos = [u'name',u'artist',u'album_artist',u'album',u'genre',u'length',u'year',u'bpm',u'date_added',u'bit_rate',u'play_count',u'skip_count',u'purchased',u'location']
        try:
            template = open('templates/{0}'.format(form))
        except IOError as e:
            print u'could not open template file: templates/{0}'.format(form)
            return
        tracktemplate = template.read()
        try:
            f = open(u'playlists/{0}.{1}'.format(self.playlists[key].name, form),u'w+')
        except IOError as e:
            print u'could not write playlist file: playlists/{0}.{1}'.format(self.playlists[key].name,form)
            return
        output = tracktemplate[:tracktemplate.index(u'<!--TRACK-->\n')]
        start = tracktemplate.index(u'<!--TRACK-->\n') + 13
        tracktemplate = tracktemplate[start:tracktemplate.index(u'<!--END-->')]
        def strip(string):
            if string[0:2] == "u'" or string[0:2] == 'u"':
                string = string[2:]
            elif string[0:1] == "'" or string[0:1] == '"':
                string = string[1:]
                if string[-1] == "'" or string[-1] == '"':
                    string = string[:-1]
            return string
        for track in self.playlists[key].tracks:
            t = self.tracks[track]
            tmp = tracktemplate
            for i in infos:
                try:
                    tmp = tmp.replace('%track{0}'.format(i), strip(repr(getattr(t, i))))
                except AttributeError as e:
                    pass
            output = output + tmp
        f.write(output)
    def __init__(self):
        self.name = u'iTunesMusicLibrary.xml'
        self.tracks = {}
        self.playlists = {}

class Track:
    __slots__ = (u'trackno'u'name',u'artist',u'album_artist',u'album',u'genre',u'length',u'year',u'bpm',u'date_added',u'bit_rate',u'play_count',u'skip_count',u'purchased',u'location')
    def tostring(self):
        return u'{0}: {1} - {2}'.format(self.trackno, self.artist, self.name)
    def __init__(self):
        self.trackno = u''
        self.name = u''
        self.artist = u''
        self.album = u''
        self.album_artist = u''
        self.year = u'0000'
        self.length = 0
        self.genre = u''
        self.play_count = 0
        self.skip_count = 0
        self.purchased = False
        self.location = u''

class Playlist:
    __slots__ = (u'name',u'smart',u'tracks')
    def __init__(self):
        self.smart = False
        self.tracks = {}

def openlibrary(loc):
    try:
        xml = open(loc)
        tree = etree.parse(xml)
    except IOError as e:
        print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
        return
    return etree._ElementTree.getroot(tree)

def processlibrary(tree):
    tracksxml = tree[0][-3];  #there's probably a better way to parse
    playlistsxml = tree[0][-1]; #but since it's always <key/><value/> this will always work

    tracks = {}
    for i in xrange(1,len(tracksxml), 2):
        trackno = tracksxml[i-1].text
        tracks[trackno] = Track()
        tracks[trackno].trackno = trackno
        for x in xrange(0,len(tracksxml[i]), 2): # this could be cleaned using the infos list, possibly
            val = tracksxml[i][x+1].text
            if tracksxml[i][x].text == 'Name':
                tracks[trackno].name = val
            elif tracksxml[i][x].text == 'Artist':
                tracks[trackno].artist = val
            elif tracksxml[i][x].text == 'Album Artist':
                tracks[trackno].album_artist = val
            elif tracksxml[i][x].text == 'Album':
                tracks[trackno].album = val
            elif tracksxml[i][x].text == 'Genre':
                tracks[trackno].genre = val
            elif tracksxml[i][x].text == 'Total Time':
                tracks[trackno].length = int(val)/1000; # itunes library gives time in milliseconds
            elif tracksxml[i][x].text == 'Year':
                tracks[trackno].year = val
            elif tracksxml[i][x].text == 'BPM':
                tracks[trackno].bpm = val
            elif tracksxml[i][x].text == 'Date Added':
                tracks[trackno].date_added = val
            elif tracksxml[i][x].text == 'Bit Rate':
                tracks[trackno].bit_rate = val
            elif tracksxml[i][x].text == 'Play Count':
                tracks[trackno].play_count = val
            elif tracksxml[i][x].text == 'Skip Count':
                tracks[trackno].skip_count = val
            elif tracksxml[i][x].text == 'Purchased':
                tracks[trackno].purchased = True
            elif tracksxml[i][x].text == 'Location':
                val = val.replace(u'file://localhost/C:',u'')
                #val = val.replace('\\','/')
                tracks[trackno].location = val

    playlists = {}
    for i in xrange(0,len(playlistsxml)):
        playlist = playlistsxml[i]
        playlistno = playlist[3].text
        playlists[playlistno] = Playlist()
        for x in xrange(0,len(playlistsxml[i]) - 1):
            val = playlistsxml[i][x+1].text
            if playlistsxml[i][x].text == 'Name':
                playlists[playlistno].name = val
            elif playlistsxml[i][x].text == 'Smart Info':
                playlists[playlistno].smart = True
            elif playlistsxml[i][x].text == 'Playlist Items':
                tracklist = []
                for z in xrange(0,len(playlistsxml[i][x+1])):
                    tracklist.append(playlistsxml[i][x+1][z][1].text)
                playlists[playlistno].tracks = tracklist
    lib = Library()
    lib.tracks = tracks
    lib.playlists = playlists
    return lib

