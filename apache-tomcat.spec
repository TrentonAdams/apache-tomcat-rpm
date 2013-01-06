Name: apache-tomcat
Version: 7.0.34
Release: 9
Summary: Open source software implementation of the Java Servlet and JavaServer Pages technologies.
Group: Productivity/Networking/Web/Servers 
License: Apache Software License.
Url: http://tomcat.apache.org 
Source0: http://apache.mirror.iweb.ca/tomcat/tomcat-7/v%{version}/src/%{name}-%{version}-src.tar.gz
Source1: http://www.apache.org/dist/tomcat/tomcat-7/v%{version}/src/%{name}-%{version}-src.tar.gz.md5
Source2: apache-tomcat-initscript

BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildRequires: ant
BuildRequires: ant-trax
Requires: java
BuildArch: x86_64

%description
Apache Tomcat is an open source software implementation of the Java Servlet and JavaServer Pages technologies. The Java Servlet and JavaServer Pages specifications are developed under the Java Community Process.

%package manager
Summary: The management web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}-%{version}-%{release}
BuildArch: noarch

%description manager
The management web application of Apache Tomcat.

%package ROOT
Summary: The ROOT web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}-%{version}-%{release}
BuildArch: noarch

%description ROOT
The ROOT web application of Apache Tomcat.

%package docs
Summary: The docs web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}-%{version}-%{release}
BuildArch: noarch

%description docs
The docs web application of Apache Tomcat.

%package examples
Summary: The examples web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}-%{version}-%{release}
BuildArch: noarch

%description examples
The examples web application of Apache Tomcat.

%package host-manager
Summary: The host-manager web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}-%{version}-%{release}
BuildArch: noarch

%description host-manager
The host-manager web application of Apache Tomcat.

%prep
cd %{_sourcedir}/
md5sum -c %{name}-%{version}-src.tar.gz.md5 || (echo "Source archive failed m5sum check" && exit 1)

%setup -q -n %{name}-%{version}-src

# This tells ant to install software in a specific directory.
cat << EOF >> build.properties
base.path=%{buildroot}/opt/apache-tomcat
EOF

%build
cd %{_builddir}/%{name}-%{version}-src
ant

%install
rm -Rf %{buildroot}
mkdir -p %{buildroot}/opt/apache-tomcat
mkdir -p %{buildroot}/opt/apache-tomcat/pid
mkdir -p %{buildroot}/etc/init.d/
mkdir -p %{buildroot}/var/run/apache-tomcat
cd %{_builddir}/%{name}-%{version}-src
ls -l
%{__cp} -Rip ./output/build/{bin,conf,lib,logs,temp,webapps} %{buildroot}/opt/apache-tomcat
#%{__cp} -Rip ./webapps/ %{buildroot}/opt/apache-tomcat
%{__cp} %{_sourcedir}/apache-tomcat-initscript %{buildroot}/etc/init.d/apache-tomcat

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}

%pre
getent group tomcat > /dev/null || groupadd -r tomcat
getent passwd tomcat > /dev/null || useradd -r -g tomcat tomcat

%post
chkconfig --add %{name}

%preun
if [ "$1" = "0" ] ; then
 service %{name} stop > /dev/null 2>&1
 chkconfig --del %{name}
fi

%files
%defattr(640,tomcat,tomcat,750)
%dir /opt/apache-tomcat
%config /opt/apache-tomcat/conf/*
/opt/apache-tomcat/bin
/opt/apache-tomcat/lib
/opt/apache-tomcat/logs
/opt/apache-tomcat/temp
/opt/apache-tomcat/pid
%dir /opt/apache-tomcat/webapps
/var/run/apache-tomcat
%attr(0750,tomcat,tomcat) /opt/apache-tomcat/bin/*.sh
%attr(0755,root,root) /etc/init.d/apache-tomcat

%files manager
/opt/apache-tomcat/webapps/manager

%files ROOT
/opt/apache-tomcat/webapps/ROOT

%files docs
/opt/apache-tomcat/webapps/docs

%files examples
/opt/apache-tomcat/webapps/examples

%files host-manager
/opt/apache-tomcat/webapps/host-manager

%changelog
* Mon Jul 4 2011 - robert (at) meinit.nl
- Initial release.
