#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <filesystem>
#include <sstream>

#ifdef _WIN32
#include <windows.h>
#else
#include <mach-o/dyld.h>
#endif

extern char **environ;

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
            std::string locatedFile = appPath + "/Resources/LocatedAppDirectory";
            if (std::filesystem::exists(locatedFile)) {
                std::ifstream file(locatedFile);
                if (file.is_open()) {
                    std::string newAppPath;
                    std::getline(file, newAppPath);
                    file.close();
                    appPath = newAppPath;
                }
            }
        }
    #endif
    return appPath;
}

int launchApp() {
    printMainMessage("Loading OrangeBlox executable!");
    std::string appPath = getAppPath();
    std::string command = "open -n -a \"" + appPath + "/MacOS/OrangeBlox.app/Contents/MacOS/OrangeBlox\"";
    int result = std::system(command.c_str());
    if (result == 0) {
        printSuccessMessage("Bootstrap Launch Success: " + std::to_string(result));
        return 0;
    } else {
        printErrorMessage("Bootstrap Launch Failed: " + std::to_string(result));
        return 1;
    }
}

#ifdef __APPLE__
#import <Cocoa/Cocoa.h>

@interface AppDelegate : NSObject <NSApplicationDelegate>
@end
@implementation AppDelegate
- (void)application:(NSApplication *)application openURLs:(NSArray<NSURL *> *)urls {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0), ^{
        for (NSURL *url in urls) {
            std::string url_scheme;
            if ([url isFileURL]) {
                url_scheme = std::string([[url path] UTF8String]);
            } else {
                url_scheme = std::string([[url absoluteString] UTF8String]);
            }
            std::string app_path = getAppPath();
            std::string url_scheme_path = app_path + "/Resources/URLSchemeExchange";
            std::ofstream file(url_scheme_path);

            if (file.is_open()) {
                file << url_scheme;
                file.close();
                printMainMessage("Created URL Exchange File: " + url_scheme_path);
            }
        }
    });
}
- (void)application:(NSApplication *)sender openFiles:(NSArray<NSString *> *)filenames {
    for (NSString *filePath in filenames) {
        std::string url_scheme = std::string([filePath UTF8String]);
        std::string app_path = getAppPath();
        std::string url_scheme_path = app_path + "/Resources/URLSchemeExchange";
        std::ofstream file(url_scheme_path);

        if (file.is_open()) {
            file << url_scheme;
            file.close();
            printMainMessage("Created URL Exchange File: " + url_scheme_path);
        }
    }
}
- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0), ^{
        launchApp();
        [NSApp terminate:nil];
        exit(0);
    });
}
@end
#endif

int main(int argc, char* argv[]) {
    std::string current_version = "2.2.4";
    std::string main_os;
    std::string app_path;
    
    #ifdef __APPLE__
        main_os = "Darwin";
    #elif _WIN32
        main_os = "Windows";
    #else
        main_os = "Darwin";
    #endif

    printWarnMessage("-----------");
    printWarnMessage("Welcome to OrangeBlox Loader (Play Roblox) 🍊!");
    printWarnMessage("Made by Efaz from efaz.dev!");
    printWarnMessage("v" + current_version);
    printWarnMessage("-----------");
    printMainMessage("Determining System OS...");

    if (main_os == "Darwin") {
        std::string app_path = getAppPath();
        std::string url_scheme_path = app_path + "/Resources/URLSchemeExchange";
        std::ofstream file(url_scheme_path);
        std::string url_scheme;
        if (argc > 1) {
            std::ostringstream oss;
            for (int i = 1; i < argc; ++i) {
                if (i > 1) oss << ' ';
                oss << argv[i];
            }
            url_scheme = "obx-launch-player " + oss.str();
        } else {
            url_scheme = "obx-launch-player orangeblox://continue";
            if (isAppRunningBundled()) {
                char exePath[1024];
                uint32_t size = sizeof(exePath);
                std::string shortcut_app_path;
                if (_NSGetExecutablePath(exePath, &size) == 0) {
                    shortcut_app_path = std::filesystem::path(exePath).parent_path().string();
                } else {
                    printErrorMessage("Buffer size too small for executable path");
                }
                shortcut_app_path = std::filesystem::path(shortcut_app_path).parent_path().string();
                std::string alternative_link_path = shortcut_app_path + "/Resources/AlternativeLink";
                if (std::filesystem::exists(alternative_link_path)) {
                    std::ifstream file(alternative_link_path);
                    if (file.is_open()) {
                        std::string alternative_link;
                        std::getline(file, alternative_link);
                        file.close();
                        url_scheme = alternative_link;
                    }
                }
            }
        }

        if (file.is_open()) {
            file << url_scheme;
            file.close();
            printMainMessage("Created URL Exchange File: " + url_scheme_path);
        }

        @autoreleasepool {
            NSApplication *app = [NSApplication sharedApplication];
            AppDelegate *delegate = [[AppDelegate alloc] init];
            [app setDelegate:delegate];
            [app run];
        }
        return 0;
    } else if (main_os == "Windows") {
        char* localAppData = std::getenv("LOCALAPPDATA");
        if (localAppData) {
            std::string app_path = getAppPath();
            std::string exe_path = app_path + "\\OrangeBlox.exe";
            if (std::filesystem::exists(exe_path)) {
                std::string url_scheme;
                if (argc > 1) {
                    std::ostringstream oss;
                    for (size_t i = 0; i < argc; ++i) {
                        if (i != 0) oss << ' ';
                        oss << argv[i];
                    }
                    url_scheme = oss.str();
                } else {
                    url_scheme = "orangeblox://continue";
                }
                std::string url_scheme_path = app_path + "\\URLSchemeExchange";
                std::ofstream file(url_scheme_path);

                if (file.is_open()) {
                    file << url_scheme;
                    file.close();
                    printMainMessage("Created URL Exchange File: " + url_scheme_path);
                }
                printMainMessage("Loading OrangeBlox.exe!");
                std::string command = "start " + exe_path;
                std::system(command.c_str());
                return 0;
            } else {
                printErrorMessage("Bootstrap Launch Failed: App is not installed.");
                return 1;
            }
        } else {
            printErrorMessage("Local App Data not found.");
            return 1;
        }
    } else {
        printMainMessage("OrangeBlox is only supported for macOS/Windows.");
        std::cin.get();
        return 1;
    }

    return 0;
}