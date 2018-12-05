from conans import ConanFile, CMake, tools, Meson
from conanos.build import config_scheme
import os


class GstpluginsbaseConan(ConanFile):
    name = "gst-plugins-base"
    version = "1.14.4"
    description = "'Base' GStreamer plugins and helper libraries"
    url = "https://github.com/conanos/gst-plugins-base-1.0"
    homepage = "https://github.com/GStreamer/gst-plugins-base"
    license = "GPLv2+"
    patch = "0001-ellipsis-coding-fix.patch"
    exports = [patch]
    generators = "gcc","visual_studio"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        'fPIC': [True, False]
    }
    default_options = { 'shared': True, 'fPIC': True }
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    #requires = ('glib/2.58.0@conanos/dev','gstreamer-1.0/1.14.4@conanos/dev','libxml2/2.9.8@conanos/dev','libogg/1.3.3@conanos/dev',
    #            'pango/1.40.14@conanos/dev','libtheora/1.1.1@conanos/dev','libvisual/0.4.0@conanos/dev','libvorbis/1.3.5@conanos/dev',
    #            'zlib/1.2.11@conanos/dev','orc/0.4.28@conanos/dev','opus/1.2.1@conanos/dev','graphene/1.4.0@conanos/dev',
    #            'libjpeg-turbo/1.5.2@conanos/dev','libpng/1.6.34@conanos/dev','libffi/3.3-rc0@conanos/dev',
    #            
    #            'cairo/1.14.12@conanos/dev','fontconfig/2.12.6@conanos/dev','freetype/2.9.0@conanos/dev',
    #            'harfbuzz/1.7.5@conanos/dev','pixman/0.34.0@conanos/dev',
    #            'gobject-introspection/1.58.0@conanos/dev'
    #            )

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
    
    def configure(self):
        del self.settings.compiler.libcxx

        config_scheme(self)


    def requirements(self):
        self.requires.add("glib/2.58.1@conanos/stable")
        self.requires.add("gstreamer/1.14.4@conanos/stable")
        self.requires.add("libogg/1.3.3@conanos/stable")
        self.requires.add("pango/1.42.4@conanos/stable")
        self.requires.add("libtheora/1.1.1@conanos/stable")
        self.requires.add("libvorbis/1.3.6@conanos/stable")
        self.requires.add("zlib/1.2.11@conanos/stable")
        self.requires.add("orc/0.4.28@conanos/stable")
        self.requires.add("opus/1.2.1@conanos/stable")
        self.requires.add("graphene/1.8.2@conanos/stable")
        self.requires.add("libpng/1.6.34@conanos/stable")
        self.requires.add("libffi/3.299999@conanos/stable")
    
    def build_requirements(self):
        self.build_requires("harfbuzz/2.1.3@conanos/stable")
        self.build_requires("freetype/2.9.1@conanos/stable")
        self.build_requires("fontconfig/2.13.0@conanos/stable")
        self.build_requires("pixman/0.34.0@conanos/stable")
        self.build_requires("fribidi/1.0.5@conanos/stable")
        self.build_requires("cairo/1.15.12@conanos/stable")
        self.build_requires("bzip2/1.0.6@conanos/stable")
        if self.settings.os == "Windows":
            self.build_requires("expat/2.2.5@conanos/stable")
        if self.settings.os == "Linux":
            self.build_requires("libuuid/1.0.3@conanos/stable")

    
    def source(self):
        remotes = {'origin': 'https://github.com/GStreamer/gst-plugins-base.git'}
        extracted_dir = self.name + "-" + self.version
        tools.mkdir(extracted_dir)
        with tools.chdir(extracted_dir):
            self.run('git init')
            for key, val in remotes.items():
                self.run("git remote add %s %s"%(key, val))
            self.run('git fetch --all')
            self.run('git reset --hard %s'%(self.version))
            self.run('git submodule update --init --recursive')
            self.run('git am %s'%(os.path.join('..',self.patch)))
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        #with tools.chdir(self._source_subfolder):
        #    with tools.environment_append({
        #        'LD_LIBRARY_PATH':'%s/lib'%(self.deps_cpp_info["libffi"].rootpath),
        #        'PATH':'%s/bin:%s/bin:%s'%(self.deps_cpp_info["orc"].rootpath,self.deps_cpp_info["gobject-introspection"].rootpath,os.getenv("PATH")),
        #        }):

        #        meson = Meson(self)
        #        _defs = {'disable_introspection':'false','disable_examples':'true','disable_gtkdoc':'true',
        #                 'prefix':'%s/builddir/install'%(os.getcwd()), 'libdir':'lib','use_orc':'yes'}
        #        meson.configure(
        #            defs=_defs,
        #            source_dir = '%s'%(os.getcwd()),
        #            build_dir= '%s/builddir'%(os.getcwd()),
        #            pkg_config_paths=['%s/lib/pkgconfig'%(self.deps_cpp_info["glib"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["gstreamer-1.0"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["libxml2"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["libogg"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["pango"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["libtheora"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["libvisual"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["libvorbis"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["zlib"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["orc"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["opus"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["graphene"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["libjpeg-turbo"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["libpng"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["libffi"].rootpath),#required by gobject

        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["cairo"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["fontconfig"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["freetype"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["harfbuzz"].rootpath),
        #                              '%s/lib/pkgconfig'%(self.deps_cpp_info["pixman"].rootpath),
        #                              ]
        #                        )
        #        meson.build(args=['-j2'])
        #        self.run('ninja -C {0} install'.format(meson.build_dir))
        pkg_config_paths=[ os.path.join(self.deps_cpp_info[i].rootpath, "lib", "pkgconfig") 
                           for i in ["glib","gstreamer","libogg","pango","libtheora","libvorbis","zlib","orc","opus",
                                     "graphene","libpng","libffi","harfbuzz","freetype","fontconfig","pixman","fribidi","cairo","expat","bzip2"] ]
        prefix = os.path.join(self.build_folder, self._build_subfolder, "install")
        defs = {'prefix' : prefix, 'disable_introspection':'true'}
        if self.settings.os == "Linux":
            defs.update({'libdir':'lib'})
        binpath=[ os.path.join(self.deps_cpp_info[i].rootpath, "bin") for i in ["glib"] ]
        include = [ os.path.join(self.deps_cpp_info["pango"].rootpath, "include","pango-1.0"),
                    os.path.join(self.deps_cpp_info["cairo"].rootpath, "include","cairo")]
        libpath = [ os.path.join(self.deps_cpp_info[i].rootpath, "lib") 
                    for i in ["glib","gstreamer","libogg","pango","libtheora","libvorbis","zlib","orc","opus",
                              "graphene","libpng","libffi","harfbuzz","freetype","fontconfig","pixman","fribidi","cairo","expat","bzip2"] ]
        meson = Meson(self)
        if self.settings.os == 'Windows':
            with tools.environment_append({
                'PATH' : os.pathsep.join(binpath + [os.getenv('PATH')]),
                "INCLUDE" : os.pathsep.join(include + [os.getenv('INCLUDE')]),
                'LIB' : os.pathsep.join(libpath + [os.getenv('LIB')]),
                }):
                meson.configure(defs=defs,source_dir=self._source_subfolder, build_dir=self._build_subfolder,
                                pkg_config_paths=pkg_config_paths)
                meson.build()
                self.run('ninja -C {0} install'.format(meson.build_dir))

    def package(self):
        self.copy("*", dst=self.package_folder, src=os.path.join(self.build_folder,self._build_subfolder, "install"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

