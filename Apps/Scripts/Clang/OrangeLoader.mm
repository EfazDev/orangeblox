#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>
#include <mach-o/dyld.h>
#include <cstdlib>
#include <sstream>
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
    char exePath[1024];
    uint32_t size = sizeof(exePath);
    if (_NSGetExecutablePath(exePath, &size) == 0) {
        std::string path = std::filesystem::path(exePath).string();
        return path.find(".app") != std::string::npos;
    }
    return false;
}

std::string getMainAppPath() {
    std::string appPath;
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
    return appPath;
}

std::string getAppPath() {
    std::string appPath = getMainAppPath();
    if (isAppRunningBundled()) {
        std::string locatedFile = appPath + "/Resources/LocatedAppDirectory";
        if (std::filesystem::exists(locatedFile) && !(std::filesystem::exists(appPath + "/Resources/Main.py"))) {
            std::ifstream file(locatedFile);
            if (file.is_open()) {
                std::string newAppPath;
                std::getline(file, newAppPath);
                file.close();
                appPath = newAppPath;
            }
        }
    }
    return appPath;
}

std::string getNameTxt() {
    std::string nameTxt = "";
    std::string appPath = getMainAppPath();
    if (std::filesystem::exists(appPath + "/Resources/RobloxStudioLauncher")) {
        return "obx-launch-studio";
    } else if (std::filesystem::exists(appPath + "/Resources/RobloxPlayerLauncher")) {
        return "obx-launch-player";
    } else {
        return "";
    }
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
    std::string current_version = "2.4.0c";
    printWarnMessage("-----------");
    printWarnMessage("Welcome to OrangeBlox Loader 🍊!");
    printWarnMessage("Made by Efaz from efaz.dev!");
    printWarnMessage("v" + current_version);
    printWarnMessage("-----------");
    printMainMessage("Determining System OS...");
    std::string app_path = getAppPath();
    std::string url_scheme_path = app_path + "/Resources/URLSchemeExchange";
    std::string url_scheme;
    if (argc > 1) {
        std::ostringstream oss;
        for (int i = 1; i < argc; ++i) {
            if (i > 1) oss << ' ';
            oss << argv[i];
        }
        url_scheme = getNameTxt() + " " + oss.str();
    } else {
        url_scheme = getNameTxt();
        std::string shortcut_app_path = getMainAppPath();
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

    if (!(url_scheme == "")) {
        std::ofstream file(url_scheme_path);
        if (file.is_open()) {
            file << url_scheme;
            file.close();
            printMainMessage("Created URL Exchange File: " + url_scheme_path);
        }
    }
    @autoreleasepool {
        NSApplication *app = [NSApplication sharedApplication];
        AppDelegate *delegate = [[AppDelegate alloc] init];
        [app setDelegate:delegate];
        [app run];
    }
    return 0;
}
