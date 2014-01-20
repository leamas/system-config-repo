%global commit 3b5da020685e25b2f97a3b2de4293afc78077139
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           system-config-repo
Version:        0
Release:        1.%{shortcommit}%{?dist}
Summary:        Administrate a single yum repository file

                # Icon from iconarchive.com
License:        MIT
URL:            https://github.com/leamas/system-config-repo
Group:          Development/System
Source0:        %{url}/archive/%{commit}/%{name}-0-%{shortcommit}.tar.gz
                # Created by tools/make_rpm, left in dist directory
Source1:        version
BuildArch:      noarch

Buildrequires:  python3-devel
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme


%description
system-config-repo provides a graphical interface to a single yum repository
file in /etc/yum.repos.d. Using the GUI user can inspect and modify whether
the repository is enabled and/or signed. It's also possible to see the
underlying file.

Application is primarely intended as a GUI for packaged 3rd-party
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
%{_mandir}/man1/system-config-repo*
%attr(440,-,-) %config(noreplace) /etc/sudoers.d/system-config-repo


%changelog
* Mon Jan 20 2014 Alec Leamas <leamas.alec@gmail.com> - 0-1.20140117gitc112d69
- Initial release.
