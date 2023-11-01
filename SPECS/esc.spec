Name: esc 
Version: 1.1.2
Release: 16%{?dist}
Summary: Enterprise Security Client Smart Card Client
License: GPL+
URL: http://directory.fedora.redhat.com/wiki/CoolKey 
Group: Applications/Internet

#Fix to harden linker flags.
Patch0: esc-gcc11.patch
Patch1: esc-1.1.2-fix1.patch
Patch2: esc-1.1.2-fix2.patch
Patch3: esc-1.1.2-fix3.patch
Patch4: esc-1.1.2-fix4.patch
Patch5: esc-1.1.2-fix5.patch
Patch6: esc-1.1.2-fix6.patch
Patch7: esc-1.1.2-fix7.patch
Patch8: esc-1.1.2-fix8.patch
Patch9: esc-1.1.2-fix9.patch
Patch10: esc-1.1.2-fix10.patch
Patch11: esc-1.1.2-fix11.patch
Patch12: esc-1.1.2-fix12.patch
Patch13: esc-1.1.2-fix13.patch


#BuildRequires: doxygen fontconfig-devel
BuildRequires: glib2-devel atk-devel
BuildRequires: pkgconfig
BuildRequires: nspr-devel nss-devel nss-static
#BuildRequires: libX11-devel libXt-devel

BuildRequires: pcsc-lite-devel
BuildRequires: desktop-file-utils
BuildRequires: gcc-c++
%if ! 0%{?rhel} >= 9
BuildRequires: pkgconfig(gconf-2.0)
%endif
BuildRequires: dbus-glib-devel
BuildRequires: glib2-devel
BuildRequires: opensc
BuildRequires: gobject-introspection-devel
BuildRequires: gtk3-devel
BuildRequires: gjs-devel
BuildRequires: chrpath


Requires: pcsc-lite >=  1.9.1-3
Requires: pcsc-lite-ccid >= 1.4.34-4
Requires: nss nspr
Requires: dbus
Requires: opensc
Requires: gjs
Requires: gobject-introspection
Requires: gtk3
Requires: glib2

AutoReqProv: 0

%define debug_build       0

%define escname %{name}-%{version}
%define escdir %{_libdir}/%{escname}
%define escbindir %{_bindir}
%define esc_chromepath   chrome/content/esc
%define appdir applications
%define icondir %{_datadir}/icons/hicolor/48x48/apps
%define esc_vendor esc 
%define autostartdir %{_sysconfdir}/xdg/autostart
%define pixmapdir  %{_datadir}/pixmaps
%define docdir    %{_defaultdocdir}/%{name}

Source0: http://pki.fedoraproject.org/pki/sources/%name/%{escname}.tar.bz2 
Source1: http://pki.fedoraproject.org/pki/sources/%name/esc
Source2: http://pki.fedoraproject.org/pki/sources/%name/esc.desktop
Source3: http://pki.fedoraproject.org/pki/sources/%name/esc.png


%description
Enterprise Security Client allows the user to enroll and manage their
cryptographic smartcards.

%prep

%setup -q -c -n %{escname}

#patch esc 
%patch0 -p1
%patch1 -p1 -b .fix1
%patch2 -p1 -b .fix2
%patch3 -p1 -b .fix3
%patch4 -p1 -b .fix4
%patch5 -p1 -b .fix5
%patch6 -p1 -b .fix6
%patch7 -p1 -b .fix7
%patch8 -p1 -b .fix8
%patch9 -p1 -b .fix9
%patch10 -p1 -b .fix10
%patch11 -p1 -b .fix11
%patch12 -p1 -b .fix12
%patch13 -p1 -b .fix13


%build

echo $RPM_BUILD_DIR

echo "build section" $PWD
cd esc 

./autogen.sh
make 
%install
echo "install section" $PWD
cd esc
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/%{escbindir}
mkdir -p $RPM_BUILD_ROOT/%{icondir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{appdir}
mkdir -p $RPM_BUILD_ROOT/%{pixmapdir}
mkdir -p $RPM_BUILD_ROOT/%{docdir}

echo "dir: "  $RPM_BUILD_ROOT/%{escbindir}/%{name}
sed -e 's;\$LIBDIR;'%{_libdir}';g' -e 's;\$VERSION;'%{version}';g'  %{SOURCE1} > $RPM_BUILD_ROOT/%{escbindir}/%{name}
chmod 755 $RPM_BUILD_ROOT/%{escbindir}/%{name}

mkdir -p $RPM_BUILD_ROOT/%{escdir}
mkdir -p $RPM_BUILD_ROOT/%{escdir}/lib

cp $RPM_BUILD_ROOT/usr/local/bin/* $RPM_BUILD_ROOT/%{escdir}

cp -rf $RPM_BUILD_ROOT/usr/local/lib $RPM_BUILD_ROOT/%{escdir}

rm $RPM_BUILD_ROOT/%{escdir}/lib/*.a
rm $RPM_BUILD_ROOT/%{escdir}/lib/*.la


rm -rf $RPM_BUILD_ROOT/usr/local

cp %{SOURCE3} $RPM_BUILD_ROOT/%{icondir}
ln -s $RPMBUILD_ROOT%{icondir}/esc.png $RPM_BUILD_ROOT/%{pixmapdir}/esc.png

cp %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/%{appdir}

cd %{_builddir}
cp %{escname}/esc/LICENSE $RPM_BUILD_ROOT/%{docdir}

#Get rid of rpath
chrpath --delete $RPM_BUILD_ROOT/%{escdir}/lib/libcoolkeymgr-1.0.so


%files
%{!?_licensedir:%global license %%doc}
%license %{docdir}/LICENSE

%{escbindir}/esc
%{escdir}/lib
%{escdir}/esc.js
%{escdir}/esc.properties
%{escdir}/operationDialog.js
%{escdir}/phoneHome.js
%{escdir}/pinDialog.js
%{escdir}/opensc.esc.conf


%{icondir}/esc.png
%{pixmapdir}/esc.png
%{_datadir}/%{appdir}/esc.desktop

%changelog
* Wed Jun 29 2022 Jack Magne <jmagne@redhat.com> - 1.1.2-16
Resolves: rhbs #2050849
- Bug 2050849 - Volkswagen Siemens CardOS M4.4 and 5.0 cards display incorrect status in ESC [RHEL 9.1]
* Thu Dec 16 2021 Jack Magne <jmagne@redhat.com> - 1.1.2-15
Resolves: rhbs #2007544,2000928,2000929
- Appease rpminspect
* Tue Dec 13 2021 Jack Magne <jmagne@redhat.com> - 1.1.2-14
Resolves: rhbs #2007544,2000928,2000929
- Bugzilla Bug  2007544 - The esc provides outdated configuration for opensc
- Bugzilla Bug  2000928 - ESC does not detect smart cards and crashes upon launch [rhel-9.0.0]
- Bugzilla Bug  2000929 - [RHEL-9][AppStream] esc present in comps but missing from repository [rhel-9.0.0] 
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.1.2-11
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
-
* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 1.1.2-10
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937
-
* Tue Jan 26 2021 Tomas Popela <tpopela@redhat.com> - 1.1.2-9
- Don't enable GConf2 on RHEL 9 as it won't be available there.
-
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
-
* Tue Jul 28 2020 Jeff Law <law@redhat.com> - 1.1.2-7
- Force C++14 as this code is not C++17 ready
- Fix sprintf format issue
- Fix ordered comparison of a pointer against zero issue
-
* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
-
* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
-
* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
-
* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
