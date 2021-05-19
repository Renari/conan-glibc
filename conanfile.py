from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class GlibcConan(ConanFile):
    name = "glibc"
    version = "2.33"
    description = "The GNU C Library project provides the core libraries for the GNU system and GNU/Linux systems, " \
                  "as well as many other systems that use Linux as the kernel. "
    topics = ("conan", "glibc", "utilities", "toolchain")
    url = "https://github.com/Renari/conan-glibc"
    homepage = "https://www.gnu.org/software/libc/"
    license = "?"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "target": "ANY"}
    default_options = {"shared": False, "fPIC": True, "target": None}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def requirements(self):
        self.requires('bison/3.7.1')

    def source(self):
        source_url = "https://ftp.gnu.org/gnu/libc/glibc-%s.tar.bz2" % self.version
        tools.get(source_url, sha256="4d7aa859d9152a4b243821eb604c0f1fee14c10d6341c2b9628d454cddd0f22e")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        tools.mkdir(self._build_subfolder)
        condigure_dir = os.path.abspath(os.path.join(self.source_folder, self._source_subfolder))

        with tools.chdir(self._build_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.configure(args=[
                "--disable-werror"
            ], configure_dir=condigure_dir, target=self.options.target)
            env_build.make()
            env_build.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH env var with : " + bindir)
        self.env_info.PATH.append(bindir)
