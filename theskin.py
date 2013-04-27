import urwid
import themeat
import os
from collections import deque

#library = themeat.processlibrary(themeat.openlibrary('testing.xml'))
library = themeat.processlibrary(themeat.openlibrary('iTunesMusicLibrary.xml'))

recentitems = deque(['','','','',''])

def viewtrackinfo(button):
    track = library.tracks[button.label[0:button.label.index(':')]]
    info = urwid.Text('\'Done\' to exit, esc to go back\n\nName: {0}\nArtist: {1}\nAlbum: {2}\nAlbum Artist: {3}\nYear: {4}\nLength: {5} seconds\nGenre: {6}\nPlay count: {7}\nSkip count: {8}\nLocation: {9}\n'.format(track.name,track.artist,track.album,track.album_artist,track.year,track.length,track.genre,track.play_count,track.skip_count,track.location))
    done = menu_button('Done',exit_program)
    top.open_box(urwid.Filler(urwid.Pile([info,done])))


def viewplaylists(array):
    ret = []
    for p in array:
        ret.append(menu_button(p,gettracksonplaylist))
    return ret

def listtemplates():
    ret = []
    for t in  os.listdir('templates'):
        ret.append(menu_button(t, listplaylistsforconversion))
    return ret

def listplaylistsforconversion(button):
    recentitems.appendleft(button.label)
    recentitems.pop()
    ret = []
    for p in library.listplaylists():
        ret.append(menu_button(p, convert))
    contents = menu('Select playlist:',ret)
    top.open_box(contents)

def getattrsunderNsongs(button):
    recentitems.appendleft(button.label[0:-1].lower())
    recentitems.pop()
    ret = [];
    for i in xrange(1,25):
        ret.append(menu_button(str(i),simpleattrsunderN))
    top.open_box(menu('Under how many?',ret))


def gettracksby(button):
    tracks = library.gettrackswithattribute(recentitems[0], button.label)
    ret = []
    for t in tracks:
        ret.append(menu_button(t.tostring(),viewtrackinfo))
    top.open_box(menu('',ret))

def simpleattrsunderN(n):
    attrs = library.getattributeunderNinstances(recentitems[0], int(n.label))
    ret = []
    for a in attrs:
        ret.append(menu_button(a,gettracksby))
    top.open_box(menu('Under {0} tracks:'.format(n.label),ret))

def convert(button):
    library.convertplaylist(button.label[0:button.label.index(':')], recentitems[0])
    success()

def gettracksonplaylist(button):
    ret = []
    for t in library.playlists[button.label[0:button.label.index(':')]].tracks:
        ret.append(menu_button(library.tracks[t].tostring(),viewtrackinfo))
    contents = menu(button.label, ret)
    top.open_box(contents)

def menu_button(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def sub_menu(caption, choices):
    contents = menu(caption, choices)
    def open_menu(button):
        return top.open_box(contents)
    return menu_button([caption, u'...'], open_menu)

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def success():
    response = urwid.Text([u'Success!\nDone to quit, esc to go back'])
    done = menu_button(u'Done', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def exit_program(button):
    raise urwid.ExitMainLoop()

menu_top = menu(u'Main Menu', [
    sub_menu(u'View playlists', viewplaylists(library.listplaylists())),
    sub_menu(u'Convert playlist', listtemplates()),
    sub_menu(u'Get artists/albums with fewer than N songs', [menu_button('Artists',getattrsunderNsongs),menu_button('Albums',getattrsunderNsongs)]),
    menu_button('Exit program',exit_program)
])


#menu_top = menu(u'Main Menu', [
#    sub_menu(u'Applications', [
#        sub_menu(u'Accessories', [
#            menu_button(u'Text Editor', item_chosen),
#            menu_button(u'Terminal', item_chosen),
#        ]),
#    ]),
#    sub_menu(u'System', [
#        sub_menu(u'Preferences', [
#            menu_button(u'Appearance', item_chosen),
#        ]),
#        menu_button(u'Lock Screen', item_chosen),
#    ]),
#])

class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 8

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill(u'/'))
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)

top = CascadingBoxes(menu_top)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
