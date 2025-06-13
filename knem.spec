# TODO:
# - kernel module (+git patches for newer kernels)
# - finish knem.rules file and package it (wrong dir, non-existing rdma group)
#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_with	kernel		# kernel module
%bcond_without	userspace	# userspace tools
#
Summary:	High-performance intra-node MPI communication for large messages
Summary(pl.UTF-8):	Wysokowydajna komunikacja międzywęzłowa MPI dla dużych komunikatów
Name:		knem
Version:	1.1.4
Release:	1
License:	BSD (userspace tools), GPL v2 (kernel module)
Group:		Applications/System
#Source0Download: https://knem.gitlabpages.inria.fr/download/
Source0:	https://gitlab.inria.fr/knem/knem/uploads/4a43e3eb860cda2bbd5bf5c7c04a24b6/%{name}-%{version}.tar.gz
URL:		https://knem.gitlabpages.inria.fr/
BuildRequires:	hwloc-devel >= 1.0
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
High-performance intra-node MPI communication for large messages.

%description -l pl.UTF-8
Wysokowydajna komunikacja międzywęzłowa MPI dla dużych komunikatów.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%if %{with kernel}
%{__make} -C driver/linux
%endif

%if %{with userspace}
%{__make} -C tools
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} -C tools install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/*_test
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING.BSD-3 ChangeLog README REPORTING-BUGS TODO
%attr(755,root,root) %{_bindir}/knem_collectives
%attr(755,root,root) %{_bindir}/knem_cost
%attr(755,root,root) %{_bindir}/knem_loopback
%attr(755,root,root) %{_bindir}/knem_pingpong
%attr(755,root,root) %{_bindir}/knem_region_cost
%endif
