from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.model.version import Version
import os


class GlibcConan(ConanFile):
    name = "glibc"
    description = "The GNU C Library project provides the core libraries for the GNU system and GNU/Linux systems, " \
                  "as well as many other systems that use Linux as the kernel. "
    topics = ("conan", "glibc", "utilities", "toolchain")
    url = "https://github.com/Renari/conan-glibc"
    homepage = "https://www.gnu.org/software/libc/"
    license = "?"
    exports_sources = ["patches/*"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "target": "ANY"}
    default_options = {"shared": False, "fPIC": True, "target": None}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def build_requirements(self):
        self.build_requires("make/4.2.1")

    def requirements(self):
        self.requires("bison/3.7.1")

    def _patch_sources(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        self._patch_sources()
        tools.mkdir(self._build_subfolder)
        condigure_dir = os.path.abspath(os.path.join(self.source_folder, self._source_subfolder))

        with tools.chdir(self._build_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.configure(args=[
                "--disable-werror",
            ], vars={
                "MAKE": self.deps_env_info["make"].CONAN_MAKE_PROGRAM
            }, configure_dir=condigure_dir, target=self.options.target)
            env_build.make()
            env_build.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH env var with : " + bindir)
        self.env_info.PATH.append(bindir)
