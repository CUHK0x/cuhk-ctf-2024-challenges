import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Scanner;  
//import java.util.Locale;  


class IndonesianCulture {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Date date = new Date();
        SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy");  
        String strDate = formatter.format(date);  

        System.out.print("Enter the password: ");
        String userInput = scanner.nextLine();

        String check = "p3n9uinIsAw3s0ne" + strDate;
        //System.out.println("Enter a string: ");
        scanner.close();
        if (userInput.equals(check)) {
            System.out.println("The input is correct!");
            readFlagFromFile();
        } else {
            System.out.println("The input is incorrect.");
        }
    }

    private static void readFlagFromFile() {
        try {
            BufferedReader reader = new BufferedReader(new FileReader("03_flag.txt"));
            String flag = reader.readLine();
            System.out.println("Flag: " + flag);
            reader.close();
        } catch (IOException e) {
            System.out.println("Error reading flag from file: " + e.getMessage());
            System.out.println("If you encountered this message when running your code on the competition server, contact challenge author p3n9uin immediately by opening a ticket on the competition Discord server.");
        }
    }
}
