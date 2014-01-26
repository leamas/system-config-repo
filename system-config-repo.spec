%global __python    %{__python3}

%global commit      9c864dc37bf0e247a949de4d9d2999b0cd991297
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitdate     20140117

Name:           system-config-repo
Version:        0
Release:        2.%{gitdate}git%{shortcommit}%{?dist}
Summary:        Administrate a single yum repository file

License:        MIT
URL:            https://github.com/leamas/system-config-repo
Group:          Development/System
Source0:        %{url}/archive/%{commit}/%{name}-0-%{shortcommit}.tar.gz
                # Created by tools/make_rpm, left in dist directory.
Source1:        version
BuildArch:      noarch

Buildrequires:  python3-devel
BuildRequires:  desktop-file-utils
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       python(abi) = %{python3_version}
Requires:       python3-gobject
Requires:       redhat-lsb-core
Requires:       sudo


%description
system-config-repo provides a graphical interface to a single yum repository
file in /etc/yum.repos.d. Using the GUI user can inspect and modify whether
the repository is enabled and/or signed. It's also possible to see the
underlying file.

Application is primarily intended as a GUI for packaged 3rd-party
repositories but is designed to work in a consistent way for any
repository file.


%prep
%setup -qn %{name}-%{commit}
cp %{SOURCE1} version


%build


%install
make DESTDIR=%{buildroot} install
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/system-config-repo.desktop
for size in 256 128 64 48 32; do
    install -pDm 644 icons/scr-repo-$size.png \
        %{buildroot}/usr/share/icons/hicolor/${size}x${size}/apps/scr-repo.png
done


%post
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :


%files
%doc README.md LICENSE
%{_bindir}/system-config-repo
%{_datadir}/system-config-repo
%{_datadir}/mime/packages/x-yum-repositories.xml
%{_datadir}/applications/system-config-repo.desktop
%{_datadir}/icons/hicolor/*/apps/scr-repo.png
%{_mandir}/man1/system-config-repo*
%attr(440,-,-) %config(noreplace) /etc/sudoers.d/system-config-repo


%changelog
* Sat Jan 25 2014 Alec Leamas <leamas.alec@gmail.com> - 0-2.20140117gitc112d69
- Adding missing R: redhat-lsb-core (bz #1057824).

* Mon Jan 20 2014 Alec Leamas <leamas.alec@gmail.com> - 0-1.20140117gitc112d69
- Initial release.
