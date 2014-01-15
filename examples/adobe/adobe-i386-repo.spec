%define         reponame %(b=%{name}; echo ${b%%-repo})

Name:           adobe-i386-linux-repo
Version:        0
Release:        1%{?dist}
Summary:        Adobe 3rd-party repository package.

License:        Public Domain
URL:            https://adobe.com
Group:          Development/System
Source0:        adobe-i386-linux.repo
Source1:        adobe-i386-linux-repo.appdata.xml
Source2:        adobe-i386-linux-repo.desktop
Source3:        RPM-GPG-KEY-adobe-linux
Source4:        README
BuildArch:      noarch

BuildRequires:  desktop-file-utils

Requires:       fedora-release
Requires:       hicolor-icon-theme
Requires:       system-config-repo
Requires:       /etc/yum.repos.d/adobe-linux-i386.repo


%description
Provides the dropbox 3rd-party repository. Using this it's possible to
install the dropbox application which gives access to a cloud-based location
which can be accessed from a multitude of devices.

The package uses system-config-repo to provide a graphical interface to the
file in /etc/yum.repos.d. Using the GUI user can inspect and modif whether
the repository is enabled and/or signed. It's also possible to see the
underlyng file.

%package base
Summary:       The files corresponding to the yum package from Adobe
Conflicts:     adobe-release-i386

%description base
The repository and pki file distributed by adobe at
http://linuxdownload.adobe.com/adobe-release/adobe-release-i386-1.0-1.noarch.rpm


%prep
%setup -cT
cp %{SOURCE0} %{reponame}.repo
cp %{SOURCE1} %{name}.appdata.xml
cp %{SOURCE2} %{name}.desktop
cp %{SOURCE3} RPM-GPG-KEY-adobe-linux
cp %{SOURCE4} README


%build


%install
install -pDm 644 %{reponame}.repo \
    %{buildroot}/etc/yum.repos.d/%{reponame}.repo
install -pDm 644 %{name}.appdata.xml \
    %{buildroot}/usr/share/appdata/%{name}.appdata.xml
install -pDm 644 RPM-GPG-KEY-adobe-linux \
    %{buildroot}/etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux
install -pDm 644 %{name}.desktop \
    %{buildroot}/usr/share/applications/%{name}.desktop
desktop-file-validate %{buildroot}/usr/share/applications/%{name}.desktop


%files
%doc README
#/usr/share/system-config-repo/repos/%{reponame}
/usr/share/appdata/%{name}.appdata.xml
/usr/share/applications/%{name}.desktop

%files base
/etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux
/etc/yum.repos.d/%{reponame}.repo



%changelog
* Wed Nov 27 2013 Alec Leamas <leamas.alec@gmail.com> - 0-1.1478565
- Initial release.
