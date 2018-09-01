%define		ver_ver		5.0
%define		ver_release	20180306

Summary:	Curses Development Kit
Summary(pl.UTF-8):	Zestaw programistyczny do Curses
Name:		cdk
Version:	%{ver_ver}_td%{ver_release}
Release:	1
License:	BSD
Group:		Libraries
Source0:	ftp://ftp.invisible-island.net/cdk/%{name}-%{ver_ver}-%{ver_release}.tgz
# Source0-md5:	3b52823d8a78c6d27d4be8839edd279e
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	ae2a6fea526cc1c4407e547bda537a08
Patch0:		%{name}-ncurses.patch
Patch1:		%{name}-man.patch
URL:		http://invisible-island.net/cdk/cdk.html
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CDK is a widget set developed on top of the basic curses library. It
contains 21 ready to use widgets. Some which are a text entry field, a
scrolling list, a selection list, a alphalist, pull-down menu, radio
list, viewer widget, dialog box, and many more.

This version of CDK is maintained by Thomas Dickey and is not the same
as that at <http://www.vexus.ca/CDK.html>.

%description -l pl.UTF-8
CDK to zestaw widgetów zbudowanych na podstawie biblioteki curses.
Zawiera 21 gotowych go użycia widgetów. Wśród nich jest pole
wprowadzania tekstu, lista przewijana, lista wyboru, lista
alfabetyczna, menu rozwijane, lista przycisków, przeglądarka, okienko
dialogowe i wiele innych.

Ta wersja CDK jest prowadzona przez Thomasa Dickeya i nie jest tym
samym, co znajduje się pod adresem <http://www.vexus.ca/CDK.html>.

%package devel
Summary:	Header files and development documentation for CDK library
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do CDK
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ncurses-devel

%description devel
Header files and development documentation for CDK library. This
version is maintained by Thomas Dickey and is not the same as that at
<http://www.vexus.ca/CDK.html>.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty do biblioteki CDK. Ta
wersja jest prowadzona przez Thomasa Dickeya i nie jest tym samym, co
znajduje się pod adresem <http://www.vexus.ca/CDK.html>.

%package static
Summary:	Static version of CDK library
Summary(pl.UTF-8):	Statyczna wersja biblioteki CDK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of CDK library. This version is maintained by Thomas
Dickey and is not the same as that at <http://www.vexus.ca/CDK.html>.

%description static -l pl.UTF-8
Statyczna wersja biblioteki CDK. Ta wersja jest prowadzona przez
Thomasa Dickeya i nie jest tym samym, co znajduje się pod adresem
<http://www.vexus.ca/CDK.html>.

%prep
%setup -q -n %{name}-%{ver_ver}-%{ver_release}
%patch0 -p1
%patch1 -p1

ln -sf . include/cdk

%build
# -funsigned-char gives valid 8bit display
CFLAGS="%{rpmcflags} -funsigned-char"
CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses"
%configure2_13 \
	--disable-x \
	--with-ncurses
%{__make}
%{__make} cdkshlib

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} installCDKSHLibrary installCDKLibrary \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} installCDKHeaderFiles installCDKManPages \
	DESTDIR=$RPM_BUILD_ROOT
install include/cdk_test.h $RPM_BUILD_ROOT%{_includedir}/cdk

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}

