DESTDIR=
PREFIX=/usr
BINDIR=$(PREFIX)/bin
LIBEXECDIR=$(PREFIX)/libexec
DATADIR=$(PREFIX)/share
MAN1=$(DATADIR)/man/man1

all:
	echo 'Only "make install" is doing something'.

install:
	install -m 755 -d $(DESTDIR)$(DATADIR)/system-config-repo/repos
	install -m 755 -d $(DESTDIR)$(BINDIR)
	install -m 755 -d $(DESTDIR)$(MAN1)

	install -pDm 440 system-config-repo.sudo  \
	    $(DESTDIR)/etc/sudoers.d/system-config-repo
	cp -ar scripts  $(DESTDIR)$(DATADIR)/system-config-repo
	cp -r repos/Default $(DESTDIR)$(DATADIR)/system-config-repo/repos
	ln -s $(DATADIR)/system-config-repo/scripts/system-config-repo  \
            $(DESTDIR)$(BINDIR)/system-config-repo
	cp -a system-config-repo.1  $(DESTDIR)$(MAN1)
	cp -a system-config-repo.1  version $(DESTDIR)$(DATADIR)/system-config-repo


pylint:
	@PYTHONPATH=scripts python3-pylint --rcfile=pylint.conf \
            scripts/repoconf.py | tee pylint.log

pep8:
	pep8 --config pep8.conf scripts/repoconf.py | tee pep8.log

examples:  PHONY
	cd examples; \
	for dir in *; do \
	    [  $$dir = "rpms" ] && continue; \
	    cd $$dir; \
	    rpmbuild -D "_sourcedir $$PWD" -D "_rpmdir ../rpms"  \
	        --quiet -bb $$dir-*repo.spec ; \
	    cd ..; \
	done

PHONY:
