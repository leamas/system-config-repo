system-config-repo README.
==========================

This is a small GUI tool aimed to simplify packaging 3-rd party yum
repositories. It's basically just a dead simple view where users
can enable/disable, view the source file and list the packages.

In the examples directory are a number of packaged repos. The packaging
includes both desktop files and gnome appdata. Thus a repo packaged this
way will be found by the standard tools:
  - The desktop environment (Gnome/KDE etc) will find the desktop file and
    thus see the repository as an application.
  - The packaging utils (yum, dnf, etc.) will find the package.
  - Gnome software is able to find the package and show a screenshot.

## Security, users and such

The tool allows users to update the file if they have write access to the
/etc/yum.repos.d/ file or is member of the wheel group. See manpage
for more.

## License
This is open software licensed under the MIT license, see the LICENSE file.

## TODO

Lots...
 - Dozens of bugs...
 - Add a File|Open menu item.
 - More examples.
