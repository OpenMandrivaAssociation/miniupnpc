%define major 8
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %name

Summary: Library and tool to control NAT in UPnP-enabled routers
Name: miniupnpc
Version: 1.6
Release: %mkrel 1
License: LGPLv2+
Group: System/Libraries
URL: http://miniupnp.free.fr/
Source: http://miniupnp.free.fr/files/%{name}-%{version}.tar.gz
Patch0: miniupnpc-1.6-link.patch
Patch1: miniupnpc-1.6-install-headers.patch
BuildRequires: cmake

%description
miniupnpc is an implementation of a UPnP client library, enabling
applications to access the services provided by an UPnP "Internet
Gateway Device" present on the network. In UPnP terminology, it is
a UPnP Control Point.

%package -n %{libname}
Summary: Library and tool to control NAT in UPnP-enabled routers
Group: System/Libraries

%description -n %{libname}
miniupnpc is an implementation of a UPnP client library, enabling
applications to access the services provided by an UPnP "Internet
Gateway Device" present on the network. In UPnP terminology, it is
a UPnP Control Point.

%package -n %{develname}
Summary: Header files, libraries and development documentation for miniupnpc
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{develname} 
This package contains the header files and development documentation for
miniupnpc. If you like to develop programs using miniupnpc, you will need
to install miniupnpc-devel.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
%cmake -DUPNPC_BUILD_STATIC=OFF -DUPNPC_BUILD_TESTS=OFF
%make

%install
rm -rf %buildroot

%makeinstall_std -C build

%files -n %{libname}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.*.*

%files -n %{develname}
%{_includedir}/miniupnpc
%{_libdir}/*.so