bzcat %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

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
%doc CHANGES COPYING EXPANDING NOTES README TODO
%attr(755,root,root) %{_libdir}/libcdk.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libcdk.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cdk5-config
%attr(755,root,root) %{_libdir}/libcdk.so
%{_includedir}/cdk
%{_includedir}/cdk.h
%{_mandir}/man3/Beep.3*
%{_mandir}/man3/CDK*.3*
%{_mandir}/man3/Cdk.3*
%{_mandir}/man3/activateCDK*.3*
%{_mandir}/man3/addCDK*.3*
%{_mandir}/man3/alignxy.3*
%{_mandir}/man3/attrbox.3*
%{_mandir}/man3/baseName.3*
%{_mandir}/man3/bindCDKObject.3*
%{_mandir}/man3/boxWindow.3*
%{_mandir}/man3/cdk.3*
%{_mandir}/man3/cdk_*.3*
%{_mandir}/man3/ceilCDK.3*
%{_mandir}/man3/char2Chtype.3*
%{_mandir}/man3/char2DisplayType.3*
%{_mandir}/man3/checkCDKObjectBind.3*
%{_mandir}/man3/checkForLink.3*
%{_mandir}/man3/chlen.3*
%{_mandir}/man3/chstrncpy.3*
%{_mandir}/man3/chtype2Char.3*
%{_mandir}/man3/chtype2String.3*
%{_mandir}/man3/cleanCDK*.3*
%{_mandir}/man3/cleanCdkTitle*.3*
%{_mandir}/man3/cleanChar.3*
%{_mandir}/man3/cleanChtype.3*
%{_mandir}/man3/cmpStrChstr.3*
%{_mandir}/man3/copyChar*.3*
%{_mandir}/man3/copyChtype*.3*
%{_mandir}/man3/deactivateCDK*.3*
%{_mandir}/man3/deleteCDK*.3*
%{_mandir}/man3/deleteCursesWindow.3*
%{_mandir}/man3/deleteFileCB.3*
%{_mandir}/man3/destroyCDK*.3*
%{_mandir}/man3/dirName.3*
%{_mandir}/man3/drawCDK*.3*
%{_mandir}/man3/drawCdkTitle.3*
%{_mandir}/man3/drawLine.3*
%{_mandir}/man3/drawObjBox.3*
%{_mandir}/man3/drawShadow.3*
%{_mandir}/man3/dumpCDKSwindow*.3*
%{_mandir}/man3/endCDK.3*
%{_mandir}/man3/eraseCDK*.3*
%{_mandir}/man3/eraseCursesWindow.3*
%{_mandir}/man3/execCDKSwindow.3*
%{_mandir}/man3/exitCancelCDKScreen*.3*
%{_mandir}/man3/exitOKCDKScreen*.3*
%{_mandir}/man3/floorCDK.3*
%{_mandir}/man3/freeChar*.3*
%{_mandir}/man3/freeChtype*.3*
%{_mandir}/man3/getCDK*.3*
%{_mandir}/man3/getDirectoryContents.3*
%{_mandir}/man3/getListIndex.3*
%{_mandir}/man3/getString.3*
%{_mandir}/man3/getcCDKObject.3*
%{_mandir}/man3/getchCDKObject.3*
%{_mandir}/man3/initCDK*.3*
%{_mandir}/man3/injectCDK*.3*
%{_mandir}/man3/insertCDK*.3*
%{_mandir}/man3/intlen.3*
%{_mandir}/man3/jumpToCell.3*
%{_mandir}/man3/jumpToLineCDKSwindow.3*
%{_mandir}/man3/justifyString.3*
%{_mandir}/man3/lenCharList.3*
%{_mandir}/man3/lenChtypeList.3*
%{_mandir}/man3/loadCDKSwindowInformation.3*
%{_mandir}/man3/lowerCDKObject.3*
%{_mandir}/man3/mixCDKTemplate.3*
%{_mandir}/man3/mode2Char.3*
%{_mandir}/man3/mode2Filetype.3*
%{_mandir}/man3/moveCDK*.3*
%{_mandir}/man3/moveCursesWindow.3*
%{_mandir}/man3/moveToCDKMatrixCell.3*
%{_mandir}/man3/newCDK*.3*
%{_mandir}/man3/popupDialog.3*
%{_mandir}/man3/popupLabel*.3*
%{_mandir}/man3/positionCDK*.3*
%{_mandir}/man3/raiseCDKObject.3*
%{_mandir}/man3/readFile.3*
%{_mandir}/man3/refreshCDKScreen.3*
%{_mandir}/man3/registerCDKObject.3*
%{_mandir}/man3/removeCDKCalendarMarker.3*
%{_mandir}/man3/resetCDKScreen*.3*
%{_mandir}/man3/saveCDKSwindowInformation.3*
%{_mandir}/man3/searchList.3*
%{_mandir}/man3/selectFile.3*
%{_mandir}/man3/setCDK*.3*
%{_mandir}/man3/setCdkExitType.3*
%{_mandir}/man3/setCdkTitle.3*
%{_mandir}/man3/setWidgetDimension.3*
%{_mandir}/man3/sortList.3*
%{_mandir}/man3/splitString.3*
%{_mandir}/man3/stripWhiteSpace.3*
%{_mandir}/man3/traverseCDK*.3*
%{_mandir}/man3/trimCDKSwindow.3*
%{_mandir}/man3/unbindCDKObject.3*
%{_mandir}/man3/unmixCDKTemplate.3*
%{_mandir}/man3/unregisterCDKObject.3*
%{_mandir}/man3/validCDKObject.3*
%{_mandir}/man3/viewFile.3*
%{_mandir}/man3/viewInfo.3*
%{_mandir}/man3/waitCDKLabel.3*
%{_mandir}/man3/writeBlanks.3*
%{_mandir}/man3/writeChar*.3*
%{_mandir}/man3/writeChtype*.3*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libcdk.a
