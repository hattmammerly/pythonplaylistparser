from lxml import etree
import time

class Library:
    __slots__ = ('name','tracks','playlists');
    def listplaylists(self):
        s = 'Playlists:';
        for k,p in self.playlists.iteritems():
            s = s + '\n{0}: {1}'.format(k,p.name);
        return s;
    def tostring(self):
        string = 'Tracks:';
        for t in self.tracks.itervalues():
            string = string + '\n\t{0}'.format(t.tostring());
        string = string + '\n\nPlaylists:';
        for p in self.playlists.itervalues():
            string = string + '\n\t{0}'.format(p.tostring());
    def playlisttostring(self, key):
        s = '{0}:'.format(self.playlists[key].name);
        for t in self.playlists[key].tracks:
            s = s + '\n\t{0}'.format(self.tracks[t].tostring());
        return s;
    def gettrackswithattribute(self, attr, val):
        if attr == 'album':
            return self.gettracksonalbum(val);
        ret = [];
        for t in self.tracks.itervalues():
            try:
                if getattr(t,attr) == val:
                    ret.append(t);
            except AttributeError as e:
                pass;
        return ret; # return, for example, list of tracks by artist Norah Jones
    def gettracksonalbum(self,val):
        ret = [];
        artist = val[0:val.index(': ')];
        album = val[val.index(': ') + 2:];
        try:
            for t in self.tracks.itervalues():
                if t.artist == artist and t.album == album:
                    ret.append(t);
        except AttributeError as e:
            pass;
        return ret;
    def getattributeunderNinstances(self, attr, n):
        ret = [];
        vals = {}; # return list of, for example, artists with <n tracks
        for t in self.tracks.itervalues():
            try:
                if attr == 'album':
                    val = u'{0}: {1}'.format(getattr(t,'artist'), getattr(t,attr));
                else:
                    val = getattr(t,attr);
            except AttributeError as e:
                val = '';
            if val in vals:
                vals[val] = vals[val] + 1;
            else:
                vals[val] = 1;
        for k,v in vals.iteritems():
            if v <= n:
                ret.append(k);
        return ret;
    def __init__(self):
        self.name = 'iTunesMusicLibrary.xml';
        self.tracks = {};
        self.playlists = {};

class Track:
    __slots__ = ('name','artist','album_artist','album','genre','length','year','bpm','date_added','bit_rate','play_count','skip_count','purchased','location');
    def tostring(self):
        return "{0} - {1}".format(self.artist, self.name);
    def __init__(self):
        self.year = '0000';
        self.purchased = False;
        self.location = '';

class Playlist:
    __slots__ = ('name','smart','tracks');
    def __init__(self):
        self.smart = False;
        self.tracks = {};

def openlibrary(loc):
    try:
        xml = open(loc);
        tree = etree.parse(xml);
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror);
        return;
    return etree._ElementTree.getroot(tree);

def processlibrary(tree):
    tracksxml = tree[0][-3];  #there's probably a better way to parse
    playlistsxml = tree[0][-1]; #but since it's always <key/><value/> this will always work

    tracks = {};
    for i in xrange(1,len(tracksxml), 2):
        trackno = tracksxml[i-1].text;
        tracks[trackno] = Track();
        for x in xrange(0,len(tracksxml[i]), 2): # this could be cleaned using the infos list, possibly
            val = tracksxml[i][x+1].text;
            if tracksxml[i][x].text == "Name":
                tracks[trackno].name = val;
            elif tracksxml[i][x].text == "Artist":
                tracks[trackno].artist = val;
            elif tracksxml[i][x].text == "Album Artist":
                tracks[trackno].album_artist = val;
            elif tracksxml[i][x].text == "Album":
                tracks[trackno].album = val;
            elif tracksxml[i][x].text == "Genre":
                tracks[trackno].genre = val;
            elif tracksxml[i][x].text == "Total Time":
                tracks[trackno].length = int(val)/1000; # itunes library gives time in milliseconds
            elif tracksxml[i][x].text == "Year":
                tracks[trackno].year = val;
            elif tracksxml[i][x].text == "BPM":
                tracks[trackno].bpm = val;
            elif tracksxml[i][x].text == "Date Added":
                tracks[trackno].date_added = val;
            elif tracksxml[i][x].text == "Bit Rate":
                tracks[trackno].bit_rate = val;
            elif tracksxml[i][x].text == "Play Count":
                tracks[trackno].play_count = val;
            elif tracksxml[i][x].text == "Skip Count":
                tracks[trackno].skip_count = val;
            elif tracksxml[i][x].text == "Purchased":
                tracks[trackno].purchased = True;
            elif tracksxml[i][x].text == "Location":
                tracks[trackno].location = val;

    playlists = {};
    for i in xrange(0,len(playlistsxml)):
        playlist = playlistsxml[i];
        playlistno = playlist[3].text;
        playlists[playlistno] = Playlist();
        for x in xrange(0,len(playlistsxml[i]) - 1):
            val = playlistsxml[i][x+1].text;
            if playlistsxml[i][x].text == "Name":
                playlists[playlistno].name = val;
            elif playlistsxml[i][x].text == "Smart Info":
                playlists[playlistno].smart = True;
            elif playlistsxml[i][x].text == "Playlist Items":
                tracklist = [];
                for z in xrange(0,len(playlistsxml[i][x+1])):
                    tracklist.append(playlistsxml[i][x+1][z][1].text);
                playlists[playlistno].tracks = tracklist;
    lib = Library();
    lib.tracks = tracks;
    lib.playlists = playlists;
    return lib;

def convertplaylist(key, form):
    infos = ['name','artist','album_artist','album','genre','length','year','bpm','date_added','bit_rate','play_count','skip_count','purchased','location'];
    try:
        template = open("templates/{0}".format(form));
    except IOError as e:
        print 'could not open template file: templates/{0}'.format(form);
        return;
    tracktemplate = template.read();
    try:
        f = open('playlists/{0}.{1}'.format(playlists[key].name, form),'w+')
    except IOError as e:
        print 'could not write playlist file: playlists/{0}.{1}'.format(playlists[key].name,form);
        return;
    output = tracktemplate[:tracktemplate.index('<!--TRACK-->\n')];
    start = tracktemplate.index('<!--TRACK-->\n') + 13;
    tracktemplate = tracktemplate[start:tracktemplate.index('<!--END-->')];
    for track in playlists[key].tracks:
        t = tracks[track];
        tmp = tracktemplate
        for i in infos:
            try:
                tmp = tmp.replace('%track{0}'.format(i), str(getattr(t, i)));
            except AttributeError as e:
                pass;
        output = output + tmp;
    f.write(output);

