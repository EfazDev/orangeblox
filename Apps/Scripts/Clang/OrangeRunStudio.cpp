#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cstdio>
#include <filesystem>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#else
#include <mach-o/dyld.h>
#endif

void printMainMessage(const std::string& mes) {
    std::cout << "\033[38;5;255m" << mes << "\033[0m" << std::endl;
}

void printErrorMessage(const std::string& mes) {
    std::cout << "\033[38;5;196m" << mes << "\033[0m" << std::endl;
}

void printSuccessMessage(const std::string& mes) {
    std::cout << "\033[38;5;82m" << mes << "\033[0m" << std::endl;
}

void printWarnMessage(const std::string& mes) {
    std::cout << "\033[38;5;202m" << mes << "\033[0m" << std::endl;
}

bool isProcessOpened(const std::string& processName) {
    std::string command = "pgrep -f " + processName + " > /dev/null 2>&1";
    int result = system(command.c_str());
    return (result == 0);
}

bool isAppRunningBundled() {
    #ifdef _WIN32
        char executablePath[MAX_PATH];
        GetModuleFileNameA(NULL, executablePath, MAX_PATH);
        std::string path = std::filesystem::path(executablePath).parent_path().string();
        return path.find("AppData\\Local") != std::string::npos;
    #elif __APPLE__
        char exePath[1024];
        uint32_t size = sizeof(exePath);
        if (_NSGetExecutablePath(exePath, &size) == 0) {
            std::string path = std::filesystem::path(exePath).string();
            return path.find(".app") != std::string::npos;
        }
        return false;
    #else
        return false;
    #endif
}

std::string getAppPath() {
    std::string appPath;
    #ifdef _WIN32
        if (isAppRunningBundled()) {
            char executablePath[MAX_PATH];
            GetModuleFileNameA(NULL, executablePath, MAX_PATH);
            appPath = std::filesystem::path(executablePath).parent_path().string();
        }
    #else
        if (isAppRunningBundled()) {
            char exePath[1024];
            uint32_t size = sizeof(exePath);
            if (_NSGetExecutablePath(exePath, &size) == 0) {
                appPath = std::filesystem::path(exePath).parent_path().string();
            } else {
                printErrorMessage("Buffer size too small for executable path");
            }
            appPath = std::filesystem::path(appPath).parent_path().string();
        }
    #endif
    return appPath;
}

int main(int argc, char* argv[]) {
    std::string current_version = "2.0.0";
    std::string main_os;
    std::string app_path;
    
    #ifdef __APPLE__
        main_os = "Darwin";
    #elif _WIN32
        main_os = "Windows";
    #else
        main_os = "Other";
    #endif

    printWarnMessage("-----------");
    printWarnMessage("Welcome to OrangeBlox Loader (Run Studio) 🍊!");
    printWarnMessage("Made by Efaz from efaz.dev!");
    printWarnMessage("v" + current_version);
    printWarnMessage("-----------");
    printMainMessage("Determining System OS...");

    if (main_os == "Darwin") {
        std::string app_path = getAppPath();
        std::string locatedFile = app_path + "/Resources/LocatedAppDirectory";

        if (std::filesystem::exists(locatedFile)) {
            std::ifstream file(locatedFile);
            if (file.is_open()) {
                std::string newAppPath;
                std::getline(file, newAppPath);
                file.close();
                app_path = newAppPath;
            }
        }

        if (std::filesystem::exists(app_path)) {
            std::string url_scheme_path = app_path + "/Resources/URLSchemeExchange";
            std::ofstream file(url_scheme_path);
            if (file.is_open()) {
                file << "orangeblox://run-studio";
                file.close();
            }
            printMainMessage("Created URL Exchange File: " + url_scheme_path);
            if (!isProcessOpened("/System/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal")) {
                printMainMessage("Opening Terminal.app in order for console to show..");
                int result = system("open -j -F -a /System/Applications/Utilities/Terminal.app");
                if (result != 0) {
                    printErrorMessage("Unable to start Terminal.app!");
                }
            }
            printMainMessage("Loading OrangeBlox executable!");
            std::string command = "open -n -a \"" + app_path + "/MacOS/OrangeBlox.app/Contents/MacOS/OrangeBloxMain\"";
            int result = std::system(command.c_str());
            if (result == 0) {
                printSuccessMessage("Bootstrap Run Success: " + std::to_string(result));
                return 0;
            } else {
                printErrorMessage("Bootstrap Run Failed: " + std::to_string(result));
                return 1;
            }
        } else {
            printErrorMessage("Bootstrap Run Failed: App is not installed.");
            return 1;
        }
    } else if (main_os == "Windows") {
        char* localAppData = std::getenv("LOCALAPPDATA");
        if (localAppData) {
            std::string app_path = getAppPath();
            std::string exe_path = app_path + "\\OrangeBlox.exe";
            if (std::filesystem::exists(exe_path)) {
                std::string url_scheme_path = app_path + "\\URLSchemeExchange";
                std::ofstream file(url_scheme_path);
                if (file.is_open()) {
                    file << "orangeblox://run-studio";
                    file.close();
                }
                printMainMessage("Created URL Exchange File: " + url_scheme_path);
                printMainMessage("Loading OrangeBlox.exe!");
                std::string command = "start " + exe_path;
                std::system(command.c_str());
                return 0;
            } else {
                printErrorMessage("Bootstrap Run Failed: App is not installed.");
                return 1;
            }
        } else {
            printErrorMessage("Local app data not found.");
            return 1;
        }
    } else {
        printMainMessage("OrangeBlox is only supported for macOS/Windows.");
        std::cin.get();
        return 1;
    }
    return 0;
}
