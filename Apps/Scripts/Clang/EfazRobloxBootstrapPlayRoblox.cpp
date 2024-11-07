#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cstdio>
#include <filesystem>
#include <vector>

#ifdef _WIN32
#include <windows.h>
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

int main(int argc, char* argv[]) {
    std::string current_version = "1.3.6";
    std::string main_os;
    
    #ifdef __APPLE__
        main_os = "Darwin";
    #elif _WIN32
        main_os = "Windows";
    #else
        main_os = "Other";
    #endif

    printWarnMessage("-----------");
    printWarnMessage("Welcome to Efaz's Roblox Bootstrap Loader!");
    printWarnMessage("Made by Efaz from efaz.dev!");
    printWarnMessage("v" + current_version);
    printWarnMessage("-----------");
    printMainMessage("Determining System OS...");

    if (main_os == "Darwin") {
        std::string app_path = "/Applications/EfazRobloxBootstrap.app/";
        if (std::filesystem::exists(app_path)) {
            std::string url_scheme_path = app_path + "Contents/Resources/URLSchemeExchange";
            std::ofstream file(url_scheme_path);
            if (file.is_open()) {
                file << "efaz-bootstrap://continue";
                file.close();
            }
            printMainMessage("Created URL Exchange File: " + url_scheme_path);
            printMainMessage("Loading EfazRobloxBootstrap executable!");
            int result = std::system("open -n -a /Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/MacOS/EfazRobloxBootstrapMain");
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
            std::string generated_app_path = std::string(localAppData) + "\\EfazRobloxBootstrap";
            std::string exe_path = generated_app_path + "\\EfazRobloxBootstrap.exe";
            if (std::filesystem::exists(exe_path)) {
                std::string url_scheme_path = generated_app_path + "\\URLSchemeExchange";
                std::ofstream file(url_scheme_path);
                if (file.is_open()) {
                    file << "efaz-bootstrap://continue";
                    file.close();
                }
                printMainMessage("Created URL Exchange File: " + url_scheme_path);
                printMainMessage("Loading EfazRobloxBootstrap.exe!");
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
        printMainMessage("Efaz's Roblox Bootstrap is only supported for macOS/Windows.");
        std::cin.get();
        return 1;
    }
    return 0;
}
