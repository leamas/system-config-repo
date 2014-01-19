%define         reponame %(b=%{name}; echo ${b%%-repo})

Name:           fedora-chromium-stable-repo
Version:        0
Release:        1%{?dist}
Summary:        Chromium stable branch builds from spot

                # Icon from iconarchive.com
License:        Public Domain
URL:            http://repos.fedorapeople.org/repos/spot/chromium-stable
Group:          Development/System
Source0:        fedora-chromium-stable.repo
Source1:        fedora-chromium-stable-repo.appdata.xml
Source2:        fedora-chromium-stable-repo.desktop
Source3:        icon.png
Source4:        README
Source5:        icons.tar
BuildArch:      noarch

Provides:       repo-gui = 1.0

BuildRequires:  desktop-file-utils

Requires:       fedora-release
Requires:       hicolor-icon-theme
Requires:       system-config-repo


%description
Provides the fedora-chromium-stable 3rd-party repository. Using this it's
possible to install chromium builds from the stable branch.

The package uses system-config-repo to provide a graphical interface to the
file in /etc/yum.repos.d. Using the GUI user can inspect and modif whether
the repository is enabled and/or signed. It's also possible to see the
underlying file.


%prep
%setup -cT
cp %{SOURCE0} %{reponame}.repo
cp %{SOURCE1} %{name}.appdata.xml
cp %{SOURCE2} %{name}.desktop
cp %{SOURCE3} icon.png
cp %{SOURCE4} README
tar xf %{SOURCE5}


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
for size in 24 32 48 64 128; do
    install -pDm 644 icons/chromium-$size.png \
	%{buildroot}/usr/share/icons/hicolor/${size}x${size}/apps/chromium.png;
done


%files
%doc README
/etc/yum.repos.d/%{reponame}.repo
/usr/share/system-config-repo/repos/%{reponame}
/usr/share/appdata/%{name}.appdata.xml
/usr/share/applications/%{name}.desktop
/usr/share/icons/hicolor/*/apps/chromium.png


%changelog
* Wed Nov 27 2013 Alec Leamas <leamas.alec@gmail.com> - 0-1.1478565
- Initial release.
