%define         reponame %(b=%{name}; echo ${b%%-repo})
%define         hicolor_dir  %{buildroot}/usr/share/icons/hicolor

Name:           virtualbox-repo
Version:        0
Release:        1%{?dist}
Summary:        Virtual Box 3rd-party repository package.

                # Icon from iconarchive.com
License:        Public Domain
URL:            https://virtualbox.com
Group:          Development/System
Source0:        virtualbox.repo
Source1:        virtualbox-repo.appdata.xml
Source2:        virtualbox-repo.desktop
Source3:        icon.png
Source4:        README
Source5:        icons.tar
BuildArch:      noarch

BuildRequires:  desktop-file-utils

Requires:       fedora-release
Requires:       hicolor-icon-theme
Requires:       system-config-repo


%description
Provides the virtualbox 3rd-party repository. Using this it's possible to
install the virtualbox virtual hosting software.

The package uses system-config-repo to provide a graphical interface to the
file in /etc/yum.repos.d. Using the GUI user can inspect and modif whether
the repository is enabled and/or signed. It's also possible to see the
underlyng file.


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
for size in 32 48 64 128; do
    install -pDm 644 icons/virtualbox-repo-$size.png \
	%{hicolor_dir}/${size}x${size}/apps//virtualbox-repo.png;
done
install -pDm 644 %{name}.desktop \
    %{buildroot}/usr/share/applications/%{name}.desktop
desktop-file-validate %{buildroot}/usr/share/applications/%{name}.desktop


%files
%doc README
/usr/share/system-config-repo/repos/%{reponame}
/usr/share/appdata/%{name}.appdata.xml
/etc/yum.repos.d/%{reponame}.repo
/usr/share/applications/%{name}.desktop
/usr/share/icons/hicolor/*/apps/virtualbox-repo.png


%changelog
* Wed Nov 27 2013 Alec Leamas <leamas.alec@gmail.com> - 0-1.1478565
- Initial release.
