<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - NIET GatePass</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
    <script>
        function toggleStudentFields() {
            var role = document.getElementById("roleSelect").value;
            var studentSection = document.getElementById("studentFieldsSection");
            var studentInputs = studentSection.querySelectorAll("input");
            
            if (role === "STUDENT") {
                studentSection.style.display = "block";
                studentInputs.forEach(function(input) {
                    input.required = true;
                });
            } else {
                studentSection.style.display = "none";
                studentInputs.forEach(function(input) {
                    input.required = false;
                    input.value = "";
                });
            }
        }
    </script>
</head>
<body>
    <div class="app-container">
        <!-- Navigation -->
        <nav class="navbar">
            <div class="brand">
                NIET <span>GatePass</span>
            </div>
            <div class="nav-user">
                <span class="user-badge">${sessionScope.user.name} (Admin)</span>
                <a href="${pageContext.request.contextPath}/logout" class="logout-btn">Logout</a>
            </div>
        </nav>

        <!-- Message Alerts -->
        <c:if test="${not empty param.success}">
            <div class="alert alert-success">
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>${param.success}</span>
            </div>
        </c:if>
        <c:if test="${not empty param.error}">
            <div class="alert alert-danger">
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
                <span>${param.error}</span>
            </div>
        </c:if>

        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card primary">
                <span class="stat-title">Total Registered Users</span>
                <span class="stat-value">${totalUsers}</span>
            </div>
            <div class="stat-card success">
                <span class="stat-title">Students</span>
                <span class="stat-value">${studentCount}</span>
            </div>
            <div class="stat-card warning">
                <span class="stat-title">Wardens</span>
                <span class="stat-value">${wardenCount}</span>
            </div>
            <div class="stat-card danger">
                <span class="stat-title">Security Guards</span>
                <span class="stat-value">${guardCount}</span>
            </div>
        </div>

        <div class="dashboard-grid">
            <!-- Left Side: User Directory -->
            <div class="glass-card">
                <h3 style="margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">User Directory</h3>
                
                <div class="table-container">
                    <table class="custom-table">
                        <thead>
                            <tr>
                                <th>Name / Username</th>
                                <th>Role</th>
                                <th>Contact Info</th>
                                <th>Hostel/Room (Students)</th>
                                <th style="text-align: center;">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <c:forEach var="usr" items="${users}">
                                <tr>
                                    <td>
                                        <div style="font-weight: 600;">${usr.name}</div>
                                        <div style="font-size: 0.8rem; color: var(--text-secondary);">${usr.username}</div>
                                    </td>
                                    <td>
                                        <span class="badge badge-<c:choose><c:when test="${usr.role == 'STUDENT'}">approved</c:when><c:when test="${usr.role == 'WARDEN'}">warning</c:when><c:when test="${usr.role == 'GUARD'}">out</c:when><c:otherwise>pending</c:otherwise></c:choose>">
                                            ${usr.role}
                                        </span>
                                    </td>
                                    <td>
                                        <div>${usr.email}</div>
                                        <div style="font-size: 0.8rem; color: var(--text-secondary);">M: ${usr.mobile}</div>
                                    </td>
                                    <td>
                                        <c:choose>
                                            <c:when test="${usr.role == 'STUDENT'}">
                                                <div>Room ${usr.roomNo} (${usr.branch})</div>
                                                <div style="font-size: 0.8rem; color: var(--text-secondary);">${usr.hostelName}</div>
                                            </c:when>
                                            <c:otherwise>
                                                <span style="color: var(--text-muted);">-</span>
                                            </c:otherwise>
                                        </c:choose>
                                    </td>
                                    <td style="text-align: center;">
                                        <c:choose>
                                            <c:when test="${usr.username == sessionScope.user.username}">
                                                <span style="color: var(--text-muted); font-size: 0.85rem; font-style: italic;">Active Self</span>
                                            </c:when>
                                            <c:otherwise>
                                                <form action="${pageContext.request.contextPath}/admin/user/delete" method="POST" onsubmit="return confirm('Are you sure you want to delete ${usr.name}?');" class="inline-form">
                                                    <input type="hidden" name="userId" value="${usr.id}">
                                                    <button type="submit" class="btn btn-danger" style="padding: 0.35rem 0.7rem; font-size: 0.8rem;">Delete</button>
                                                </form>
                                            </c:otherwise>
                                        </c:choose>
                                    </td>
                                </tr>
                            </c:forEach>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Right Side: Add User Form -->
            <div class="glass-card" style="height: fit-content;">
                <h3 style="margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Add New System User</h3>
                
                <form action="${pageContext.request.contextPath}/admin/user/add" method="POST">
                    <div class="form-group">
                        <label class="form-label" for="username">Username / Roll Number</label>
                        <input type="text" id="username" name="username" class="form-control" placeholder="e.g. roll number or name ID" required autocomplete="off">
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="password">Password</label>
                        <input type="password" id="password" name="password" class="form-control" placeholder="Create login password" required>
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="name">Full Name</label>
                        <input type="text" id="name" name="name" class="form-control" placeholder="Enter full name" required autocomplete="off">
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="roleSelect">User Role</label>
                        <select id="roleSelect" name="role" class="form-control" onchange="toggleStudentFields()" required>
                            <option value="STUDENT">Student</option>
                            <option value="WARDEN">Hostel Warden</option>
                            <option value="GUARD">Security Guard</option>
                            <option value="ADMIN">System Admin</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="email">Email Address</label>
                        <input type="email" id="email" name="email" class="form-control" placeholder="e.g. user@niet.co.in" required autocomplete="off">
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="mobile">Mobile Number</label>
                        <input type="tel" id="mobile" name="mobile" class="form-control" placeholder="10-digit mobile number" required autocomplete="off">
                    </div>

                    <!-- Student Specific Section (Shown by default since STUDENT is first select option) -->
                    <div id="studentFieldsSection">
                        <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; border-top: 1px solid var(--border-color); padding-top: 1rem; color: var(--primary);">Student Details</h4>
                        
                        <div class="form-group">
                            <label class="form-label" for="hostelName">Hostel Name</label>
                            <input type="text" id="hostelName" name="hostelName" class="form-control" placeholder="e.g. Raman Hostel" required autocomplete="off">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="roomNo">Room Number</label>
                            <input type="text" id="roomNo" name="roomNo" class="form-control" placeholder="e.g. 102" required autocomplete="off">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="branch">Branch</label>
                            <input type="text" id="branch" name="branch" class="form-control" placeholder="e.g. CSE / IT / ECE" required autocomplete="off">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="year">Year</label>
                            <input type="text" id="year" name="year" class="form-control" placeholder="e.g. 3rd Year" required autocomplete="off">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="parentMobile">Parent Contact Number</label>
                            <input type="tel" id="parentMobile" name="parentMobile" class="form-control" placeholder="10-digit parent contact" required autocomplete="off">
                        </div>
                    </div>

                    <button type="submit" class="btn btn-primary btn-block" style="margin-top: 1.5rem;">Register User</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
