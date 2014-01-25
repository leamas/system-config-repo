%define         reponame %(b=%{name}; echo ${b%%-repo})
%define         hicolor_dir  %{buildroot}/usr/share/icons/hicolor

Name:           postgres-93-repo
Version:        0
Release:        1%{?dist}
Summary:        3rd-party PostgreSQL vers 9.3 repository package

                # Icon from iconarchive.com
License:        Public Domain
URL:            https://pgdg-93-fedora.com
Group:          Development/System
BuildArch:      noarch
Source0:        pgdg-93-fedora.repo
Source1:        pgdg-93-fedora-repo.appdata.xml
Source2:        pgdg-93-fedora-repo.desktop
Source3:        icon.png
Source4:        README
Source5:        icons.tar
Source6:	RPM-GPG-KEY-PGDG-93

Provides:       repo-gui = 1.0

BuildRequires:  desktop-file-utils

Requires:       fedora-release
Requires:       hicolor-icon-theme
Requires:       system-config-repo
Requires:       /etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG-93
Requires:       /etc/yum.repos.d/pgdg-93-fedora.repo

Provides:       repo-gui = 1.0


%description
Provides the pgdg-93-fedora 3rd-party repository. Using this it's possible to
install the PostgreSQL application built by the upstream project instead
of the packages built by Fedora packagers.

The package uses system-config-repo to provide a graphical interface to the
file in /etc/yum.repos.d. Using the GUI user can inspect and modify whether
the repository is enabled and/or signed. It's also possible to see the
underlying file.

%package base
Summary:   Repo file and signing key provided by upstream package

%description base
The files provided by the packaged yum repository at
http://yum.postgresql.org/howtoyum.php


%prep
%setup -cT
cp %{SOURCE0} %{reponame}.repo
cp %{SOURCE1} %{name}.appdata.xml
cp %{SOURCE2} %{name}.desktop
cp %{SOURCE3} icon.png
cp %{SOURCE4} README
tar xf %{SOURCE5}
cp %{SOURCE6} RPM-GPG-KEY-PGDG-93



%build


%install
install -pDm 644 %{reponame}.repo \
    %{buildroot}/etc/yum.repos.d/%{reponame}.repo
install -pDm 644 %{name}.appdata.xml \
    %{buildroot}/usr/share/appdata/%{name}.appdata.xml
install -pDm 644 icon.png \
    %{buildroot}/usr/share/system-config-repo/repos/%{reponame}/icon.png
install -pDm 644 RPM-GPG-KEY-PGDG-93 \
    %{buildroot}/etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG-93
install -pDm 644 %{name}.desktop \
    %{buildroot}/usr/share/applications/%{name}.desktop
desktop-file-validate %{buildroot}/usr/share/applications/%{name}.desktop

for size in 24 32 64 128; do
    install -pDm 644 icons/PostgreSQL-repo-$size.png \
	%{hicolor_dir}/${size}x${size}/apps//PostgreSQL-repo.png;
done



%files
%doc README
/usr/share/system-config-repo/repos/%{reponame}
/usr/share/appdata/%{name}.appdata.xml
/usr/share/applications/%{name}.desktop
/usr/share/icons/hicolor/*/apps/PostgreSQL-repo.png

%files base
/etc/yum.repos.d/%{reponame}.repo
/etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG-93

%changelog
* Wed Nov 27 2013 Alec Leamas <leamas.alec@gmail.com> - 0-1.1478565
- Initial release.
