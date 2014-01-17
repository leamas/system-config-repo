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
BuildArch:      noarch

Buildrequires:  python3-devel
Requires:       hicolor-icon-theme


%description
system-config-repo provides a graphical interface to a single yum repository
file in /etc/yum.repos.d. Using the GUI user can inspect and modif whether
the repository is enabled and/or signed. It's aslo possible to see the
underlyng file.

Application is primarely intended as a GUI for packaged 3rd-party
repositories.


%prep
%setup -qn %{name}-%{commit}


%build


%install
make DESTDIR=%{buildroot} install


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
* Wed Nov 27 2013 Alec Leamas <leamas.alec@gmail.com> - 0-1.1478565
- Initial release.
