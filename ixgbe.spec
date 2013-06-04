# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%ifarch sparc
%undefine	with_smp
%endif

%if %{without kernel}
%undefine with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%define		rel	18
%define		pname	ixgbe
Summary:	Intel(R) 10 Gigabit driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel(R) 10 Gigabit
Name:		%{pname}%{_alt_kernel}
Version:	3.15.1
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://downloads.sourceforge.net/e1000/%{pname}-%{version}.tar.gz
# Source0-md5:	3558384b9eb31bf1185117091ac5f567
URL:		http://sourceforge.net/projects/e1000/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) 10 Gigabit
adapters with 82598EB chipset.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych z rodziny
Intel(R) 10 Gigabit opartych o układ 82598EB.

%package -n kernel%{_alt_kernel}-net-ixgbe
Summary:	Intel(R) 10 Gigabit driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel(R) 10 Gigabit
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-net-ixgbe
This package contains the Linux driver for the Intel(R) 10 Gigabit
adapters with 82598EB chipset.

%description -n kernel%{_alt_kernel}-net-ixgbe -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych z rodziny
Intel(R) 10 Gigabit opartych o układ 82598EB.

%prep
%setup -q -n %{pname}-%{version}
cp src/Makefile src/Makefile.%{name}
cat > src/Makefile <<'EOF'
obj-m := ixgbe.o
ixgbe-objs := ixgbe_main.o ixgbe_common.o ixgbe_api.o ixgbe_param.o \
ixgbe_lib.o ixgbe_ethtool.o kcompat.o ixgbe_82598.o \
ixgbe_82599.o ixgbe_ptp.o ixgbe_x540.o ixgbe_sriov.o \
ixgbe_mbx.o ixgbe_dcb.o ixgbe_dcb_82598.o ixgbe_dcb_82599.o \
ixgbe_sysfs.o ixgbe_procfs.o ixgbe_phy.o ixgbe_fcoe.o \
ixgbe_dcb_nl.o

EXTRA_CFLAGS=-DDRIVER_IXGBE
EOF

%build
%build_kernel_modules -C src -m %{pname}

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/%{pname} -d kernel/drivers/net -n %{pname} -s current
# blacklist kernel module
cat > $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf <<'EOF'
blacklist ixgbe
alias ixgbe ixgbe-current
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-ixgbe
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-ixgbe
%depmod %{_kernel_ver}

%files	-n kernel%{_alt_kernel}-net-ixgbe
%defattr(644,root,root,755)
%doc ixgbe.7 README
/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/%{pname}*.ko*
