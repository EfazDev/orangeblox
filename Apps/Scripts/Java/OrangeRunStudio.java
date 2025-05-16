package Apps.Scripts.Java;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class OrangeRunStudio {
    public static String current_version = "2.0.1";
    public static String main_os = "Windows";
    public static void main(String[] args) throws IOException {
        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            main_os = "Windows";
        } else if (System.getProperty("os.name").toLowerCase().contains("mac")) {
            main_os = "Darwin";
        } else {
            main_os = "Linux";
        }

        printWarnMessage("-----------");
        printWarnMessage("Welcome to OrangeBlox Loader 🍊!");
        printWarnMessage("Made by Efaz from efaz.dev!");
        printWarnMessage("v" + current_version);
        printWarnMessage("-----------");
        printMainMessage("Determining System OS...");
        if (main_os == "Windows") {
            String local_app_data = System.getenv("LOCALAPPDATA");
            if (!(local_app_data == "") && exists(local_app_data)) {
                final String bootstrap_location = getAppPath();
                if (exists(bootstrap_location)) {
                    // Write URLSchemeExchange File
                    final String file_path = bootstrap_location + "\\URLSchemeExchange";
                    final FileWriter file_writer = new FileWriter(file_path);
                    file_writer.write("orangeblox://run-studio");
                    file_writer.close();
                    printMainMessage("Created URL Exchange File: " + file_path);

                    // Start Bootstrap
                    ProcessBuilder process_builder = new ProcessBuilder("start", bootstrap_location + "\\OrangeBlox.exe");
                    printMainMessage("Loading OrangeBlox executable!");
                    process_builder.start();
                }
            }
        } else if (main_os == "Darwin") {
            String app_location = getAppPath();
            if (exists(app_location)) {
                // Write URLSchemeExchange File
                String file_path = app_location + "/Resources/URLSchemeExchange";
                FileWriter file_writer = new FileWriter(file_path);
                file_writer.write("orangeblox://run-studio");
                file_writer.close();
                printMainMessage("Created URL Exchange File: " + file_path);

                // Start Bootstrap
                String executable_command = "open -n -a \"" + app_location + "/MacOS/OrangeBlox.app/\"";
                ProcessBuilder process_builder = new ProcessBuilder("bash", "-c", executable_command);
                printMainMessage("Loading OrangeBlox executable!");
                process_builder.start();
            }
        }
    }

    private static String ascii_escape = "\033";
    public static void printMainMessage(String mes) {
        System.out.println(ascii_escape + "[38;5;255m" + mes + ascii_escape + "[0m");
    }
    public static void printErrorMessage(String mes) {
        System.out.println(ascii_escape + "[38;5;196m" + mes + ascii_escape + "[0m");
    }
    public static void printSuccessMessage(String mes) {
        System.out.println(ascii_escape + "[38;5;82m" + mes + ascii_escape + "[0m");
    }
    public static void printWarnMessage(String mes) {
        System.out.println(ascii_escape + "[38;5;202m" + mes + ascii_escape + "[0m");
    }
    public static String getAppPath() {
        File located_app = new File("../LocatedAppDirectory");
        if (located_app.exists()) {
            try (BufferedReader reader = new BufferedReader(new FileReader(located_app))) {
                String line = reader.readLine();
                if (line != null) {
                    return line;
                } else {
                    printErrorMessage("File is empty.");
                }
            } catch (IOException e) {
                printErrorMessage("Error reading located app path!");
            }
        }
        return "";
    }
    public static boolean exists(String path) {
        final File FileObject = new File(path);
        if (FileObject.exists()) {
            return true;
        } else {
            return false;
        }
    }
}