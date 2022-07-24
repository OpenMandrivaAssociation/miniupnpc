%define major 17
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %name
%define _disable_lto 1

Summary:	Library and tool to control NAT in UPnP-enabled routers
Name:		miniupnpc
Version:	2.2.3
Release:	1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://miniupnp.free.fr/
Source:		http://miniupnp.free.fr/files/%{name}-%{version}.tar.gz
# Do not create libminiupnpc.so.1.5 and libminiupnpc.so.8 linking to it
#Patch1:		%{name}-version.patch
#Patch2:		miniupnpc-2.1-upstream-fix.patch
Source1:	USAGE
BuildRequires:	cmake
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3egg(setuptools)

%description
miniupnpc is an implementation of a UPnP client library, enabling
applications to access the services provided by an UPnP "Internet
Gateway Device" present on the network. In UPnP terminology, it is
a UPnP Control Point.

%package -n %{libname}
Summary:	Library and tool to control NAT in UPnP-enabled routers
Group:		System/Libraries

%description -n %{libname}
miniupnpc is an implementation of a UPnP client library, enabling
applications to access the services provided by an UPnP "Internet
Gateway Device" present on the network. In UPnP terminology, it is
a UPnP Control Point.

%package -n %{develname}
Summary:	Header files, libraries and development documentation for miniupnpc
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname} 
This package contains the header files and development documentation for
miniupnpc. If you like to develop programs using miniupnpc, you will need
to install miniupnpc-devel.

%package -n python-%{name}
Summary:	Python interface to %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python-%{name}
This package contains python interfaces to %{name}.

%prep
%setup -q
%autopatch -p1
cp %{SOURCE1} .

sed -i "s|\(python setup.py install\)$|\1 --root=\$(DESTDIR)/|" Makefile

# Changelog says added -ansi without reason, but that
# breaks C files (python module) using C++ comments
sed -i 's/\(CFLAGS += -ansi\)/#\1/' Makefile

%build
#export CC=%{__cc}
%cmake -DUPNPC_BUILD_STATIC=OFF -DUPNPC_BUILD_TESTS=ON

%make_build

### build example client
%make_build upnpc-shared all

### build python3 bindings
%py_build

%install
#export CC=%{__cc}
%make_install -C build

%py_install

# install manpage and binary for example client using libminiupnpc
install -D -m 644 man3/miniupnpc.3 %{buildroot}%{_mandir}/man3/miniupnpc.3
install -D -m 0755 upnpc-shared %{buildroot}%{_bindir}/upnpc

# install pkg-conf .pc file
install -D -m 0644 miniupnpc.pc %{buildroot}%{_libdir}/pkgconfig/miniupnpc.pc

%check
export CC=%{__cc}
make CFLAGS="%{optflags} -DMINIUPNPC_SET_SOCKET_TIMEOUT" check

%files
%doc Changelog.txt
%doc LICENSE
%doc README
%{_bindir}/upnpc
%doc USAGE

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/miniupnpc
%{_libdir}/*.so
%{_mandir}/man3/miniupnpc.3*

%files -n python-%{name}
%{python_sitearch}/miniupnpc-%{version}-py?.?.egg-info
%{python_sitearch}/miniupnpc.cpython-*.so
