%define upstream_name	 Apache-SessionX
%define upstream_version 2.01

Name:		perl-%{upstream_name}
Version:	%perl_convert_version %{upstream_version}
Release:	4

Summary:	An extented persistence framework for session data
License:	GPL+ or Artistic
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{upstream_name}
Source0:	http://search.cpan.org/CPAN/authors/id/G/GR/GRICHTER/%{upstream_name}-%{upstream_version}.tar.bz2
Patch0:		%{name}-2.01.fhs.patch
Patch1:		%{name}-2.01.test.patch

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
%patch0
%patch1 -p 1

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


%changelog
* Sat May 28 2011 Funda Wang <fwang@mandriva.org> 2.10.0-3mdv2011.0
+ Revision: 680460
- mass rebuild

* Wed Jul 29 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 2.10.0-2mdv2011.0
+ Revision: 402967
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 2.01-6mdv2009.0
+ Revision: 255284
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Wed Dec 26 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.01-4mdv2008.1
+ Revision: 138120
- fix build dependencies

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Oct 27 2006 Nicolas LÃ©cureuil <neoclust@mandriva.org> 2.01-3mdv2007.0
+ Revision: 73229
- import perl-Apache-SessionX-2.01-3mdk

* Fri Apr 28 2006 Nicolas Lécureuil <neoclust@mandriva.org> 2.01-3mdk
- Fix SPEC according to Perl Policy
	- BuildRequires

* Tue Mar 14 2006 Nicolas Lécureuil <neoclust@mandriva.org> 2.01-2mdk
- Add BuildRequires

* Mon Nov 28 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.01-1mdk
- new version 
- %%{1}mdv2007.1
- spec cleanup
- use FHS-compliant /var/lib/ApacheSessionX for storing data
- don't deal with storage directory permission
- fix doc files perms
- fix test to use temp files

