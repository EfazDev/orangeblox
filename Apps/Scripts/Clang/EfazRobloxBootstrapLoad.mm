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

bool isProcessOpened(const std::string& processName) {
    std::string command = "pgrep -f " + processName + " > /dev/null 2>&1";
    int result = system(command.c_str());
    return (result == 0);
}

int launchApp() {
    if (!isProcessOpened("/System/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal")) {
        printMainMessage("Opening Terminal.app in order for console to show..");
        int result = system("open -j -F -a /System/Applications/Utilities/Terminal.app");
        if (result != 0) {
            printErrorMessage("Unable to start Terminal.app!");
        }
    }
    printMainMessage("Loading EfazRobloxBootstrap executable!");
    int result = std::system("open -n -a \"/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/MacOS/EfazRobloxBootstrapMain\"");
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
#import <Foundation/Foundation.h>

@interface AppDelegate : NSObject <NSApplicationDelegate>
@end
@implementation AppDelegate
- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0), ^{
        launchApp();
        [NSApp terminate:nil];
    });
}
- (void)application:(NSApplication *)application openURLs:(NSArray<NSURL *> *)urls {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0), ^{
        for (NSURL *url in urls) {
            NSString *urlString = url.absoluteString;
            std::string url_scheme = [urlString UTF8String];
            std::string app_path = "/Applications/EfazRobloxBootstrap.app/";
            std::string url_scheme_path = app_path + "Contents/Resources/URLSchemeExchange";
            std::ofstream file(url_scheme_path);

            if (file.is_open()) {
                file << url_scheme;
                file.close();
                printMainMessage("Created URL Exchange File: " + url_scheme_path);
            }
        }
    });
}
@end
#endif

int main(int argc, char* argv[]) {
    std::string current_version = "1.5.6";
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
        if (argc > 1) {
            std::string url_scheme = argv[1];
            std::string app_path = "/Applications/EfazRobloxBootstrap.app/";
            std::string url_scheme_path = app_path + "Contents/Resources/URLSchemeExchange";
            std::ofstream file(url_scheme_path);

            if (file.is_open()) {
                file << url_scheme;
                file.close();
                printMainMessage("Created URL Exchange File: " + url_scheme_path);
            }
            return launchApp();
        } else {
            @autoreleasepool {
                NSApplication *app = [NSApplication sharedApplication];
                AppDelegate *delegate = [[AppDelegate alloc] init];
                [app setDelegate:delegate];
                [app run];
            }
            return 0;
        }
    } else if (main_os == "Windows") {
        char* localAppData = std::getenv("LOCALAPPDATA");
        if (localAppData) {
            std::string generated_app_path = std::string(localAppData) + "\\EfazRobloxBootstrap";
            std::string exe_path = generated_app_path + "\\EfazRobloxBootstrap.exe";
            if (std::filesystem::exists(exe_path)) {
                if (argc > 1) {
                    std::string url_scheme = argv[1];
                    std::string url_scheme_path = generated_app_path + "\\URLSchemeExchange";
                    std::ofstream file(url_scheme_path);

                    if (file.is_open()) {
                        file << url_scheme;
                        file.close();
                        printMainMessage("Created URL Exchange File: " + url_scheme_path);
                    }
                }
                printMainMessage("Loading EfazRobloxBootstrap.exe!");
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
        printMainMessage("Efaz's Roblox Bootstrap is only supported for macOS/Windows.");
        std::cin.get();
        return 1;
    }

    return 0;
}
