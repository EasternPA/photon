%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Name:           pycurl3
Version:        7.43.0.5
Release:        1%{?dist}
Summary:        A Python interface to libcurl
Group:          Development/Languages
License:        LGPLv2+ and an MIT/X
URL:            http://pycurl.sourceforge.net/
Source0:        http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
%define sha1    pycurl=a19159dd7cdf8b0c9f96d57e23b3717010c51041
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  openssl-devel
BuildRequires:  curl-devel

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
%if %{with_check}
BuildRequires: python3-setuptools, vsftpd, curl-libs
BuildRequires: python3-xml
%endif
Requires:       curl
Requires:       python3
Requires:       python3-libs
%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.


%package doc
Summary:    Documentation and examples for pycurl
Requires:   %{name} = %{version}

%description doc
Documentation and examples for pycurl

%prep
%setup -q -n pycurl-%{version}
rm -f doc/*.xml_validity
#chmod a-x examples/*

# removing prebuilt-binaries
rm -f tests/fake-curl/libcurl/*.so

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" python3 setup.py build

%install
rm -rf %{buildroot}
python3 setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/pycurl
chmod 755 %{buildroot}%{python3_sitelib}/pycurl*.so


%check
export PYCURL_VSFTPD_PATH=vsftpd
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose nose-show-skipped bottle flaky pyflakes
rm -f tests/multi_option_constants_test.py tests/ftp_test.py tests/option_constants_test.py tests/seek_cb_test.py
LANG=en_US.UTF-8  make test PYTHON=python%{python3_version} NOSETESTS="nosetests-3.4 -v"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%files doc
%defattr(-,root,root)
%doc COPYING-LGPL COPYING-MIT RELEASE-NOTES.rst ChangeLog README.rst examples doc tests

%changelog
*   Mon Jul 27 2020 Tapas Kundu <tkundu@vmware.com> 7.43.0.5-1
-   Update to 7.43.0.5
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 7.43.0-5
-   Mass removal python2
*   Mon Nov 12 2018 Tapas Kundu <tkundu@vmware.com> 7.43.0-4
-   Fixed the make check.
*   Mon Aug 14 2017 Chang Lee <changlee@vmware.com> 7.43.0-3
-   Added check requires and fixed check
*   Wed May 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 7.43.0-2
-   Using python2 explicitly while building
*   Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 7.43.0-1
-   Upgrade to 7.43.0  and add pycurl3
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 7.21.5-5
-   BuildRequires curl-devel.
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 7.21.5-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.21.5-3
-   GA - Bump release of all rpms
*   Fri Apr 29 2016 Divya Thaluru <dthaluru@vmware.com> 7.21.5-2
-   Removing prebuilt binaries
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 7.21.5-1
-   Upgrade version
*   Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 7.19.5.1-2
-   Added Doc subpackage. Removed chmod a-x for examples.
*   Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
-   Initial build.  First version
