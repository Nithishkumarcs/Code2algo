using System;

class Program {
    static void Main() {
        int score = 85;
        char grade;
        if (score >= 90) grade = 'A';
        else if (score >= 80) grade = 'B';
        else if (score >= 70) grade = 'C';
        else if (score >= 60) grade = 'D';
        else grade = 'F';
        Console.WriteLine("Student Grade: " + grade);
    }
}
