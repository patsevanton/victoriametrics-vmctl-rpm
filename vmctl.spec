Name:    vmctl
Version: 0.1.2
Release: 4
Summary: Victoria Metrics command line tool

Group:   Development Tools
License: ASL 2.0
URL: https://github.com/VictoriaMetrics/vmctl/releases/download/%{version}/vmctl-%{version}-linux-amd64.tar.gz
Source0: %{name}.service
Source1: vmctl.conf
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%description
Victoria Metrics command line tool

%prep
curl -L %{url} > vmctl-linux-amd64.tar.gz
tar -zxf vmctl-linux-amd64.tar.gz
ls

%install
%{__install} -m 0755 -d %{buildroot}%{_bindir}
%{__install} -m 0755 -d %{buildroot}/etc/default/
cp %{SOURCE1} %{buildroot}/etc/default/
cp vmctl-linux-amd64 %{buildroot}%{_bindir}/vmctl
%{__install} -m 0755 -d %{buildroot}/var/lib/vmctl

%pre
/usr/bin/getent group victoriametrics > /dev/null || /usr/sbin/groupadd -r victoriametrics
/usr/bin/getent passwd victoriametrics > /dev/null || /usr/sbin/useradd -r -d /var/lib/victoria-metrics-data -s /bin/bash -g victoriametrics victoriametrics
%{__mkdir} /var/lib/victoria-metrics-data

%files
/etc/default/vmctl.conf
%{_bindir}/vmctl
%dir %attr(0775, victoriametrics, victoriametrics) /var/lib/vmctl
