Summary: Zabbix Agent
Name: zabbix-howbuy-agent
Version: 2.2.2
Release: 1
Group: Networking/Admin
Source: zabbix-2.2.2.tar.gz
Packager: Kern cai <kernkerncai@gmail.com>
License: GPLv2
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%define prefix /usr/local/zabbix-agent-ops

%description
In addition to the basic monitoring, self monitoring disk IO, MySQL state.Zabbix Agent RPM package for the master 2.2.2 and owner by kerncai.
%prep
cd $RPM_BUILD_DIR
rm -fr zabbix-2.2.2
tar zxf $RPM_SOURCE_DIR/zabbix-2.2.2.tar.gz
patch -p0 < $RPM_SOURCE_DIR/path.patch

%build
cd $RPM_BUILD_DIR/zabbix-2.2.2
./configure --prefix=%{prefix} --enable-agent

%install
cd $RPM_BUILD_DIR/zabbix-2.2.2
make install DESTDIR=$RPM_BUILD_ROOT

# extra.conf
install -D -m0644 $RPM_SOURCE_DIR/extra.conf $RPM_BUILD_ROOT%{prefix}/etc/extra.conf

# var
mkdir -p $RPM_BUILD_ROOT%{prefix}/var

# service
install -D -m0755 $RPM_BUILD_DIR/zabbix-2.2.2/misc/init.d/fedora/core5/zabbix_agentd $RPM_BUILD_ROOT/etc/init.d/%{name}

# cron
install -D -m0644 $RPM_SOURCE_DIR/cron.conf $RPM_BUILD_ROOT/etc/cron.d/%{name}

# iostat
install -D -m0755 $RPM_SOURCE_DIR/dev-discovery.sh $RPM_BUILD_ROOT%{prefix}/bin/dev-discovery.sh
install -D -m0755 $RPM_SOURCE_DIR/iostat-cron.sh $RPM_BUILD_ROOT%{prefix}/bin/iostat-cron.sh
install -D -m0755 $RPM_SOURCE_DIR/iostat-check.sh $RPM_BUILD_ROOT%{prefix}/bin/iostat-check.sh

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

