%define module	Apache-SessionX
%define name	perl-%{module}
%define version	2.01
%define release	%mkrel 3
%define testdir %{_tmppath}/%{name}-%{version}-test

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	An extented persistence framework for session data
License:	GPL or Artistic
Group:		Development/Perl
Source:		http://search.cpan.org/CPAN/authors/id/G/GR/GRICHTER/%{module}-%{version}.tar.bz2
Patch0:		%{name}-2.01.fhs.patch
Patch1:		%{name}-2.01.test.patch
Url:		http://search.cpan.org/dist/%{module}
%if %{mdkversion} < 1010
BuildRequires:	perl-devel
%endif
BuildRequires:	perl(Apache::Session)
BuildRequires:	perl(Mysql)
BuildRequires:	perl(DBD::Pg)
BuildRequires:  perl(DB_File)
BuildArch:	noarch

%description
Apache::SessionX extends Apache::Session. It was initialy written to use
Apache::Session from inside of HTML::Embperl, but is seems to be useful
outside of Embperl as well, so here is it as standalone module.

Apache::Session is a persistence framework which is particularly
useful for tracking session data between httpd requests. Apache::Session is
designed to work with Apache and mod_perl, but it should work under CGI and
other web servers, and it also works outside of a web server altogether.

Apache::Session consists of five components: the interface, the object
store, the lock manager, the ID generator, and the serializer. The interface
is defined in SessionX.pm, which is meant to be easily subclassed. The
object store can be the filesystem, a Berkeley DB, a MySQL DB, an Oracle DB,
or a Postgres DB. Locking is done by lock files, semaphores, or the locking
capabilities of MySQL and Postgres. Serialization is done via Storable, and
optionally ASCII-fied via MIME or pack(). ID numbers are generated via MD5.
The reader is encouraged to extend these capabilities to meet his own
requirements.

%prep
%setup -q -n %{module}-%{version}
chmod 644 README
%patch0
%patch1 -p 1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor < /dev/null
%make

%check
%{__rm} -rf %{testdir}
mkdir %{testdir}
export TESTDIR=%{testdir}
%{__make} test

%clean 
%{__rm} -rf %{buildroot}
%{__rm} -rf %{testdir}

%install
%{__rm} -rf %{buildroot}
%makeinstall_std
install -d -m 755 %{buildroot}%{_localstatedir}/ApacheSessionX

%files
%defattr(-,root,root)
%doc CHANGES README
%{_mandir}/*/*
%{perl_vendorlib}/Apache
%attr(-,apache,apache) %{_localstatedir}/ApacheSessionX



