%define         ver_ver     4.9.10
%define         ver_release 20020727

Summary:	Curses Development Kit
Summary(pl):	Zestaw programistyczny do Curses
Name:		cdk
Version:	%{ver_ver}_td%{ver_release}
Release:	1
License:	BSD
Group:		Libraries
URL:		http://dickey.his.com/cdk/cdk.html
Source0:	ftp://dickey.his.com/cdk/%{name}-%{ver_ver}-%{ver_release}.tgz
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5: ae2a6fea526cc1c4407e547bda537a08
Patch0:		%{name}-includes.patch
Patch1:		%{name}-man_remove_dupl.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CDK is a widget set developed on top of the basic curses library. It
contains 21 ready to use widgets. Some which are a text entry field, a
scrolling list, a selection list, a alphalist, pull-down menu, radio
list, viewer widget, dialog box, and many more.

This version of CDK is maintained by Thomas Dickey and is not the same
as that at http://www.vexus.ca/CDK.html.

%description -l pl
CDK to zestaw widgetów zbudowanych na podstawie biblioteki curses.
Zawiera 21 gotowych go u¿ycia widgetów. W¶ród nich jest pole
wprowadzania tekstu, lista przewijana, lista wyboru, lista
alfabetyczna, menu rozwijane, lista przycisków, przegl±darka, okienko
dialogowe i wiele innych.

Ta wersja CDK jest prowadzona przez Thomasa Dickeya i nie jest tym
samym, co znajduje siê pod adresem http://www.vexus.ca/CDK.html.

%package devel
Summary:	Header files and development documentation for CDK library
Summary(pl):	Pliki nag³ówkowe i dokumentacja do CDK
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	ncurses-devel

%description devel
Header files and development documentation for CDK library. This
version is maintained by Thomas Dickey and is not the same as that at
http://www.vexus.ca/CDK.html.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja programisty do biblioteki CDK. Ta
wersja jest prowadzona przez Thomasa Dickeya i nie jest tym samym, co
znajduje siê pod adresem http://www.vexus.ca/CDK.html.

%package static
Summary:	Static version of CDK library
Summary(pl):	Statyczna wersja biblioteki CDK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of CDK library. This version is maintained by Thomas
Dickey and is not the same as that at http://www.vexus.ca/CDK.html.

%description static -l pl
Statyczna wersja biblioteki CDK. Ta wersja jest prowadzona przez
Thomasa Dickeya i nie jest tym samym, co znajduje siê pod adresem
http://www.vexus.ca/CDK.html.

%prep
%setup -q -n %{name}-%{ver_ver}-%{ver_release}
%patch0 -p1
%patch1 -p1
ln -sf . include/cdk

%build
# -funsigned-char gives valid 8bit display
CFLAGS="%{rpmcflags} -funsigned-char"
CPPFLAGS="-I/usr/include/ncurses"
%configure2_13 \
	--disable-x \
	--with-ncurses
%{__make}
%{__make} cdkshlib

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} installCDKSHLibrary installCDKLibrary \
	DESTDIR="$RPM_BUILD_ROOT"

%{__make} installCDKHeaderFiles installCDKManPages \
	DESTDIR="$RPM_BUILD_ROOT"

bzcat %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT/%{_mandir}

for d in demos examples; do
   rm -f $d/Makefile.in
   mkf=$d/Makefile
   sed 's|\-I\.\..*/include |\-I%{_includedir}/cdk |' <$mkf >$mkf.fix
   mv -f $mkf.fix $mkf
done
cp -rf demos examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc CHANGES COPYING EXPANDING NOTES README TODO
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/cdk
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
