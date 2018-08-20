from conans import ConanFile, CMake, tools
import os


class RaknetConan(ConanFile):
    name = "raknet"
    version = "4.081"
    license = "BSD License"
    url = "https://github.com/rhard/RakNet"
    description = "RakNet is a cross platform, open source, C++ networking engine for game programmers"
    settings = "os", "compiler", "build_type", "arch"
    options = {"fPIC": [True, False]}
    default_options = "fPIC=True"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/rhard/RakNet.git")
        self.run("cd RakNet && git checkout raklib")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("RakNet/CMakeLists.txt", "project(RakNet)",
                              '''PROJECT(RakNet)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions["RAKNET_ENABLE_DEPENDENT_EXTENTIONS"] = "OFF"
        cmake.definitions["RAKNET_ENABLE_SAMPLES"] = "OFF"
        cmake.definitions["RAKNET_ENABLE_DLL"] = "OFF"
        cmake.definitions["RAKNET_ENABLE_STATIC"] = "ON"
        cmake.definitions["RAKNET_GENERATE_INCLUDE_ONLY_DIR"] = "OFF"
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.configure(source_folder="RakNet")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="RakNet/Source")
        self.copy("*.lib", dst="lib", src="Lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            lib_path = os.path.join(self.package_folder, "lib")
            current_lib = os.path.join(lib_path, "RakNetLibStaticd.lib")
            if os.path.isfile(current_lib):
                os.rename(current_lib, os.path.join(lib_path, "RakNetLibStatic.lib"))

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.libs = ["RakNetLibStatic", "pthread"]
        elif self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["RakNetLibStatic","ws2_32"]
        elif self.settings.os == "Macos":
            self.cpp_info.libs = ["RakNetLibStatic"]
