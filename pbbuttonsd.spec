
%{!?min_kernel:%define          min_kernel      2.4.18}

Summary:	Daemon that handle the special hotkeys of an Apple iBook, Powerbook or TiBook
Summary(pl):	Demon obs³uguj±cy klawisze specjalne w Apple iBook, Powerbook i TiBook
Name:		pbbuttonsd
Version:	0.5.6
Release:	2
License:	GPL
Group:		Daemons
Source0:	http://www.cymes.de/members/joker/projects/pbbuttons/tar/%{name}-%{version}.tar.gz
# Source0-md5:	39e11699dfaa666ca3639184670bba22
Source1:	%{name}.init
Source2:	%{name}.sysconf
Source3:	%{name}-initreq.h
Patch0:		%{name}-c++.patch
URL:		http://www.cymes.de/members/joker/projects/pbbuttons/pbbuttons.html
BuildRequires:	autoconf
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Obsoletes:	pmud
ExclusiveArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package lib
Summary:	Static libpbb.a library
Summary(pl):	Statyczna biblioteka libpbb.a
Group:		Development/Libraries
# it doesn't require base

%description lib
This library is part of the daemon package pbbuttonsd and is
available as static library only.

%description lib -l pl
Ta biblioteka jest czê¶ci± pakietu pbbuttonsd i jest dostêpna tylko
w wersji statycznej.

%package -n pbbcmd 
Summary:	Command line tool to communicate with pbbuttonsd
Summary(pl):	Dzia³aj±ce z linii poleceñ narzêdzie do komunikowania z pbbuttonsd
Group:		Deamons
BuildRequires:	autoconf
Requires:	pbbuttonsd

%description -n pbbcmd
pbbcmd is a tool to communicate with pbbuttonsd. It is possible to
send single commands to the daemon or ask it for certain information.

%description -n pbbcmd -l pl
pbbcmd to narzêdzie do komunikowania z pbbuttonsd. Umo¿liwia wysy³anie
pojedynczych poleceñ do demona lub ¿±danie okre¶lonych informacji.

%prep
%setup -q
%patch0 -p1

cp %{SOURCE3} initreq.h

%build
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig},%{_mandir}/{man1,man5}}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}

install src/pbbuttonsd $RPM_BUILD_ROOT%{_sbindir}
install pbbcmd/pbbcmd $RPM_BUILD_ROOT%{_sbindir}
install pbbuttonsd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install pbbuttonsd.1 $RPM_BUILD_ROOT%{_mandir}/man1
install pbbuttonsd.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
install libpbbipc/libpbb.a $RPM_BUILD_ROOT%{_libdir}
install libpbbipc/pbb.h $RPM_BUILD_ROOT%{_includedir}
install libpbbipc/pbberrno.h $RPM_BUILD_ROOT%{_includedir}
install libpbbipc/pbbipc.h $RPM_BUILD_ROOT%{_includedir}
install libpbbipc/pbbmisc.h $RPM_BUILD_ROOT%{_includedir}
install libpbbipc/pbbtaglist.h $RPM_BUILD_ROOT%{_includedir}
install libpbbipc/pbbtags.h $RPM_BUILD_ROOT%{_includedir}

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
%attr(755,root,root) %{_sbindir}/pbbuttonsd
%attr(754,root,root) /etc/rc.d/init.d/pbbuttonsd
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) /etc/sysconfig/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%files lib
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_includedir}/*

%files -n pbbcmd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pbbcmd
