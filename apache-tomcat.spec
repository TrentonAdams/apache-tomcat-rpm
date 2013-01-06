Name: apache-tomcat
Version: 7.0.34
Release: 9
Summary: Open source software implementation of the Java Servlet and JavaServer Pages technologies.
Group: Productivity/Networking/Web/Servers 
License: Apache Software License.
Url: http://tomcat.apache.org 
Source0: http://apache.mirror.iweb.ca/tomcat/tomcat-7/v%{version}/src/%{name}-%{version}-src.tar.gz
Source1: http://www.apache.org/dist/tomcat/tomcat-7/v%{version}/src/%{name}-%{version}-src.tar.gz.md5
Source2: https://raw.github.com/TrentonAdams/%{name}-rpm/master/%{name}-initscript

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
Requires: %{name}
BuildArch: noarch

%description manager
The management web application of Apache Tomcat.

%package ROOT
Summary: The ROOT web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}
BuildArch: noarch

%description ROOT
The ROOT web application of Apache Tomcat.

%package docs
Summary: The docs web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}
BuildArch: noarch

%description docs
The docs web application of Apache Tomcat.

%package examples
Summary: The examples web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}
BuildArch: noarch

%description examples
The examples web application of Apache Tomcat.

%package host-manager
Summary: The host-manager web application of Apache Tomcat.
Group: System Environmnet/Applications
Requires: %{name}
BuildArch: noarch

%description host-manager
The host-manager web application of Apache Tomcat.

%prep
cd %{_sourcedir}/
md5sum -c %{name}-%{version}-src.tar.gz.md5 || (echo "Source archive failed m5sum check" && exit 1)

%setup -q -n %{name}-%{version}-src

# This tells ant to install software in a specific directory.
cat << EOF >> build.properties
base.path=%{buildroot}/opt/%{name}
EOF

%build
cd %{_builddir}/%{name}-%{version}-src
ant

%install
rm -Rf %{buildroot}
mkdir -p %{buildroot}/opt/%{name}
mkdir -p %{buildroot}/opt/%{name}/pid
mkdir -p %{buildroot}/etc/init.d/
mkdir -p %{buildroot}/var/run/%{name}
cd %{_builddir}/%{name}-%{version}-src
ls -l
%{__cp} -Rip ./output/build/{bin,conf,lib,logs,temp,webapps} %{buildroot}/opt/%{name}
%{__cp} %{SOURCE2} %{buildroot}/etc/init.d/%{name}

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
%dir /opt/%{name}
%config /opt/%{name}/conf/*
/opt/%{name}/bin
/opt/%{name}/lib
/opt/%{name}/logs
/opt/%{name}/temp
/opt/%{name}/pid
%dir /opt/%{name}/webapps
/var/run/%{name}
%attr(0750,tomcat,tomcat) /opt/%{name}/bin/*.sh
%attr(0755,root,root) /etc/init.d/%{name}

%files manager
/opt/%{name}/webapps/manager

%files ROOT
/opt/%{name}/webapps/ROOT

%files docs
/opt/%{name}/webapps/docs

%files examples
/opt/%{name}/webapps/examples

%files host-manager
/opt/%{name}/webapps/host-manager

%changelog
* Mon Jul 4 2011 - robert (at) meinit.nl
- Initial release.
