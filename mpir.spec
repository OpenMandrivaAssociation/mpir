%define major     23
%define libname   %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

%define majorxx   8
%define libnamexx %mklibname %{name}xx %{majorxx}
%define _disable_rebuild_configure %nil

Name:           mpir
Version:        3.0.0
Release:        5
Summary:        Multiprecision integer library derived from GMP
License:        LGPLv3+
Group:          System/Libraries
Url:            http://mpir.org/
Source:         http://mpir.org/%{name}-%{version}.tar.bz2
Patch0:         %{name}-config.patch

# ppc64 assembly has not yet been ported to little endian
ExcludeArch:    ppc64le

BuildRequires:  gcc-c++
BuildRequires:  m4
BuildRequires:  yasm

%description
MPIR is a library for arbitrary precision arithmetic, operating on signed
integers, rational numbers, and floating point numbers. It has a rich set
of functions, and the functions have a regular interface.

#------------------------------------------------

%package -n     %{libname}
Summary:        Multiprecision integer library derived from GMP
Group:          System/Libraries

%description -n %{libname}
MPIR is a library for arbitrary precision arithmetic, operating on signed
integers, rational numbers, and floating point numbers. It has a rich set
of functions, and the functions have a regular interface.

#------------------------------------------------

%package -n     %{libnamexx}
Summary:        Multiprecision integer library derived from GMP
Group:          System/Libraries

%description -n %{libnamexx}
MPIR is a library for arbitrary precision arithmetic, operating on signed
integers, rational numbers, and floating point numbers. It has a rich set
of functions, and the functions have a regular interface.

#------------------------------------------------

%package -n     %{develname}
Summary:        Development package for %{name}
Group:          Development/C++
Requires:       %{libname} >= %{version}-%{release}
Requires:       %{libnamexx} >= %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:       %{name}xx-devel = %{version}-%{release}
Provides:       lib%{name}xx-devel = %{version}-%{release}
Requires(pre):    info-install
Requires(postun): info-install

%description -n %{develname}
MPIR is an open source multiprecision integer library derived from version
4.2.1 of the GMP.

MPIR is a library for arbitrary precision arithmetic, operating on signed
integers, rational numbers, and floating point numbers. It has a rich set
of functions, and the functions have a regular interface.

This subpackage contains libraries and header files for developing
applications that want to make use of libmpir.

#------------------------------------------------

%prep
%setup -q
%autopatch -p1

%build
%set_build_flags
export CC=gcc
export CXX=g++

./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--disable-static \
	--enable-cxx \
	--enable-fat \
%ifarch %{ix86} %{x86_64}
	--with-yasm=%{_bindir}/yasm
%else
	--with-yasm=/bin/false
%endif

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_removing_rpath
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g.*\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build

%install
%make_install

# we don't want these
find %{buildroot} -name '*.la' -delete

%files -n %{libname}
%{_libdir}/libmpir.so.%{major}{,.*}

%files -n %{libnamexx}
%{_libdir}/libmpirxx.so.%{majorxx}{,.*}

%files -n %{develname}
%doc COPYING README
%{_includedir}/*.h
%{_libdir}/libmpir.so
%{_libdir}/libmpirxx.so
%{_infodir}/mpir.info*.*
