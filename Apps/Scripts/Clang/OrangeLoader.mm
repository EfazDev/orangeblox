#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>
#include <mach-o/dyld.h>
#import <Cocoa/Cocoa.h>

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

int main(int argc, char* argv[]) {
    std::string current_version = "2.2.7";
    printWarnMessage("-----------");
    printWarnMessage("Welcome to OrangeBlox Loader 🍊!");
    printWarnMessage("Made by Efaz from efaz.dev!");
    printWarnMessage("v" + current_version);
    printWarnMessage("-----------");
    printMainMessage("Determining System OS...");
    @autoreleasepool {
        NSApplication *app = [NSApplication sharedApplication];
        AppDelegate *delegate = [[AppDelegate alloc] init];
        [app setDelegate:delegate];
        [app run];
    }
    return 0;
}
