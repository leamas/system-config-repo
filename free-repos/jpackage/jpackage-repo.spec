%define         reponame %(b=%{name}; echo ${b%%-repo})

Name:           jpackage-repo
Version:        0
Release:        1%{?dist}
Summary:        jpackage repo provides a large set of java packages.

License:        Public Domain
URL:            http://www.jpackage.org/yum.php
Group:          Development/System
Source0:        jpackage.repo
Source1:        jpackage-repo.appdata.xml
Source2:        jpackage-repo.desktop
BuildArch:      noarch

Provides:       repo-gui = 1.0

BuildRequires:  desktop-file-utils

Requires:       fedora-release
Requires:       hicolor-icon-theme
Requires:       system-config-repo


%description
The JPackage Project has two primary goals:

 - To provide a coherent set of Java software packages for Linux,
   satisfying all quality requirements of other applications.
 - To establish an efficient and robust policy for Java software
   packaging and installation.

We focus on free and open source software whenever possible. For convenience,
we also provide non-free packages without the restricted source code.

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


%changelog
* Wed Nov 27 2013 Alec Leamas <leamas.alec@gmail.com> - 0-1.1478565
- Initial release.
