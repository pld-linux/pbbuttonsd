#
# Conditional build
%bcond_without	alsa	# without ALSA mixer support
%bcond_without	oss	# without OSS mixer support
#
Summary:	Daemon that handle the special hotkeys of an Apple iBook, Powerbook or TiBook
Summary(pl.UTF-8):	Demon obsługujący klawisze specjalne w Apple iBook, Powerbook i TiBook
Name:		pbbuttonsd
Version:	0.8.1a
Release:	6
License:	GPL v2+
Group:		Daemons
Source0:	http://downloads.sourceforge.net/pbbuttons/%{name}-%{version}.tar.gz
# Source0-md5:	0a6a756d4b4f3ae90c906ed305725100
Source1:	%{name}.init
Source2:	%{name}.sysconf
Patch0:		%{name}-c++.patch
Patch1:		%{name}-ac.patch
Patch2:		%{name}-libsmbios.patch
Patch3:		%{name}-format.patch
URL:		http://pbbuttons.berlios.de/
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 1.0.0}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
%ifarch %{ix86}
BuildRequires:	libsmbios-devel >= 2.2.7
BuildRequires:	pciutils-devel
BuildRequires:	zlib-devel
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	glib2 >= 1:2.6.0
Requires:	rc-scripts
Obsoletes:	pmud
ExclusiveArch:	%{ix86} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
With the pbbuttonsd daemon, the keys for the display brightness, the
volume of speaker and headphone, the mute key and the eject key will
do their job as expected. The daemon also do some power management
tasks including low battery warnings, dimming the display if idle,
sleep on command, etc.

%description -l pl.UTF-8
Pakiet zawiera demona pbbuttonsd, obsługującego klawisze specjalne
(jasność wyświetlania, głośność, wyciszanie, wyjmowanie CD).
Jednocześnie obsługuje niektóre funkcje zarządzania energią, m.in.
ostrzega o wyładowaniu baterii, wygasza nieużywany wyświetlacz,
umożliwia usypianie komputera na komendę.

%package lib
Summary:	Static libpbb.a library
Summary(pl.UTF-8):	Statyczna biblioteka libpbb.a
Group:		Development/Libraries
# it doesn't require base

%description lib
This library is part of the daemon package pbbuttonsd and is available
as static library only.

%description lib -l pl.UTF-8
Ta biblioteka jest częścią pakietu pbbuttonsd i jest dostępna tylko w
wersji statycznej.

%package -n pbbcmd
Summary:	Command line tool to communicate with pbbuttonsd
Summary(pl.UTF-8):	Działające z linii poleceń narzędzie do komunikowania z pbbuttonsd
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description -n pbbcmd
pbbcmd is a tool to communicate with pbbuttonsd. It is possible to
send single commands to the daemon or ask it for certain information.

%description -n pbbcmd -l pl.UTF-8
pbbcmd to narzędzie do komunikowania z pbbuttonsd. Umożliwia wysyłanie
pojedynczych poleceń do demona lub żądanie określonych informacji.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{!?with_alsa:echo "AC_DEFUN([AM_PATH_ALSA],[])" >> acinclude.m4}
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--without-pmud \
	--with-ibam \
	--with-alsa%{!?with_alsa:=no} \
	--with-oss%{!?with_oss:=no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sbindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_bindir}/pbbuttonsd $RPM_BUILD_ROOT%{_sbindir}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pbbcmd $RPM_BUILD_ROOT%{_sbindir}

cp -p scripts/README README-power
cp -p scripts/scripts.d/skeleton scripts-skeleton

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pbbuttonsd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pbbuttonsd

for script in $RPM_BUILD_ROOT/etc/power/scripts.d/*; do
	%{__sed} -i 's#^. pmcs-config#. /etc/power/pmcs-config#' $script
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
		: Not all run-parts script invocations are converted to PLD standard
		exit 1
	fi
done

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pbbuttonsd
%service pbbuttonsd restart "pbbuttonsd daemon"

%preun
if [ "$1" = "0" ]; then
	%service pbbuttonsd stop
	/sbin/chkconfig --del pbbuttonsd
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README TODO README-power scripts-skeleton
%attr(755,root,root) %{_sbindir}/pbbuttonsd
%attr(754,root,root) /etc/rc.d/init.d/pbbuttonsd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pbbuttonsd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pbbuttonsd.cnf
%dir %{_localstatedir}/lib/ibam
%dir %{_localstatedir}/lib/pbbuttons

%dir /etc/power
%attr(754,root,root) /etc/power/pmcs-apmd
%attr(754,root,root) /etc/power/pmcs-pbbuttonsd
%attr(754,root,root) /etc/power/pmcs-pmud
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/power/pmcs-config

%dir /etc/power/scripts.d
%exclude /etc/power/scripts.d/skeleton
%attr(754,root,root) /etc/power/scripts.d/*
/etc/power/event.d

%{_mandir}/man1/pbbcmd.1*
%{_mandir}/man1/pbbuttonsd.1*
%{_mandir}/man5/pbbuttonsd.cnf.5*

%files lib
%defattr(644,root,root,755)
%{_libdir}/libpbb.a
%{_includedir}/pbb*.h

%files -n pbbcmd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pbbcmd
