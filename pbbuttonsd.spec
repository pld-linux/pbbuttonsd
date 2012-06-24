
%{!?min_kernel:%define          min_kernel      2.4.18}

Summary:	Daemon that handle the special hotkeys of an Apple iBook, Powerbook or TiBook
Summary(pl):	Demon obs�uguj�cy klawisze specjalne w Apple iBook, Powerbook i TiBook
Name:		pbbuttonsd
Version:	0.5.2
Release:	1
License:	GPL
Group:		Daemons
# http://www.cymes.de/members/joker/projects/pbbuttons/tar/%{name}-%{version}.tar.gz
Source0:	pbbuttonsd-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconf
URL:		http://www.cymes.de/members/joker/projects/pbbuttons/pbbuttons.html
BuildRequires:	autoconf
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	ppc

%define		_sysconfdir	/etc

%description
With the pbbuttonsd daemon, the keys for the display brightness, the
volume of speaker and headphone, the mute key and the eject key will
do their job as expected. The daemon also do some power management
tasks including low battery warnings, dimming the display if idle,
sleep on command, etc.

%description -l pl
Pakiet zawiera demona pbbuttonsd, obs�uguj�cego klawisze specjalne
(jasno�� wy�wietlania, g�o�no��, wyciszanie, wyjmowanie CD).
Jednocze�nie ob�uguje niekt�re funkcje zarz�dzania energi�, m.in.
ostrzega o wy�adowaniu baterii, wygasza nieu�ywany wy�wietlacz,
umo�liwia usypianie komputera na komend�.

%package -n pbbuttonsd-lib
Summary:        static library libpbb.a
Summary(pl):    statyczna bibiloteka libpbb.a
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description -n pbbuttonsd-lib
This library is part of the daemon package pbbuttonsd and is 
available as static library only

%description -n pbbuttonsd-lib -l pl
Ta biblioteka jest czescia pakietu pbbuttonsd i jest dostepna tylko 
w wersji statycznej.

%prep
%setup -q

%build
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_sbindir}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig},%{_mandir}/{man1,man5}}
install -d $RPM_BUILD_ROOT/%{_libdir}

install src/pbbuttonsd $RPM_BUILD_ROOT/%{_sbindir}
install pbbuttonsd.conf $RPM_BUILD_ROOT/%{_sysconfdir}
install pbbuttonsd.1 $RPM_BUILD_ROOT/%{_mandir}/man1
install pbbuttonsd.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5
install libpbbipc/libpbb.a $RPM_BUILD_ROOT/%{_libdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pbbuttonsd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pbbuttonsd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pbbuttonsd
if [ -f /var/lock/subsys/pbbuttonsd ]; then
	/etc/rc.d/init.d/pbbuttonsd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/pbbuttonsd start\" to start pbbuttonsd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/pbbuttonsd ]; then
		/etc/rc.d/init.d/pbbuttonsd stop >&2
	fi
	/sbin/chkconfig --del pbbuttonsd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog INSTALL NEWS README TODO 
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/pbbuttonsd.conf
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/pbbuttonsd
%attr(640,root,root) %config %verify(not size md5 mtime) /etc/sysconfig/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n pbbuttonsd-lib
%defattr(644,root,root,755)
%{_libdir}/*
 
