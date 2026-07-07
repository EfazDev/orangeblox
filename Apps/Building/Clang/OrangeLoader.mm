#include <iostream>
#include <cstdlib>
#import <Cocoa/Cocoa.h>

#define print(colorCode, msg) std::cout << "\033[38;5;" << colorCode << "m" << msg << "\033[0m" << std::endl
void printMainMessage(const std::string& mes) { print(255, mes); }
void printErrorMessage(const std::string& mes) { print(196, mes); }
void printSuccessMessage(const std::string& mes) { print(82, mes); }
void printWarnMessage(const std::string& mes) { print(202, mes); }

void writeURLExchange(NSString *targetAppPath, NSString *content) {
    if (content.length == 0) return;
    NSString *exchangePath = [@"~/Library/OrangeBlox/URLLaunchExchange" stringByExpandingTildeInPath];
    [content writeToFile:exchangePath atomically:YES encoding:NSUTF8StringEncoding error:nil];
    printMainMessage("Created URL Exchange File: " + std::string([exchangePath UTF8String]));
}

NSString* getTargetAppPath(NSString *resourcePath) {
    NSFileManager *fm = [NSFileManager defaultManager];
    NSString *mainPyPath = [resourcePath stringByAppendingPathComponent:@"Main.py"];
    NSString *locatedFilePath = [resourcePath stringByAppendingPathComponent:@"LocatedAppDirectory"];

    if (![fm fileExistsAtPath:mainPyPath] && [fm fileExistsAtPath:locatedFilePath]) {
        NSString *newPath = [NSString stringWithContentsOfFile:locatedFilePath encoding:NSUTF8StringEncoding error:nil];
        if (newPath) { return [newPath stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]]; }
    }
    return [resourcePath stringByDeletingLastPathComponent];
}

@interface AppDelegate : NSObject <NSApplicationDelegate>
@property (nonatomic, strong) NSString *targetAppPath;
@end
@implementation AppDelegate
- (void)application:(NSApplication *)application openURLs:(NSArray<NSURL *> *)urls {
    for (NSURL *url in urls) {
        NSString *scheme = url.isFileURL ? url.path : url.absoluteString;
        writeURLExchange(self.targetAppPath, scheme);
    }
}
- (void)application:(NSApplication *)sender openFiles:(NSArray<NSString *> *)filenames {
    for (NSString *filePath in filenames) {
        writeURLExchange(self.targetAppPath, filePath);
    }
}
- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0), ^{
        printMainMessage("Launching OrangeBlox App..");
        NSString *appBundlePath = [self.targetAppPath stringByDeletingLastPathComponent];
        NSString *command = [NSString stringWithFormat:@"/usr/bin/open -n -a \"%@\"", appBundlePath];
        int result = std::system([command UTF8String]);
        if (result == 0) {
            printSuccessMessage("OrangeBlox Launch Success: 0");
        } else {
            printErrorMessage("OrangeBlox Launch Failed: " + std::to_string(result));
        }
        dispatch_async(dispatch_get_main_queue(), ^{
            exit(0);
        });
    });
}
@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        printWarnMessage("-----------");
        printWarnMessage("Welcome to OrangeBlox Loader 🍊!");
        printWarnMessage("Made by Efaz from efaz.dev!");
        printWarnMessage("v2.6.0d");
        printWarnMessage("-----------");
        printMainMessage("Determining System Paths...");
        NSFileManager *fm = [NSFileManager defaultManager];
        NSString *resourcePath = [[NSBundle mainBundle] resourcePath];
        NSString *targetAppPath = getTargetAppPath(resourcePath);
        NSString *urlScheme = @"";
        if ([fm fileExistsAtPath:[resourcePath stringByAppendingPathComponent:@"RobloxStudioLauncher"]]) {
            urlScheme = @"obx-launch-studio";
        } else if ([fm fileExistsAtPath:[resourcePath stringByAppendingPathComponent:@"RobloxPlayerLauncher"]]) {
            urlScheme = @"obx-launch-player";
        }
        if (argc > 1) {
            NSMutableArray *argsArray = [NSMutableArray array];
            for (int i = 1; i < argc; ++i) {
                [argsArray addObject:[NSString stringWithUTF8String:argv[i]]];
            }
            NSString *argsStr = [argsArray componentsJoinedByString:@" "];
            urlScheme = [NSString stringWithFormat:@"%@ %@", urlScheme, argsStr];
        } else if (urlScheme.length == 0) {
            NSString *altLinkPath = [resourcePath stringByAppendingPathComponent:@"AlternativeLink"];
            if ([fm fileExistsAtPath:altLinkPath]) {
                urlScheme = [NSString stringWithContentsOfFile:altLinkPath encoding:NSUTF8StringEncoding error:nil];
                urlScheme = [urlScheme stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
            }
        }
        writeURLExchange(targetAppPath, urlScheme);
        NSApplication *app = [NSApplication sharedApplication];
        AppDelegate *delegate = [[AppDelegate alloc] init];
        delegate.targetAppPath = targetAppPath;
        [app setDelegate:delegate];
        [app run];
    }
    return 0;
}