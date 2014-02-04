%define         reponame %(b=%{name}; echo ${b%%-repo})

Name:           dropbox-repo
Version:        0
Release:        3%{?dist}
Summary:        3rd-party repo package for Dropbox client

License:        Public Domain
URL:            http://github.com/leamas/system-config-repo
Source0:        dropbox.repo
Source1:        dropbox-repo.appdata.xml
Source2:        dropbox-repo.desktop
Source3:        icon.png
Source4:        README
Source5:        branding-permission.txt
BuildArch:      noarch

Provides:       repo-gui = 1.0

BuildRequires:  desktop-file-utils
BuildRequires:  appdata-tools

Requires:       system-config-repo
Requires:       /etc/yum.repos.d/dropbox.repo


%description
This repo package makes it possible to easily download and install the
newest Dropbox desktop client (linux.dropbox.com/).

The package uses system-config-repo to provide a graphical interface to the
file in /etc/yum.repos.d. Using the GUI user can inspect and modify whether
the repository is enabled and/or signed. It's also possible to view the
underlying file.


%package config
Summary:   The basic repository file
Requires:  %{name} = %{version}-%{release}

%description config
The main repository file, in some cases provided by other packages.


%prep
%setup -cT
cp %{SOURCE4} README
cp %{SOURCE5} branding-permission.txt


%build


%install
install -pDm 644 %{SOURCE0} \
    %{buildroot}/etc/yum.repos.d/%{reponame}.repo
install -pDm 644 %{SOURCE1} \
    %{buildroot}/usr/share/appdata/%{name}.appdata.xml
install -pDm 644 %{SOURCE3} \
    %{buildroot}/usr/share/system-config-repo/repos/%{reponame}/icon.png
install -pDm 644 %{SOURCE2} \
    %{buildroot}/usr/share/applications/%{name}.desktop
desktop-file-validate %{buildroot}/usr/share/applications/%{name}.desktop


%check
ping -qc 1 www.redhat.com >& /dev/null || opts='--nonet'
appdata-validate $opts %{buildroot}/usr/share/appdata/%{name}.appdata.xml


%files
%doc README branding-permission.txt
/usr/share/system-config-repo/repos/%{reponame}
/usr/share/appdata/%{name}.appdata.xml
/usr/share/applications/%{name}.desktop

%files config
%config(noreplace) /etc/yum.repos.d/%{reponame}.repo


%changelog
* Tue Feb 04 2014 Alec Leamas <leamas.alec@gmail.com> - 0-3
- Adapt to new scheme where repo file is manually activated.
- Use NotShowIn=Mate to avoid collision with existing package.
- Use includepkgs in repo file.
- Add DISCLAIMER to repository file.
- Requires yet not available update of system-config-repo.

* Mon Jan 27 2014 Alec Leamas <leamas.alec@gmail.com> - 0-2
- Update &&check using --nonet

* Sun Jan 26 2014 Alec Leamas <leamas.alec@gmail.com> - 0-2
- Drop R: hicolor-icon-theme, R: fedora-release
- Add branding permission document.
- Drop Group:
- Set Url: to packaging project rather than dropbox.
- Split out config package to handle e. g., file provided by caja-dropbox
- Skip redundant copy in %%prep
- Update appdata, add %%check for it.

* Wed Nov 27 2013 Alec Leamas <leamas.alec@gmail.com> - 0-1.1478565
- Initial release.
