#
# Conditional build:
%bcond_without	apidocs		# API documentation

Summary:	Xt/Motif GUI component toolkit library for Coin
Summary(pl.UTF-8):	Biblioteka komponentu graficznego interfejsu Xt/Motif dla biblioteki Coin
Name:		SoXt
Version:	1.4.1
Release:	1
License:	BSD
Group:		X11/Libraries
#Source0Download: https://github.com/coin3d/soxt/releases
Source0:	https://github.com/coin3d/soxt/releases/download/v%{version}/soxt-%{version}-src.tar.gz
# Source0-md5:	6856751e41cab5e13621ab1f3b5e8542
Patch0:		%{name}-pc.patch
URL:		https://github.com/coin3d/soxt
BuildRequires:	Coin-devel >= 4.0.0
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	cmake >= 3.0
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	motif-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SoXt is a Xt/Motif GUI component toolkit library for Coin. It is also
compatible with SGI and TGS Open Inventor, and the API is based on the
API of the InventorXt GUI component toolkit.

%description -l pl.UTF-8
SoXt to biblioteka toolkitu komponentu graficznego interfejsu
użytkownika (GUI) Xt/Motif dla biblioteki Coin. Jest zgodna także z
biblioteką SGI i TGS Open Inventor, a API jest oparte na API toolkitu
komponentu graficznego interfejsu użytkownika InventorXt.

%package devel
Summary:	Header files for SoXt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SoXt
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Coin-devel >= 4.0.0
Requires:	OpenGL-GLX-devel
Requires:	motif-devel
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXt-devel

%description devel
Header files for SoXt library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SoXt.

%package apidocs
Summary:	API documentation for SoXt library
Summary(pl.UTF-8):	Dokumentacja API biblioteki SoXt
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for SoXt library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki SoXt.

%prep
%setup -q -n soxt
%patch0 -p1

%build
install -d builddir
cd builddir
%cmake .. \
%if %{with apidocs}
	-DSOXT_BUILD_DOCUMENTATION=ON \
	-DSOXT_BUILD_DOC_MAN=ON
%endif

%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with apidocs}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/html
# to common names etc.
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{_*_,components,devices,misc,viewers}.3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS.txt COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libSoXt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSoXt.so.20
%{_datadir}/SoXt

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libSoXt.so
%{_includedir}/Inventor/Xt
%{_pkgconfigdir}/SoXt.pc
%{_libdir}/cmake/SoXt-%{version}
%if %{with apidocs}
%{_mandir}/man3/SoXt*.3*
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc builddir/html/*.{css,html,js,png}
%endif
