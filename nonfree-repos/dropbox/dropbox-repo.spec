%define         reponame %(b=%{name}; echo ${b%%-repo})

Name:           dropbox-repo
Version:        0
Release:        1%{?dist}
Summary:        3rd-party repo package for Dropbox client

                # Icon from iconarchive.com
License:        Public Domain
URL:            https://dropbox.com
Group:          Development/System
Source0:        dropbox.repo
Source1:        dropbox-repo.appdata.xml
Source2:        dropbox-repo.desktop
Source3:        icon.png
Source4:        README
BuildArch:      noarch

Provides:       repo-gui = 1.0

BuildRequires:  desktop-file-utils

Requires:       fedora-release
Requires:       hicolor-icon-theme
Requires:       system-config-repo


%description
This repo package makes it possible to easily download and install the
newest Dropbox desktop client (linux.dropbox.com/).

The package uses system-config-repo to provide a graphical interface to the
file in /etc/yum.repos.d. Using the GUI user can inspect and modify whether
the repository is enabled and/or signed. It's also possible to view the
underlyng file.


%prep
%setup -cT
cp %{SOURCE0} %{reponame}.repo
cp %{SOURCE1} %{name}.appdata.xml
cp %{SOURCE2} %{name}.desktop
cp %{SOURCE3} icon.png
cp %{SOURCE4} README


%build


%install
install -pDm 644 %{reponame}.repo \
    %{buildroot}/etc/yum.repos.d/%{reponame}.repo
install -pDm 644 %{name}.appdata.xml \
    %{buildroot}/usr/share/appdata/%{name}.appdata.xml
install -pDm 644 icon.png \
    %{buildroot}/usr/share/system-config-repo/repos/%{reponame}/icon.png
install -pDm 644 %{name}.desktop \
    %{buildroot}/usr/share/applications/%{name}.desktop
desktop-file-validate %{buildroot}/usr/share/applications/%{name}.desktop


%files
%doc README
/usr/share/system-config-repo/repos/%{reponame}
/usr/share/appdata/%{name}.appdata.xml
/etc/yum.repos.d/%{reponame}.repo
/usr/share/applications/%{name}.desktop


%changelog
* Wed Nov 27 2013 Alec Leamas <leamas.alec@gmail.com> - 0-1.1478565
- Initial release.
