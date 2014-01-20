system-config-repo README.
==========================

This is a small GUI tool aimed to simplify packaging 3-rd party yum
repositories. It's basically just a dead simple view where users
can enable/disable, view the source file and list the packages in
a repository file usually found in /etc/yum.repos.d

In the examples directory are a number of packaged repos. The packaging
includes both desktop files and gnome appdata. Thus a repo packaged this
way will be found by the standard tools:
  - The desktop environment (Gnome/KDE etc) will find the desktop file and
    thus see the repository as an application.
  - The packaging utils (yum, dnf, etc.) will find the package.
  - Gnome software is able to find the package and show a screenshot.

Besides handling packaged repos, the tool is designed to handle any
repository file in a consistent way.

## Security, users and such

The tool allows user to update the file if she has write access to the
repository file or is member of the wheel group. See manpage for more.

## License
This is open software licensed under the MIT license, see the LICENSE file.

## Packaging a repo

Packaging a repo is basically adding extra info on the repo in the gui such
as summary, description and the icon.

Since system-config-repo is invoked with a repository file, it needs to find
out the package which contains the relevant info for an actual repofile. The algorithm used is:
- Check if there is package which owns the repository file. If this package
  provides 'repo-gui', use this package.
- Otherwise, check if there is a package which requires the repository file.
  If this package provides 'repo-gui', use it.
- Otherwise, there is no package to use, fall back to default values for
  summary, description and icon.

Some points while packaging a repo.
- Although the repository normally is named after after repository file,
  this is not required. See e. g., the postgres-sql example.
- In many cases the repository file could be installed by another package.
  Normally, it's not possible to depend on it  since it isn't in commonly
  used repositories. If so, put the repository file (and possibly also the
  signing key) in a subpackage and let the main package require the
  repository file. See e. g., the adobe example.
- Using icons is legally complicated, they re often trademarked. See
  https://lists.fedoraproject.org/pipermail/legal/2011-April/thread.html#1604
- Using appdata is basically about providing info through gnome-software and
  also about localizing summary and description. See
  http://people.freedesktop.org/~hughsient/appdata/

## TODO

Lots...
 - Dozens of bugs...
- More examples.
