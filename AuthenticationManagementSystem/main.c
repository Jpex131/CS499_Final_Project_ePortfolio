#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bcrypt.h"  // Include the bcrypt library for password hashing

// Function to initialize the database and create the USERS table if it doesn't exist
void initializeDatabase() {
    sqlite3 *db;         // Pointer to SQLite database
    char *errMsg = 0;    // Pointer to an error message
    int rc;              // Integer to store the return code of SQLite functions

    // Attempt to open the database file, create if it doesn't exist
    rc = sqlite3_open("userDatabase.db", &db);
    if (rc) {
        // If opening the database fails, print the error and return
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return;
    } else {
        fprintf(stderr, "Opened database successfully\n");
    }

    // SQL statement to create the USERS table
    char *sql = "CREATE TABLE IF NOT EXISTS USERS("  \
                "USERNAME TEXT PRIMARY KEY NOT NULL," \
                "PASSWORD TEXT NOT NULL," \
                "ROLE     TEXT NOT NULL);";

    // Execute the SQL statement to create the table
    rc = sqlite3_exec(db, sql, 0, 0, &errMsg);
    if (rc != SQLITE_OK) {
        // If SQL execution fails, print the error message
        fprintf(stderr, "SQL error: %s\n", errMsg);
        sqlite3_free(errMsg);
    } else {
        fprintf(stdout, "Table created successfully\n");
    }
    // Close the database connection
    sqlite3_close(db);
}

// Struct to represent a User
typedef struct {
    char username[50];   // User's username
    char password[60];   // User's hashed password
    char userType[15];   // User's type (e.g., Admin, Zookeeper, Veterinarian)
} User;

// Function Declarations
void registerUser();   // Function to register a new user
void loginUser();      // Function to log in a user
void readUserFile(char* userType); // Function to read user-specific file
void logout();         // Function to handle user logout

// Global array to store user data (for demonstration purposes)
User users[100];
int userCount = 0;     // Counter for the number of users

int main() {
    sqlite3 *db;       // Pointer to SQLite database
    sqlite3_open("userDatabase.db", &db); // Open the database

    initializeDatabase(); // Initialize the database and create table if necessary

    int choice;        // Variable to store the user's menu choice
    while (1) {
        // Display the menu and get user's choice
        printf("1. Register\n2. Login\n3. Exit\nEnter your choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                registerUser(); // Register a new user
                break;
            case 2:
                loginUser();    // Login an existing user
                break;
            case 3:
                exit(0);        // Exit the program
            default:
                printf("Invalid choice\n"); // Handle invalid choices
        }
    }

    // Close the database connection before exiting
    sqlite3_close(db);
    return 0;
}

void registerUser(sqlite3 *db, const char *username, const char *plainPassword, const char *role) {
    char hashedPassword[60];  // Array to store the hashed password
    char sql[200];            // SQL query string
    char *errMsg = 0;         // Pointer to an error message
    int rc;                   // Return code of SQLite functions

    // Hash the plain text password with BCrypt
    char salt[BCRYPT_HASHSIZE];
    bcrypt_gensalt(12, salt);
    bcrypt_hashpw(plainPassword, salt, hashedPassword);

    // Prepare SQL query to insert the new user into the USERS table
    sprintf(sql, "INSERT INTO USERS (USERNAME,PASSWORD,ROLE) VALUES ('%s', '%s', '%s');", username, hashedPassword, role);

    // Execute the SQL query to insert the user
    rc = sqlite3_exec(db, sql, 0, 0, &errMsg);
    if (rc != SQLITE_OK) {
        // If the query execution fails, print the error message
        fprintf(stderr, "SQL error: %s\n", errMsg);
        sqlite3_free(errMsg);
    } else {
        fprintf(stdout, "User registered successfully\n");
    }
}

void loginUser() {
    char username[50], plainPassword[50], hashedPassword[60]; // Variables to store username and passwords

    // Prompt user for username and password
    printf("Enter username: ");
    scanf("%s", username);
    printf("Enter password: ");
    scanf("%s", plainPassword);

    // Iterate through the array of users to find a match
    for (int i = 0; i < userCount; i++) {
        if (strcmp(users[i].username, username) == 0) {
            // If username is found, hash the entered password and compare
            bcrypt_hashpw(plainPassword, users[i].password, hashedPassword);
            if (strcmp(hashedPassword, users[i].password) == 0) {
                printf("Login successful.\n");
                readUserFile(users[i].userType); // Read the user-specific file
                logout();                        // Logout the user
                return;
            } else {
                printf("Invalid password.\n");   // Password does not match
                return;
            }
        }
    }
    printf("User not found.\n");                // Username not found
}

void readUserFile(char* userType) {
    // Read and process the file based on the user's type
    printf("Reading file for %s...\n", userType);
    // Implement the file reading logic here
}

void logout() {
    // Handle the logout process
    printf("Logged out.\n");
}
