<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guard Dashboard - NIET GatePass</title>
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
                <span class="user-badge">${sessionScope.user.name} (Guard)</span>
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

        <div class="dashboard-grid">
            <!-- Left Side: Search and Actions -->
            <div>
                <!-- Look up Student -->
                <div class="glass-card" style="margin-bottom: 2rem;">
                    <h3 style="margin-bottom: 1rem;">Student Roll Number Look Up</h3>
                    <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.95rem;">Enter the student's roll number to check out/in their approved gate pass.</p>
                    
                    <form action="${pageContext.request.contextPath}/guard/dashboard" method="GET" class="search-container">
                        <input type="text" name="query" value="${searchQuery}" class="form-control" placeholder="Search by Student Roll Number..." required autocomplete="off">
                        <button type="submit" class="btn btn-primary">Search</button>
                    </form>

                    <!-- Search Results -->
                    <c:if test="${not empty searchQuery}">
                        <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: var(--text-secondary);">Search Results for "${searchQuery}"</h4>
                        
                        <c:choose>
                            <c:when test="${empty searchResults}">
                                <div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.02); border-radius: 8px; border: 1px dashed var(--border-color);">
                                    No active or approved gate pass found for this roll number.
                                </div>
                            </c:when>
                            <c:otherwise>
                                <c:forEach var="pass" items="${searchResults}">
                                    <div class="glass-card" style="margin-bottom: 1rem; background: rgba(15, 23, 42, 0.4); border-color: rgba(99, 102, 241, 0.3);">
                                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                                            <div>
                                                <h3 style="color: var(--primary); font-size: 1.2rem;">#GP-${pass.id} - ${pass.passType}</h3>
                                                <p style="font-weight: 600; font-size: 1.05rem; margin-top: 0.25rem;">${pass.student.name}</p>
                                                <p style="color: var(--text-secondary); font-size: 0.85rem;">Roll: ${pass.student.username} | Room: ${pass.student.roomNo} | ${pass.student.hostelName}</p>
                                            </div>
                                            <span class="badge badge-${pass.status.toString().toLowerCase()}">${pass.status}</span>
                                        </div>

                                        <div class="details-list">
                                            <div class="detail-item">
                                                <span class="detail-label">Purpose</span>
                                                <span class="detail-value">${pass.purpose}</span>
                                            </div>
                                            <div class="detail-item">
                                                <span class="detail-label">Destination</span>
                                                <span class="detail-value">${pass.destination}</span>
                                            </div>
                                            <div class="detail-item">
                                                <span class="detail-label">Departure Window</span>
                                                <span class="detail-value">
                                                    <fmt:parseDate value="${pass.departureDateTime}" pattern="yyyy-MM-dd'T'HH:mm" var="parsedDep" type="both"/>
                                                    <fmt:formatDate value="${parsedDep}" pattern="dd MMM, hh:mm a"/>
                                                </span>
                                            </div>
                                            <div class="detail-item">
                                                <span class="detail-label">Expected Return</span>
                                                <span class="detail-value" style="color: var(--warning); font-weight:600;">
                                                    <fmt:parseDate value="${pass.expectedReturnDateTime}" pattern="yyyy-MM-dd'T'HH:mm" var="parsedRet" type="both"/>
                                                    <fmt:formatDate value="${parsedRet}" pattern="dd MMM, hh:mm a"/>
                                                </span>
                                            </div>
                                        </div>

                                        <div style="border-top: 1px solid var(--border-color); padding-top: 1rem; margin-top: 1rem; display: flex; justify-content: space-between; align-items: center;">
                                            <span style="font-size: 0.85rem; color: var(--text-secondary);">Warden: <strong>${pass.approvedBy.name}</strong></span>
                                            
                                            <c:if test="${pass.status == 'APPROVED'}">
                                                <form action="${pageContext.request.contextPath}/guard/checkout" method="POST" class="inline-form">
                                                    <input type="hidden" name="passId" value="${pass.id}">
                                                    <button type="submit" class="btn btn-success">Log Checkout (Exit)</button>
                                                </form>
                                            </c:if>
                                            <c:if test="${pass.status == 'OUT'}">
                                                <form action="${pageContext.request.contextPath}/guard/checkin" method="POST" class="inline-form">
                                                    <input type="hidden" name="passId" value="${pass.id}">
                                                    <button type="submit" class="btn btn-primary">Log Checkin (Return)</button>
                                                </form>
                                            </c:if>
                                        </div>
                                    </div>
                                </c:forEach>
                            </c:otherwise>
                        </c:choose>
                    </c:if>
                </div>

                <!-- Recently Returned Log -->
                <div class="glass-card">
                    <h3 style="margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Recently Returned Students</h3>
                    <c:choose>
                        <c:when test="${empty recentlyReturned}">
                            <p style="color: var(--text-secondary); text-align: center; padding: 1.5rem 0;">No checkins recorded recently.</p>
                        </c:when>
                        <c:otherwise>
                            <div class="table-container">
                                <table class="custom-table">
                                    <thead>
                                        <tr>
                                            <th>Roll No</th>
                                            <th>Student Name</th>
                                            <th>Exit Time</th>
                                            <th>Entry Time</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <c:forEach var="pass" items="${recentlyReturned}">
                                            <tr>
                                                <td style="font-weight: 500;">${pass.student.username}</td>
                                                <td>${pass.student.name}</td>
                                                <td style="font-size: 0.85rem; color: var(--text-secondary);">
                                                    <fmt:parseDate value="${pass.actualExitTime}" pattern="yyyy-MM-dd'T'HH:mm" var="parsedExit" type="both"/>
                                                    <fmt:formatDate value="${parsedExit}" pattern="dd MMM, hh:mm a"/>
                                                </td>
                                                <td style="font-size: 0.85rem; color: var(--success); font-weight: 600;">
                                                    <fmt:parseDate value="${pass.actualEntryTime}" pattern="yyyy-MM-dd'T'HH:mm" var="parsedEntry" type="both"/>
                                                    <fmt:formatDate value="${parsedEntry}" pattern="dd MMM, hh:mm a"/>
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

            <!-- Right Side: Students currently out -->
            <div>
                <div class="glass-card" style="height: 100%;">
                    <h3 style="margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Students Currently Outside</h3>
                    
                    <c:choose>
                        <c:when test="${empty checkedOutPasses}">
                            <p style="color: var(--text-secondary); text-align: center; padding: 2rem 0;">No students are outside currently.</p>
                        </c:when>
                        <c:otherwise>
                            <div style="display: flex; flex-direction: column; gap: 1rem;">
                                <c:forEach var="pass" items="${checkedOutPasses}">
                                    <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem;">
                                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                                            <div>
                                                <span style="font-weight: 600; font-size: 0.95rem;">${pass.student.name}</span>
                                                <br>
                                                <span style="font-size: 0.8rem; color: var(--text-secondary);">${pass.student.username} | Room ${pass.student.roomNo}</span>
                                            </div>
                                            <form action="${pageContext.request.contextPath}/guard/checkin" method="POST" class="inline-form">
                                                <input type="hidden" name="passId" value="${pass.id}">
                                                <button type="submit" class="btn btn-primary" style="padding: 0.35rem 0.7rem; font-size: 0.8rem;">Return</button>
                                            </form>
                                        </div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            Exit: 
                                            <fmt:parseDate value="${pass.actualExitTime}" pattern="yyyy-MM-dd'T'HH:mm" var="parsedExit" type="both"/>
                                            <fmt:formatDate value="${parsedExit}" pattern="dd MMM, hh:mm a"/>
                                        </div>
                                        <div style="font-size: 0.85rem; color: var(--warning);">
                                            Exp: 
                                            <fmt:parseDate value="${pass.expectedReturnDateTime}" pattern="yyyy-MM-dd'T'HH:mm" var="parsedRet" type="both"/>
                                            <fmt:formatDate value="${parsedRet}" pattern="dd MMM, hh:mm a"/>
                                        </div>
                                    </div>
                                </c:forEach>
                            </div>
                        </c:otherwise>
                    </c:choose>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
