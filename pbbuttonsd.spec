
%{!?min_kernel:%define          min_kernel      2.4.18}

Summary:	Daemon that handle the special hotkeys of an Apple iBook, Powerbook or TiBook
Summary(pl):	Demon obs³uguj±cy klawisze specjalne w Apple iBook, Powerbook i TiBook
Name:		pbbuttonsd
Version:	0.6.7
Release:	2
License:	GPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/pbbuttons/%{name}-%{version}.tar.gz
# Source0-md5:	dd578afa5252206db0bdd3054064e9a9
Source1:	%{name}.init
Source2:	%{name}.sysconf
Source3:	%{name}-initreq.h
Patch0:		%{name}-c++.patch
URL:		http://www.cymes.de/members/joker/projects/pbbuttons/pbbuttons.html
BuildRequires:	autoconf
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Obsoletes:	pmud
ExclusiveArch:	%{ix86} ppc
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
Jednocze¶nie obs³uguje niektóre funkcje zarz±dzania energi±, m.in.
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
Requires:	%{name} = %{version}-%{release}

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
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sbindir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_bindir}/pbbuttonsd $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_bindir}/pbbcmd $RPM_BUILD_ROOT%{_sbindir}

cp scripts/README README-power
cp scripts/scripts.d/skeleton scripts-skeleton

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pbbuttonsd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pbbuttonsd

for script in $RPM_BUILD_ROOT/etc/power/scripts.d/*; do
    sed -i 's#^. pmcs-config#. /etc/power/pmcs-config#' $script
done

#
# Fix for pld run-parts script.
#

# convert run-parts invocation so it does not contain
# "--arg" and directory is given as first argument to run-parts script
find $RPM_BUILD_ROOT/etc/power -type f -exec sed -i \
    's#run-parts --arg="\([^"]\+\)" --arg="\([^"]\+\)" --arg="\([^"]\+\)" \(.\+\)#run-parts \4 "\1" "\2" "\3"#' \
    {} \;

find $RPM_BUILD_ROOT/etc/power -type f -exec sed -i \
    's#run-parts --arg=\([^ ]\+\) --arg=\([^ ]\+\) \(.\+\)#run-parts \3 "\1" "\2"#' \
    {} \;

# check if all run-parts invoked with "--arg" are converted
for f in $(find $RPM_BUILD_ROOT/etc/power -type f); do
    if grep -q -- --arg $f; then
        echo Not all run-parts script invocations are converted to PLD standard
        exit 1
    fi
done

%find_lang %{name}

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO README-power scripts-skeleton
%attr(755,root,root) %{_sbindir}/pbbuttonsd
%attr(754,root,root) /etc/rc.d/init.d/pbbuttonsd
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) /etc/sysconfig/*
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/pbbuttonsd.conf

%dir /etc/power

%attr(750,root,root) /etc/power/pmcs-pbbuttonsd
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) /etc/power/pmcs-config

%dir /etc/power/scripts.d
%exclude /etc/power/scripts.d/skeleton
%attr(750,root,root) /etc/power/scripts.d/*
/etc/power/event.d
/etc/power/pmcs-apmd
/etc/power/pmcs-pmud

%{_mandir}/man1/*
%{_mandir}/man5/*

%files lib
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_includedir}/*

%files -n pbbcmd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pbbcmd
