%define         ver_ver     4.9.10
%define         ver_release 20000923

Summary:	Curses Development Kit
Name:		cdk
Version:	%{ver_ver}_td%{ver_release}
Release:	1
License:	BSD
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
URL:		http://dickey.his.com/cdk/cdk.html
Source0:	ftp://dickey.his.com/cdk/%{name}-%{ver_ver}-%{ver_release}.tgz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CDK is a widget set developed on top of the basic curses library. It
contains 21 ready to use widgets. Some which are a text entry field, a
scrolling list, a selection list, a alphalist, pull-down menu, radio
list, viewer widget, dialog box, and many more.

This version of CDK is maintained by Thomas Dickey and is not the same
as that at http://www.vexus.ca/CDK.html.

%package devel
Summary:	Header files and development documentation for CDK library
Summary(pl):	Pliki nag³ówkowe i dokumentacja do CDK
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Header files and development documentation for CDK library. This
version is maintained by Thomas Dickey and is not the same as that at
http://www.vexus.ca/CDK.html.

%package static
Summary:	Static version of CDK library
Summary(pl):	Statyczna wersja biblioteki CDK
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Static version of CDK library. This version is maintained by Thomas
Dickey and is not the same as that at http://www.vexus.ca/CDK.html.

%prep
%setup -q -n %{name}-%{ver_ver}-%{ver_release}

%build
# -funsigned-char gets valid 8bit display
CFLAGS="%{!?debug:$RPM_OPT_FLAGS}%{?debug:-O -g}" -funsigned-char"; 
%configure \
	--disable-x \
	--with-ncurses
%{__make}
%{__make} cdkshlib

%install
rm -rf $RPM_BUILD_ROOT

%{__make} installCDKSHLibrary installCDKLibrary \
	DESTDIR="$RPM_BUILD_ROOT"

%{__make} installCDKHeaderFiles installCDKManPages \
	DESTDIR="$RPM_BUILD_ROOT"

gzip -9nf BUGS CHANGES EXPANDING NOTES README TODO

for d in demos examples; do 
   rm -f $d/Makefile.in
   mkf=$d/Makefile
   sed 's|\-I%{_prefix}/X11R6/include|\-I%{_includedir}/cdk/|' <$mkf >$mkf.fix
   mv -f $mkf.fix $mkf
done

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc *gz examples demos
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
