%define         reponame %(b=%{name}; echo ${b%%-repo})

Name:           google-chrome-repo
Version:        0
Release:        1%{?dist}
Summary:        Google 3rd-party repository package.

License:        Public Domain
URL:            http://www.google.com/linuxrepositories/
Group:          Development/System
Source0:        google-chrome.repo
Source1:        google-chrome-repo.appdata.xml
Source2:        google-chrome-repo.desktop
BuildArch:      noarch

Provides:       repo-gui = 1.0

BuildRequires:  desktop-file-utils

Requires:       fedora-release
Requires:       hicolor-icon-theme
Requires:       system-config-repo


%description
Provides the Google google-chrome  3rd-party repository. Using this it's
possible to install the google-chrome browser, the branded Google product.
Note the difference between google-chrome and the open-source chromium
browser.

The package uses system-config-repo to provide a graphical interface to the
file in /etc/yum.repos.d. Using the GUI user can inspect and modify whether
the repository is enabled, signed, etc. It's also possible to see the
underlyng file.


%prep
%setup -cT
cp %{SOURCE0} %{reponame}.repo
cp %{SOURCE1} %{name}.appdata.xml
cp %{SOURCE2} %{name}.desktop


%build


%install
install -pDm 644 %{reponame}.repo \
    %{buildroot}/etc/yum.repos.d/%{reponame}.repo
install -pDm 644 %{name}.appdata.xml \
    %{buildroot}/usr/share/appdata/%{name}.appdata.xml
install -pDm 644 %{name}.desktop \
    %{buildroot}/usr/share/applications/%{name}.desktop
desktop-file-validate %{buildroot}/usr/share/applications/%{name}.desktop


%files
/etc/yum.repos.d/%{reponame}.repo
/usr/share/appdata/%{name}.appdata.xml
/usr/share/applications/%{name}.desktop
#/usr/share/system-config-repo/repos/%{reponame}




%changelog
* Thu Jan 23 2014 Alec Leamas <leamas.alec@gmail.com> - 0-1
- Initial release.
