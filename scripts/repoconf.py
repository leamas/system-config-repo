#!/usr/bin/env python3

''' Simple repository maintenance app. '''


import configparser
import os
import os.path
import re
import subprocess
import sys
import tempfile

from urllib.request import urlopen

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from gi.repository import Gtk         # pylint: disable=no-name-in-module
from gi.repository import GObject     # pylint: disable=no-name-in-module
from gi.repository.Pango import FontDescription  # pylint: disable=F0401,E0611

import version


VERSION = "Version: %s ( %s %s )" % (
    version.VERSION, version.COMMIT, version.DATE.split()[0])

USAGE = \
'''Usage: system-config-repo <repofile>

<repofile> is a path to a yum repository file. If not absolute interpreted
as relative to /etc/yum.repos.d/. See manpage system-config-repo(1) for more.
'''


def here(path):
    ' Return path added to current dir for __file__. '
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def _error_dialog(parent_window, message):
    ''' Simple modal error dialog. '''
    dialog = Gtk.MessageDialog(parent_window,
                               Gtk.DialogFlags.DESTROY_WITH_PARENT
                                   | Gtk.DialogFlags.MODAL,
                               Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.OK,
                               message)
    dialog.run()
    dialog.destroy()


def _parse_repo(repofile):
    ''' Return the parsed repo data. '''
    config = configparser.ConfigParser()
    try:
        config.read(repofile)
    except configparser.MissingSectionHeaderError as ex:
        raise ValueError(str(ex))
    return config


def _parse_commandline():
    ''' Parse commandline, return (repofile, repo_id). '''
    if len(sys.argv) == 1:
        return None, None
    if not (1 < len(sys.argv) < 3):
        sys.stderr.write(USAGE)
        sys.exit(1)
    if sys.argv[1] in ['-h', '--help']:
        sys.stderr.write(USAGE)
        sys.exit(0)
    repofile = sys.argv[1]
    if not os.access(repofile, os.R_OK):
        repofile = os.path.join('/etc/yum.repos.d', repofile)
    if not os.access(repofile, os.R_OK):
        raise OSError("Cannot open : " + repofile + "\n")
    try:
        reply = subprocess.check_output(['rpm', '-qf', repofile])
        repo_id = reply.decode('utf-8').rsplit('-', 2)[0]
    except subprocess.CalledProcessError:
        try:
            basename = os.path.basename(repofile).split('.', 1)[0]
        except (ValueError, IndexError):
            raise OSError("Bad filename: " + repofile + "\n")
        repo_id = basename + '-repo'
    return repofile, repo_id


def _update_repofile(config, path, main_window):
    ''' Update repofile using data in config. '''

    if os.access(path, os.W_OK):
        with open(path, 'w') as f:
            config.write(f)
        return
    tmpfile = tempfile.mkstemp()[1]
    with open(tmpfile, 'w') as f:
        config.write(f)
    os.environ['SUDO_ASKPASS'] = here('sudo_askpass')
    try:
        subprocess.check_call(
            ['sudo', '-A', here('update-repo'), path, tmpfile])
    except subprocess.CalledProcessError as ex:
        _error_dialog(main_window, 'Cannot update repo file: ' + str(ex))
    finally:
        os.unlink(tmpfile)


