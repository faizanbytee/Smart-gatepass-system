package com.niet.gatepass.config;

import com.niet.gatepass.model.Role;
import com.niet.gatepass.model.User;
import com.niet.gatepass.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private UserRepository userRepository;

    @Override
    public void run(String... args) throws Exception {
        if (userRepository.count() == 0) {
            // Seed Admin User
            User admin = new User(
                    null,
                    "admin",
                    "admin123",
                    "System Admin",
                    Role.ADMIN,
                    "admin@niet.co.in",
                    "9999999999",
                    null, null, null, null, null
            );
            userRepository.save(admin);

            // Seed Warden User
            User warden = new User(
                    null,
                    "warden1",
                    "warden123",
                    "Dr. K.P. Singh (Warden)",
                    Role.WARDEN,
                    "warden.kp@niet.co.in",
                    "8888888888",
                    null, null, null, null, null
            );
            userRepository.save(warden);

            // Seed Guard User
            User guard = new User(
                    null,
                    "guard1",
                    "guard123",
                    "Ramesh Kumar (Guard)",
                    Role.GUARD,
                    "guard1@niet.co.in",
                    "7777777777",
                    null, null, null, null, null
            );
            userRepository.save(guard);

            // Seed Students
            User student1 = new User(
                    null,
                    "2501330109001",
                    "student123",
                    "Amit Kumar",
                    Role.STUDENT,
                    "amit.cse@niet.co.in",
                    "9876543210",
                    "Raman Hostel",
                    "302",
                    "CSE",
                    "3rd Year",
                    "9876543211"
            );
            userRepository.save(student1);

            User student2 = new User(
                    null,
                    "2501330109002",
                    "student123",
                    "Priya Sharma",
                    Role.STUDENT,
                    "priya.it@niet.co.in",
                    "8765432109",
                    "Kalpana Girls Hostel",
                    "105",
                    "IT",
                    "2nd Year",
                    "8765432100"
            );
            userRepository.save(student2);

            User student3 = new User(
                    null,
                    "2501330109003",
                    "student123",
                    "Rohan Verma",
                    Role.STUDENT,
                    "rohan.ece@niet.co.in",
                    "9812345678",
                    "Tagore Hostel",
                    "412",
                    "ECE",
                    "4th Year",
                    "9812345670"
            );
            userRepository.save(student3);

            User student4 = new User(
                    null,
                    "2501330109004",
                    "student123",
                    "Sneha Gupta",
                    Role.STUDENT,
                    "sneha.cse@niet.co.in",
                    "9723456789",
                    "Kalpana Girls Hostel",
                    "204",
                    "CSE",
                    "3rd Year",
                    "9723456780"
            );
            userRepository.save(student4);

            User student5 = new User(
                    null,
                    "2501330109005",
                    "student123",
                    "Vikram Singh",
                    Role.STUDENT,
                    "vikram.me@niet.co.in",
                    "9634567890",
                    "Raman Hostel",
                    "118",
                    "ME",
                    "2nd Year",
                    "9634567899"
            );
            userRepository.save(student5);

            User student6 = new User(
                    null,
                    "2501330109006",
                    "student123",
                    "Ananya Roy",
                    Role.STUDENT,
                    "ananya.aiml@niet.co.in",
                    "9545678901",
                    "Sarojini Girls Hostel",
                    "301",
                    "AI & ML",
                    "1st Year",
                    "9545678900"
            );
            userRepository.save(student6);

            User student7 = new User(
                    null,
                    "2501330109007",
                    "student123",
                    "Rahul Mishra",
                    Role.STUDENT,
                    "rahul.cse@niet.co.in",
                    "9456789012",
                    "Bhabha Hostel",
                    "220",
                    "CSE",
                    "4th Year",
                    "9456789010"
            );
            userRepository.save(student7);

            System.out.println("--- DB SEEDING COMPLETED SUCCESSFULY ---");
        }
    }
}
