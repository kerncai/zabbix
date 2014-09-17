Summary: Zabbix Agent
Name: zabbix-agent-bi
Version: 2.2.5
Release: 4
Group: Networking/Admin
Source: zabbix-2.2.5.tar.gz
Packager: kerncai <kernkerncai@gmail.com>
License: GPLv2
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%define prefix /usr/local/zabbix-agent-bi

%description
Zabbix Agent

%prep
cd $RPM_BUILD_DIR
rm -fr zabbix-2.2.5
tar zxf $RPM_SOURCE_DIR/zabbix-2.2.5.tar.gz
patch -p0 < $RPM_SOURCE_DIR/path.patch

%build
cd $RPM_BUILD_DIR/zabbix-2.2.5
./configure --prefix=%{prefix} --enable-agent

%install
cd $RPM_BUILD_DIR/zabbix-2.2.5
make install DESTDIR=$RPM_BUILD_ROOT

# extra.conf
install -D -m0644 $RPM_SOURCE_DIR/extra.conf $RPM_BUILD_ROOT%{prefix}/etc/extra.conf

# var
mkdir -p $RPM_BUILD_ROOT%{prefix}/var

# service
install -D -m0755 $RPM_BUILD_DIR/zabbix-2.2.5/misc/init.d/fedora/core5/zabbix_agentd $RPM_BUILD_ROOT/etc/init.d/%{name}

# cron
install -D -m0644 $RPM_SOURCE_DIR/cron.conf $RPM_BUILD_ROOT/etc/cron.d/%{name}

# iostat
install -D -m0755 $RPM_SOURCE_DIR/dev-discovery.sh $RPM_BUILD_ROOT%{prefix}/bin/dev-discovery.sh
install -D -m0755 $RPM_SOURCE_DIR/iostat-cron.sh $RPM_BUILD_ROOT%{prefix}/bin/iostat-cron.sh
install -D -m0755 $RPM_SOURCE_DIR/iostat-check.sh $RPM_BUILD_ROOT%{prefix}/bin/iostat-check.sh

#port-discovery
install -D -m0755 $RPM_SOURCE_DIR/port-discovery.sh $RPM_BUILD_ROOT%{prefix}/bin/port-discovery.sh

%clean
rm -fr $RPM_BUILD_ROOT

%files
%dir %{prefix}
%{prefix}/bin
%{prefix}/sbin
%{prefix}/share

%dir %{prefix}/etc
%{prefix}/etc/extra.conf
%config(noreplace) %{prefix}/etc/zabbix_agentd.conf
%config(noreplace) %{prefix}/etc/zabbix_agentd.conf.d
%config(noreplace) %{prefix}/etc/zabbix_agent.conf
%config(noreplace) %{prefix}/etc/zabbix_agent.conf.d

%attr(-,zabbix,zabbix) %{prefix}/var

/etc/init.d/%{name}
/etc/cron.d/%{name}

%pre
if [ $1 -eq 1 ]; then
    user_check="`grep zabbix /etc/passwd | wc -l`"
    group_check="`grep zabbix /etc/group | wc -l`"

    if [[ $user_check -eq 0 ]];
    then
        groupadd zabbix
    fi

    if [[ $group_check -eq 0 ]];
    then
        useradd -M -d %{prefix}/var -s /sbin/nologin -g zabbix zabbix
    fi
fi

%post
if [ $1 -eq 1 ]; then
    chkconfig --add %{name}
    chkconfig --level 345 %{name} on
    service %{name} start
fi

%preun
if [ $1 -eq 0 ]; then
    service %{name} stop
    chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
    service %{name} condrestart
fi