class Data(object):
    ''' Wrapper fo all data sources: appdata, package info, etc. '''

    class _PkgInfo(object):
        ''' Wrapper for data in rpm database. '''

        def __init__(self, pkg):
            for attr in ['description', 'summary', 'url']:
                try:
                    cmd = ('rpm -q --qf %%{%s} ' % attr) + pkg
                    value = \
                        subprocess.check_output(cmd.split()).decode('utf-8')
                except (subprocess.CalledProcessError, OSError):
                    value = None
                setattr(self, attr, value)

    class _Appdata(object):
        ''' Gnome appdata wrapper. '''

        def __init__(self, repo_id):
            for attr in ['description', 'summary', 'url']:
                setattr(self, attr, None)
            path = '/usr/share/appdata/%s.appdata.xml' % repo_id
            if not os.path.exists(path):
                return
            tree = ET.parse(path)
            for attr in ['description', 'summary', 'url']:
                elem = tree.find(attr)
                if elem:
                    setattr(self, attr, str(elem[0].text).strip())

    class _Repodata(object):
        ''' Wraps data in /usr/share/system-config-repo/repos dir. '''
        REPOS = '/usr/share/system-config-repo/repos'

        def __init__(self, repo_id):
            self.repo_id = repo_id
            for key in ['description', 'summary', 'url']:
                base = os.path.join(self.REPOS, self.repo_id)
                key_path = os.path.join(base, key + '.txt')
                if os.path.exists(key_path):
                    with open(key_path) as f:
                        setattr(self, key, f.read().strip())

    def __init__(self, repo_id, repofile, pkg):
        self.repodata = self._Repodata(repo_id)
        self.pkg_info = self._PkgInfo(pkg)
        self.appdata = self._Appdata(repo_id)
        self.defaults = self._Repodata('Default')
        self.repo_id = repo_id
        self.repofile = repofile

    def _get_item(self, item):
        ''' Get a named item (summary, url etc.) from right source. '''
        for source in \
        [self.repodata, self.appdata, self.pkg_info, self.defaults]:
            if hasattr(source, item) and getattr(source, item):
                return getattr(source, item)
        return None

    @property
    def summary(self):
        ''' Get the summary field. '''
        return self._get_item('summary')

    @property
    def description(self):
        ''' Get the description field. '''
        descr = self._get_item('description')
        return re.sub(r'[ \n]+', ' ', descr) if descr else None

    @property
    def url(self):
        ''' Get the url field. '''
        return self._get_item('url')

    @property
    def icon(self):
        ''' Get the icon (only in repodata). '''
        key = re.sub('-repo$', '', self.repo_id)
        path = os.path.join(self._Repodata.REPOS, key, 'icon.png')
        if os.path.exists(path):
            return path
        return os.path.join(self._Repodata.REPOS, 'Default', 'icon.png')


