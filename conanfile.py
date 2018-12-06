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
        deps = ["glib","gstreamer","libogg","pango","libtheora","libvorbis","zlib","orc","opus",
                "graphene","libpng","libffi","harfbuzz","freetype","fontconfig","pixman","fribidi","cairo","expat","bzip2"]
        pkg_config_paths=[ os.path.join(self.deps_cpp_info[i].rootpath, "lib", "pkgconfig") for i in deps ]
        prefix = os.path.join(self.build_folder, self._build_subfolder, "install")
        defs = {'prefix' : prefix, 'disable_introspection':'true'}
        if self.settings.os == "Linux":
            defs.update({'libdir':'lib'})
        binpath=[ os.path.join(self.deps_cpp_info[i].rootpath, "bin") for i in ["glib"] ]
        include = [ os.path.join(self.deps_cpp_info["pango"].rootpath, "include","pango-1.0"),
                    os.path.join(self.deps_cpp_info["cairo"].rootpath, "include","cairo")]
        libpath = [ os.path.join(self.deps_cpp_info[i].rootpath, "lib") for i in deps ]
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
        
        if self.settings.os == 'Linux':
            with tools.environment_append({
                'PATH' : os.pathsep.join(binpath + [os.getenv('PATH')]),
                'LD_LIBRARY_PATH' : os.pathsep.join(libpath),
                }):
                meson.configure(defs=defs,source_dir=self._source_subfolder, build_dir=self._build_subfolder,
                                pkg_config_paths=pkg_config_paths)
                meson.build()
                self.run('ninja -C {0} install'.format(meson.build_dir))

    def package(self):
        self.copy("*", dst=self.package_folder, src=os.path.join(self.build_folder,self._build_subfolder, "install"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

