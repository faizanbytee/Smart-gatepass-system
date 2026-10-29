# Smart Gate Pass Approval System in NIET Hostel

[![Java](https://img.shields.io/badge/Java-21%20%2F%2024-orange.svg)](https://www.oracle.com/java/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.3.1-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Hibernate](https://img.shields.io/badge/Hibernate-JPA-blue.svg)](https://hibernate.org/)
[![Database](https://img.shields.io/badge/Database-MySQL%20%2F%20H2-blue.svg)](https://www.mysql.com/)

An enterprise-grade Java web application designed to digitize, automate, and secure the process of student gate pass issuance, warden reviews, and security gate boundary tracking at **Noida Institute of Engineering & Technology (NIET)** hostels.

---

## 📌 Project Overview

Historically, hostel gate passes have been managed using manual paper registers, hand-written slips, and physical signatures. This manual system suffers from signature forgery, administrative bottlenecks, illegible records, and a lack of real-time visibility into student movement.

The **Smart Gate Pass Approval System** replaces physical outpass slips with a centralized, role-based web application that connects **Students**, **Hostel Wardens**, **Security Guards**, and **Administrators** in real time.

---

## 🚀 Key Features

### 1. 🎓 Student Portal
- Secure login using unique university Roll Number.
- Apply for gate passes:
  - **Local Outing** (Hours-based, same day)
  - **Home Leave** (Days-based, overnight)
- Automated departure & return date-time validation.
- Live status tracking (**PENDING**, **APPROVED**, **REJECTED**, **OUT**, **RETURNED**).
- Personal student profile view with hostel room and contact details.

### 2. 🏛️ Hostel Warden Dashboard
- Live queue of pending gate pass requests with student details and destination.
- Single-click **Approve** or **Reject** actions with mandatory remarks.
- Processed passes history log with audit trails.
- Real-time statistics: Pending approvals, currently checked-out students, and total processed.

### 3. 🛡️ Security Guard Checkpoint
- Quick lookup search bar by student **Roll Number**.
- Digital verification of warden approval status.
- One-click **Log Checkout (Exit)** recording exact departure timestamp.
- One-click **Log Checkin (Return)** recording exact return timestamp.
- Live dashboard monitor showing all students currently outside hostel premises.
- History log of recently returned students.

### 4. ⚙️ Administrator Console
- Centralized user management directory (Students, Wardens, Guards, Admins).
- Add new users with dynamic role-based form validation.
- Delete or manage system user access.
- System analytics and user breakdown statistics.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Spring Boot 3.3.1 |
| **Language Platform** | Java 21 / Java 24 (compiling to release 21) |
| **Persistence / ORM** | Spring Data JPA / Hibernate ORM |
| **Database** | MySQL 8.0 (Production) / H2 In-Memory (Dev & Testing) |
| **View Engine** | JavaServer Pages (JSP) + JSTL Standard Tags |
| **Embedded Server** | Apache Tomcat 10.1 (Pre-configured inside Spring Boot) |
| **Build Tool** | Gradle Wrapper 9.5 |
| **Styling & UI** | Custom Responsive CSS (Glassmorphism Dark Theme) |
| **Security** | Session-based `AuthInterceptor` route guard |

---

## 🔐 Default Demo Accounts (Pre-Seeded)

The database automatically seeds with default accounts on startup for instant evaluation:

| Role | Username / ID | Password | Name | Details |
| :--- | :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | System Admin | System Administrator |
| **Warden** | `warden1` | `warden123` | Dr. K.P. Singh | Hostel Warden |
| **Security Guard** | `guard1` | `guard123` | Ramesh Kumar | Main Gate Guard |
| **Student 1** | `2501330109001` | `student123` | Amit Kumar | Raman Hostel (Room 302, CSE) |
| **Student 2** | `2501330109002` | `student123` | Priya Sharma | Kalpana Girls Hostel (Room 105, IT) |
| **Student 3** | `2501330109003` | `student123` | Rohan Verma | Tagore Hostel (Room 412, ECE) |
| **Student 4** | `2501330109004` | `student123` | Sneha Gupta | Kalpana Girls Hostel (Room 204, CSE) |
| **Student 5** | `2501330109005` | `student123` | Vikram Singh | Raman Hostel (Room 118, ME) |
| **Student 6** | `2501330109006` | `student123` | Ananya Roy | Sarojini Girls Hostel (Room 301, AI & ML) |
| **Student 7** | `2501330109007` | `student123` | Rahul Mishra | Bhabha Hostel (Room 220, CSE) |

---

## 🏃 How to Run the Project

### Prerequisites
- **JDK 21** or newer installed.
- (Optional) **MySQL 8.0** if running in production mode.

### Steps:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
   cd <YOUR-REPO-NAME>
   ```

2. **Run using Gradle Wrapper:**
   ```powershell
   .\gradlew bootRun --no-daemon
   ```

3. **Open the Web Browser:**
   Navigate to:
   ```
   http://localhost:8080/
   ```

4. **Sign in** with any of the demo credentials above!

---

## 📁 Project Directory Structure

```
smart-gatepass-system/
├── src/
│   ├── main/
│   │   ├── java/com/niet/gatepass/
│   │   │   ├── config/             # AuthInterceptor, WebMvcConfig, DataInitializer
│   │   │   ├── controller/         # Login, Student, Warden, Guard, Admin controllers
│   │   │   ├── model/              # User, GatePass, Role, PassStatus entities
│   │   │   └── repository/         # UserRepository, GatePassRepository
│   │   ├── resources/
│   │   │   ├── static/css/         # Glassmorphic style.css
│   │   │   └── application.properties # H2 & MySQL database configurations
│   │   └── webapp/WEB-INF/jsp/     # JSP View Templates
│   │       ├── login.jsp
│   │       ├── student/            # dashboard.jsp, request.jsp
│   │       ├── warden/             # dashboard.jsp
│   │       ├── guard/              # dashboard.jsp
│   │       └── admin/              # dashboard.jsp
│   └── test/                       # Spring Boot context load integration tests
├── build.gradle                    # Gradle dependencies & compilation tasks
├── settings.gradle
└── README.md
```

---

## 👤 Author
- **Faizan Ahmad** (Roll No: `0251dcs458` / `2501330109004`)
- Department of Computer Science & Engineering
- Noida Institute of Engineering & Technology (NIET), Greater Noida