class FileChooserWindow(Gtk.Window):
    '''File chooser dialog for selecting repo file. '''

    def __init__(self, main_window):
        Gtk.Window.__init__(self, title="Open repository file")
        self.main_window = main_window

    def run(self):
        ''' Run the dialog, possibly launching new window. '''

        buttons = (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        dialog = Gtk.FileChooserDialog("Please choose a file",
                                       self,
                                       Gtk.FileChooserAction.OPEN,
                                       buttons)
        dialog.set_current_folder('/etc/yum.repos.d')
        filter_repos = Gtk.FileFilter()
        filter_repos.set_name("Repository files.")
        filter_repos.add_pattern('*.repo')
        dialog.add_filter(filter_repos)
        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files.")
        filter_all.add_pattern('*')
        dialog.add_filter(filter_all)
        dialog.connect("delete-event", lambda w, d: dialog.destroy())
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                subprocess.check_call(['gtk-launch',
                                       'system-config-repo',
                                       dialog.get_filename()])
            except (OSError, subprocess.CalledProcessError):
                _error_dialog(self.main_window,
                              "Cannot run open command...")
        dialog.destroy()


class Handler(object):
    ''' Init window and handle signals. '''


    def can_update(self):
        ''' Return True if user can update the repository file. '''
        if os.access(self.repofile, os.W_OK):
            return True
        try:
            with open('/dev/null', 'w') as devnull:
                subprocess.check_call(['sudo', '-l', here('update-repo')],
                                      stdout=devnull, stderr=devnull)
            return True
        except subprocess.CalledProcessError:
            return False

    def show_some_text(self, title, text):
        '''  Show some text in a textview. '''

        def cb_on_view_ok_btn_clicked(button, data=None):
            ''' OK button on view_some_text window. '''
            button.get_toplevel().hide()
            return True

        def cb_on_window_delete_event(window, event):
            ''' Generic window close event. '''
            window.hide()
            return True

        textview = self.builder.get_object("view_textview")
        textview.modify_font(FontDescription("Monospace"))
        buf = textview.get_buffer()
        buf.set_text(text)
        w = self.builder.get_object('view_window')
        w.set_title(title)
        w.connect('delete-event', cb_on_window_delete_event)
        b = self.builder.get_object('view_ok_btn')
        b.connect('clicked', cb_on_view_ok_btn_clicked)
        w.set_size_request(600, 600)
        w.show_all()
        return w

    def show_repo(self, repofile):
        ''' Read-only repo display in a textview. '''
        try:
            with open(repofile) as f:
                text = f.read()
        except OSError:
            _error_dialog(self.main_window,
                          "Cannot open repofile: " + repofile)
            return None
        title = "system-config-repo: " + os.path.basename(repofile)
        self.show_some_text(title, text)

    def show_signing_key(self, uri):
        ''' Display the signing key at uri in a text window. '''
        try:
            socket = urlopen(uri)
            text = socket.read().decode('utf-8')
        except IOError as ex:
            _error_dialog(self.main_window,
                          "Cannot open %s: %s." % (uri, str(ex)))
            return True
        keyfile = tempfile.mkstemp()[1]
        with open(keyfile, 'w') as f:
            f.write(text)
        try:
            metadata = subprocess.check_output(
                 ['gpg', '--with-fingerprint', keyfile]).decode('utf-8')
        except subprocess.CalledProcessError:
            metadata = '(Cannot retrieve metadata uing gpg)'
        finally:
            os.unlink(keyfile)
        text = metadata + "\n" + text
        title = "system-config-repo: " + os.path.basename(uri)
        self.show_some_text(title, text)

    def show_packagelist(self):
        ''' Generate a package list using repoquery and display it. '''
        cmd = 'repoquery -qa --disablerepo=*'
        for section in self.config.sections():
            cmd += ' --enablerepo=' + section
        try:
            pkglist = subprocess.check_output(cmd.split()).decode('utf-8')
        except subprocess.CalledProcessError as ex:
            _error_dialog(self.main_window,
                          "Cannot retrieve package list: " + str(ex))
            return True
        title = 'system-config-repo: Package list'
        self.show_some_text(title, pkglist)
        return True

    def init_about(self):
        ''' Install the Help | About dialog. '''
        # See: https://developer.gnome.org/gtk3/stable/GtkAboutDialog.html
        about = Gtk.AboutDialog()
        about.set_program_name('system-config-repo')
        about.set_version(VERSION)
        about.set_logo_icon_name('system-config-repo')
        about.set_copyright("Copyright \xc2\xa9 2014 Alec Leamas")
        #about.set_authors(authors)
        about.set_website("http://github.com/leamas/system-config-repo")
        about.set_website_label("Github project home")
        about.connect("response", lambda w, d: w.hide())
        self.builder.get_object("about_menuitem").connect(
            "activate", lambda w, a: a.show(), about)

    def init_logo(self):
        ''' Set up the dialog logo.'''
        widget = self.builder.get_object('logo_align')
        child = widget.get_child()
        if child:
            widget.remove(child)
        icon = self.data.icon
        image = Gtk.Image.new_from_file(icon)
        widget.add(image)

    def init_summary(self):
        ''' Set up the summary field. '''

        def on_summary_activate_cb(widget, data=None):
            ''' User clicked on More.../Less.. link in summary. '''
            see_link_hbox = self.builder.get_object('see_link_hbox')
            if widget.get_label().startswith('Less'):
                widget.set_label('More...')
                label.set_text(summary)
                see_link_hbox.set_visible(False)
            else:
                widget.set_label('Less...')
                label.set_text(self.data.description)
                see_link_hbox.set_visible(True)
            return True

        label = self.builder.get_object('summary_lbl')
        see_link = self.builder.get_object('see_link')
        if self.data.url:
            see_link.set_uri(self.data.url)
            see_link.set_label(self.data.url)
        else:
            see_link.hide()
        widget = self.builder.get_object('summary_more_link')
        if not self.data.description or not self.data.summary:
            summary = self.repofile + "\n(No data available)"
        else:
            summary = self.data.summary
        widget.set_label('Less...')
        on_summary_activate_cb(widget)
        widget.connect('activate-link', on_summary_activate_cb)

    def init_repolist(self, config):
        ''' Set up the repolist to be ready for an update. '''

        def on_key_link_activate_cb(widget, uri):
            ''' User clicks in signing key link. '''
            self.show_signing_key(uri)
            return True

        def on_checkbox_toggled_cb(widget, data):
            ''' User toggled 'Enabled' or 'Signed'. '''
            (section, item) = data
            value = '1' if widget.get_active() else '0'
            config.set(section, item, value)
            _update_repofile(config, self.repofile, self.main_window)
            return True

        def get_checkbox(section, label, item, enabled=True):
            ''' Return Enabled or Signed checkbox. '''
            box = Gtk.CheckButton()
            box.set_label(label)
            box.set_alignment(0, 0.5)
            try:
                box.set_active(config.getboolean(section, item))
            except configparser.NoOptionError:
                box.set_active(False)
            box.set_sensitive(self.can_update() and enabled)
            box.connect('toggled', on_checkbox_toggled_cb, (section, item))
            return box

        def get_keylink(section):
            ''' Return link to signing key. '''
            try:
                link = Gtk.LinkButton(config.get(section, 'gpgkey'))
            except configparser.NoOptionError:
                link = Gtk.LinkButton('http://not-found')
                link.set_sensitive(False)
            link.set_label('Signing key...')
            link.set_alignment(0, 0.5)
            link.connect(
                'activate-link', on_key_link_activate_cb, link.get_uri())
            return link

        def get_label(section):
            ''' Return the initial label for every repo in file. '''
            label = Gtk.Label()
            if config.has_option(section, 'name'):
                text = config.get(section, 'name')
            elif config.has_option(section, 'description'):
                text =  section + ': ' + config.get(section, 'description')
            else:
                text = section
            label.set_text(text)
            label.set_alignment(0, 0.5)
            return label

        top = self.builder.get_object('repolist_align')
        child = top.get_child()
        if child:
            top.remove(child)
        top_vbox = Gtk.VBox()
        top.add(top_vbox)
        for section in config.sections():
            vbox = Gtk.VBox()
            top_vbox.add(vbox)
            vbox.add(Gtk.HSeparator())
            if len(config.sections()) > 1 or config.has_option(section,
                                                               'description'):
                vbox.add(get_label(section))
            vbox.add(get_checkbox(section, 'Enabled', 'enabled'))
            has_key = config.has_option(section, 'gpgkey')
            vbox.add(get_checkbox(section, 'Signed', 'gpgcheck', has_key))
            vbox.add(get_checkbox(
                section,'Skip if unavailable', 'skip_if_unavailable'))
            if has_key:
                vbox.add(get_keylink(section))

    def static_connect(self, builder):
        ''' Connect static signals. '''

        def on_delete_cb(window_, event):
            ''' User just closed window. '''
            Gtk.main_quit()

        def on_view_repo_clicked_cb(button, data=None):
            ''' Display the repository source file. '''

            def do_view_repo():
                ''' Do the dirty work. '''
                self.show_repo(self.repofile)
                self.builder.get_object('main_window').set_sensitive(True)

            self.builder.get_object('main_window').set_sensitive(False)
            GObject.idle_add(do_view_repo)

        def on_main_list_clicked_cb(button, data=None):
            ''' User pushes 'List packages' button. '''
            self.show_packagelist()

        def on_manpage_activate_cb(button, data=None):
            ''' Display manpage... '''

            def do_manpage():
                ''' Do the dirty work. '''
                try:
                    subprocess.call(
                        ['yelp', 'man:' + here('../system-config-repo.1')])
                except subprocess.CalledProcessError:
                    pass
                self.builder.get_object('main_window').set_sensitive(True)

            self.builder.get_object('main_window').set_sensitive(False)
            GObject.idle_add(do_manpage)

        def on_file_open_activate_cb(button, data=None):
            ''' File|Open menu item. '''
            FileChooserWindow(self.main_window).run()
            return True

        connections = [
           ('main_window', 'delete-event', on_delete_cb),
           ('main_ok_btn', 'clicked', Gtk.main_quit),
           ('main_view_btn','clicked',on_view_repo_clicked_cb),
           ('main_list_btn','clicked', on_main_list_clicked_cb),
           ('quit_menuitem', 'activate', Gtk.main_quit),
           ('manpage_item', 'activate', on_manpage_activate_cb),
           ('open_file_item', 'activate', on_file_open_activate_cb)
        ]
        for (widget, signal, callback) in connections:
            builder.get_object(widget).connect(signal, callback)

    def init_window(self, builder, config):
        ''' Initiate window, prepare for an update. '''
        w = self.builder.get_object('main_window')
        w.set_title('system-config-repo')
        self.static_connect(builder)
        self.init_about()
        self.init_logo()
        self.init_summary()
        self.init_repolist(config)

    def __init__(self, builder):
        self.builder = builder
        self.main_window = builder.get_object('main_window')
        try:
            self.repofile, self.repo_id = _parse_commandline()
        except OSError as ex:
            _error_dialog(self.main_window, str(ex))
            sys.exit(1)
        if not self.repofile:
            FileChooserWindow(self.main_window).run()
            sys.exit(0)
        self.data = Data(self.repo_id, self.repofile, self.repo_id)
        try:
            self.config = _parse_repo(self.repofile)
        except (configparser.Error, ValueError) as ex:
            _error_dialog(self.main_window,
                          "Cannot parse repository: " + str(ex) + "\n")
            sys.exit(2)
        self.init_window(builder, self.config)
        builder.get_object('main_window').show_all()
        builder.get_object('see_link_hbox').hide()
        if not self.data.description:
            builder.get_object('summary_more_link').hide()



def main():
    ''' Indeed: main program. '''
    builder = Gtk.Builder()
    builder.add_from_file(here("system-config-repo.ui"))
    builder.connect_signals(Handler(builder))
    Gtk.main()


if __name__ == '__main__':
    main()

# vim: set expandtab ts=4 sw=4:
