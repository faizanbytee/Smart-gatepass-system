<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Dashboard - NIET GatePass</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <div class="app-container">
        <!-- Navigation -->
        <nav class="navbar">
            <div class="brand">
                NIET <span>GatePass</span>
            </div>
            <div class="nav-user">
                <span class="user-badge">${sessionScope.user.name} (Student)</span>
                <a href="${pageContext.request.contextPath}/logout" class="logout-btn">Logout</a>
            </div>
        </nav>

        <!-- Messages -->
        <c:if test="${not empty param.success}">
            <div class="alert alert-success">
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>${param.success}</span>
            </div>
        </c:if>

        <div class="dashboard-grid">
            <!-- Main Content Area -->
            <div>
                <!-- Statistics -->
                <div class="stats-grid">
                    <div class="stat-card primary">
                        <span class="stat-title">Total Applications</span>
                        <span class="stat-value">${myPasses.size()}</span>
                    </div>
                    <div class="stat-card warning">
                        <span class="stat-title">Pending</span>
                        <span class="stat-value">${pendingCount}</span>
                    </div>
                    <div class="stat-card success">
                        <span class="stat-title">Approved</span>
                        <span class="stat-value">${approvedCount}</span>
                    </div>
                    <div class="stat-card danger">
                        <span class="stat-title">Currently Out</span>
                        <span class="stat-value">${outCount}</span>
                    </div>
                </div>

                <!-- My Applications -->
                <div class="glass-card">
                    <div class="panel-header">
                        <h3>My Gate Pass History</h3>
                        <a href="${pageContext.request.contextPath}/student/request" class="btn btn-primary">+ New Request</a>
                    </div>
                    
                    <c:choose>
                        <c:when test="${empty myPasses}">
                            <p style="color: var(--text-secondary); text-align: center; padding: 2rem 0;">No gate pass requests found. Click 'New Request' to apply.</p>
                        </c:when>
                        <c:otherwise>
                            <div class="table-container">
                                <table class="custom-table">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Type</th>
                                            <th>Purpose</th>
                                            <th>Destination</th>
                                            <th>Departure</th>
                                            <th>Exp. Return</th>
                                            <th>Status</th>
                                            <th>Remarks</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <c:forEach var="pass" items="${myPasses}">
                                            <tr>
                                                <td>#GP-${pass.id}</td>
                                                <td>
                                                    <span style="font-weight: 500;">${pass.passType}</span>
                                                </td>
                                                <td>${pass.purpose}</td>
                                                <td>${pass.destination}</td>
                                                <td>
                                                    <fmt:parseDate value="${pass.departureDateTime}" pattern="yyyy-MM-dd'T'HH:mm" var="parsedDep" type="both"/>
                                                    <fmt:formatDate value="${parsedDep}" pattern="dd MMM yyyy, hh:mm a"/>
                                                </td>
                                                <td>
                                                    <fmt:parseDate value="${pass.expectedReturnDateTime}" pattern="yyyy-MM-dd'T'HH:mm" var="parsedRet" type="both"/>
                                                    <fmt:formatDate value="${parsedRet}" pattern="dd MMM yyyy, hh:mm a"/>
                                                </td>
                                                <td>
                                                    <span class="badge badge-${pass.status.toString().toLowerCase()}">${pass.status}</span>
                                                </td>
                                                <td>
                                                    <c:choose>
                                                        <c:when test="${not empty pass.remarks}">
                                                            <span style="font-style: italic; color: var(--text-secondary);">${pass.remarks}</span>
                                                        </c:when>
                                                        <c:otherwise>
                                                            <span style="color: var(--text-muted);">-</span>
                                                        </c:otherwise>
                                                    </c:choose>
                                                </td>
                                            </tr>
                                        </c:forEach>
                                    </tbody>
                                </table>
                            </div>
                        </c:otherwise>
                    </c:choose>
                </div>
            </div>

            <!-- Profile Info Sidebar -->
            <div class="dashboard-sidebar-grid">
                <div class="glass-card">
                    <h3 style="margin-bottom: 1.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border-color);">Hostel Profile</h3>
                    
                    <div class="form-group">
                        <span class="form-label">Roll Number</span>
                        <div class="detail-value" style="font-size: 1.1rem; font-weight: 600;">${sessionScope.user.username}</div>
                    </div>
                    
                    <div class="form-group">
                        <span class="form-label">Hostel Name</span>
                        <div class="detail-value">${sessionScope.user.hostelName}</div>
                    </div>
                    
                    <div class="form-group">
                        <span class="form-label">Room / Year / Branch</span>
                        <div class="detail-value">Room ${sessionScope.user.roomNo} | ${sessionScope.user.year} | ${sessionScope.user.branch}</div>
                    </div>

                    <div class="form-group">
                        <span class="form-label">Student Contact</span>
                        <div class="detail-value">${sessionScope.user.mobile}</div>
                    </div>

                    <div class="form-group" style="margin-bottom: 0;">
                        <span class="form-label">Parent Contact</span>
                        <div class="detail-value">${sessionScope.user.parentMobile}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
