from conans import ConanFile, CMake, tools, Meson
import os


class GstpluginsbaseConan(ConanFile):
    name = "gst-plugins-base-1.0"
    version = "1.14.4"
    description = "'Base' GStreamer plugins and helper libraries"
    url = "https://github.com/conanos/gst-plugins-base-1.0"
    homepage = "https://github.com/GStreamer/gst-plugins-base"
    license = "GPLv2+"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = ('glib/2.58.0@conanos/dev','gstreamer-1.0/1.14.4@conanos/dev','libxml2/2.9.8@conanos/dev','libogg/1.3.3@conanos/dev',
                'pango/1.40.14@conanos/dev','libtheora/1.1.1@conanos/dev','libvisual/0.4.0@conanos/dev','libvorbis/1.3.5@conanos/dev',
                'zlib/1.2.11@conanos/dev','orc/0.4.28@conanos/dev','opus/1.2.1@conanos/dev','graphene/1.4.0@conanos/dev',
                'libjpeg-turbo/1.5.2@conanos/dev','libpng/1.6.34@conanos/dev','libffi/3.3-rc0@conanos/dev',
                
                'cairo/1.14.12@conanos/dev','fontconfig/2.12.6@conanos/dev','freetype/2.9.0@conanos/dev',
                'harfbuzz/1.7.5@conanos/dev','pixman/0.34.0@conanos/dev',
                'gobject-introspection/1.58.0@conanos/dev'
                )
    source_subfolder = "source_subfolder"
    remotes = {'origin': 'https://github.com/GStreamer/gst-plugins-base.git'}
    
    def source(self):
        #tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        #extracted_dir = "gst-plugins-base-" + self.version
        #os.rename(extracted_dir, self.source_subfolder)

        tools.mkdir(self.source_subfolder)
        with tools.chdir(self.source_subfolder):
            self.run('git init')
            for key, val in self.remotes.items():
                self.run("git remote add %s %s"%(key, val))
            self.run('git fetch --all')
            self.run('git reset --hard %s'%(self.version))
            self.run('git submodule update --init --recursive')

    def build(self):
        with tools.chdir(self.source_subfolder):
            with tools.environment_append({
                'LD_LIBRARY_PATH':'%s/lib'%(self.deps_cpp_info["libffi"].rootpath),
                'PATH':'%s/bin:%s/bin:%s'%(self.deps_cpp_info["orc"].rootpath,self.deps_cpp_info["gobject-introspection"].rootpath,os.getenv("PATH")),
                }):

                meson = Meson(self)
                _defs = {'disable_introspection':'false','disable_examples':'true','disable_gtkdoc':'true',
                         'prefix':'%s/builddir/install'%(os.getcwd()), 'libdir':'lib','use_orc':'yes'}
                meson.configure(
                    defs=_defs,
                    source_dir = '%s'%(os.getcwd()),
                    build_dir= '%s/builddir'%(os.getcwd()),
                    pkg_config_paths=['%s/lib/pkgconfig'%(self.deps_cpp_info["glib"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["gstreamer-1.0"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libxml2"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libogg"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["pango"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libtheora"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libvisual"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libvorbis"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["zlib"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["orc"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["opus"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["graphene"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libjpeg-turbo"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libpng"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libffi"].rootpath),#required by gobject

                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["cairo"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["fontconfig"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["freetype"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["harfbuzz"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["pixman"].rootpath),
                                      ]
                                )
                meson.build(args=['-j2'])
                self.run('ninja -C {0} install'.format(meson.build_dir))

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir/install"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

