Summary:	Daemon that handle the special hotkeys of an Apple iBook, Powerbook or TiBook
Summary(pl):	Demon obs³uguj±cy klawisze specjalne w Apple iBook, Powerbook i TiBook
Name:		pbbuttonsd
Version:	0.4.8
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://www.cymes.de/members/joker/projects/pbbuttons/tar/%{name}-%{version}.tar.gz
URL:		http://www.cymes.de/members/joker/projects/pbbuttons/pbbuttonsd.html
BuildRequires:	autoconf
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/pbbuttons
%define		_bindir		%{_sbindir}

%description
With the pbbuttonsd daemon, the keys for the display brightness, the
volume of speaker and headphone, the mute key and the eject key will
do their job as expected. The daemon also do some power management
tasks including low battery warnings, dimming the display if idle,
sleep on command, etc.

%description -l pl
Pakiet zawiera demona pbbuttonsd, obs³uguj±cego klawisze specjalne
(jasno¶æ wy¶wietlania, g³o¶no¶æ, wyciszanie, wyjmowanie CD).
Jednocze¶nie ob³uguje niektóre funkcje zarz±dzania energi±, m.in.
ostrzega o wy³adowaniu baterii, wygasza nieu¿ywany wy¶wietlacz,
umo¿liwia usypianie komputera na komendê.

%prep
%setup -q

%build
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig},%{_mandir}/man8}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

#gzip -9nf NEWS TODO 

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
%doc conf/*.gz *.gz
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/pbbuttonsd
%attr(640,root,root) %config %verify(not size md5 mtime) /etc/sysconfig/*
%{_mandir}/man8/*
