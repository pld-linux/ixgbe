# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	2
%define		pname	ixgbe
Summary:	Intel(R) 10 Gigabit driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel(R) 10 Gigabit
Name:		%{pname}%{_alt_kernel}
Version:	4.4.6
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://downloads.sourceforge.net/e1000/%{pname}-%{version}.tar.gz
# Source0-md5:	e11e83c96afe846b5ee72c309a58e11f
Patch0:		linux-4.6.patch
URL:		http://sourceforge.net/projects/e1000/
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.701
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) 10 Gigabit
adapters with 82598EB chipset.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych z rodziny
Intel(R) 10 Gigabit opartych o układ 82598EB.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-net-ixgbe\
Summary:	Intel(R) 10 Gigabit driver for Linux\
Summary(pl.UTF-8):	Sterownik do karty Intel(R) 10 Gigabit\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-net-ixgbe\
This package contains the Linux driver for the Intel(R) 10 Gigabit\
adapters with 82598EB chipset.\
\
%description -n kernel%{_alt_kernel}-net-ixgbe -l pl.UTF-8\
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych z rodziny\
Intel(R) 10 Gigabit opartych o układ 82598EB.\
\
%files	-n kernel%{_alt_kernel}-net-ixgbe\
%defattr(644,root,root,755)\
%doc ixgbe.7 README\
/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf\
/lib/modules/%{_kernel_ver}/kernel/drivers/net/%{pname}*.ko*\
\
%post	-n kernel%{_alt_kernel}-net-ixgbe\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-net-ixgbe\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%build_kernel_modules -C src -m %{pname}\
%install_kernel_modules -D installed -m src/%{pname} -d kernel/drivers/net -n %{pname} -s current\
%{nil}

%define install_kernel_pkg()\
install -d $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}\
# blacklist kernel module\
cat > $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf <<'EOF'\
blacklist ixgbe\
alias ixgbe ixgbe-current\
EOF\
%{nil}

%{expand:%create_kernel_packages}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1

cp src/Makefile src/Makefile.%{name}
cat > src/Makefile <<'EOF'
obj-m := ixgbe.o
ixgbe-objs := ixgbe_main.o ixgbe_common.o ixgbe_api.o ixgbe_param.o \
ixgbe_lib.o ixgbe_ethtool.o kcompat.o ixgbe_82598.o \
ixgbe_82599.o ixgbe_ptp.o ixgbe_x540.o ixgbe_x550.o ixgbe_sriov.o \
ixgbe_mbx.o ixgbe_dcb.o ixgbe_dcb_82598.o ixgbe_dcb_82599.o \
ixgbe_sysfs.o ixgbe_procfs.o ixgbe_phy.o ixgbe_fcoe.o \
ixgbe_dcb_nl.o ixgbe_debugfs.o

EXTRA_CFLAGS+=-DDRIVER_IXGBE
EXTRA_CFLAGS+=-DIXGBE_PTP
EOF

%build
%{expand:%build_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{expand:%install_kernel_packages}
cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
