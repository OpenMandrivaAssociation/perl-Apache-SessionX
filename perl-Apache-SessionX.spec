%define upstream_name	 Apache-SessionX
%define upstream_version 2.01

Name:		perl-%{upstream_name}
Version:	%{upstream_version}
Release:	2

Summary:	An extented persistence framework for session data
License:	GPL+ or Artistic
Group:		Development/Perl
Url:		https://metacpan.org/dist/Apache-SessionX
Source0:	https://cpan.metacpan.org/authors/id/G/GR/GRICHTER/Apache-SessionX-2.01.tar.gz
Patch0:		%{name}-2.01.fhs.patch
Patch1:		%{name}-2.01.test.patch

BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl(Apache::Session)
BuildRequires:	perl(DB_File)
BuildArch:	noarch

%define testdir %{_tmppath}/%{name}-%{version}-test

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
%setup -q -n %{upstream_name}-%{upstream_version}
chmod 644 README
%patch -P0
%patch -P1 -p 1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor < /dev/null
%make

%check
rm -rf %{testdir}
mkdir %{testdir}
export TESTDIR=%{testdir}
make test

%clean 
rm -rf %{testdir}

%install
%makeinstall_std
install -d -m 755 %{buildroot}%{_localstatedir}/lib/ApacheSessionX

%files
%doc CHANGES README
%{_mandir}/*/*
%{perl_vendorlib}/Apache
%attr(-,apache,apache) %{_localstatedir}/lib/ApacheSessionX


