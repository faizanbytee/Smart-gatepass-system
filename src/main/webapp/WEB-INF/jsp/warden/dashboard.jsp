<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Warden Dashboard - NIET GatePass</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
    <script>
        function submitWithRemarks(action, passId, studentName) {
            var actionText = action === 'approve' ? 'APPROVE' : 'REJECT';
            var remarks = prompt("Enter remarks for " + actionText + " of gate pass for " + studentName + ":");
            if (remarks === null) return; // cancelled
            
            // Create a dynamic form to submit
            var form = document.createElement("form");
            form.setAttribute("method", "post");
            form.setAttribute("action", "${pageContext.request.contextPath}/warden/" + action);
            
            var passIdInput = document.createElement("input");
            passIdInput.setAttribute("type", "hidden");
            passIdInput.setAttribute("name", "passId");
            passIdInput.setAttribute("value", passId);
            form.appendChild(passIdInput);
            
            var remarksInput = document.createElement("input");
            remarksInput.setAttribute("type", "hidden");
            remarksInput.setAttribute("name", "remarks");
            remarksInput.setAttribute("value", remarks);
            form.appendChild(remarksInput);
            
            document.body.appendChild(form);
            form.submit();
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
                <span class="user-badge">${sessionScope.user.name} (Warden)</span>
                <a href="${pageContext.request.contextPath}/logout" class="logout-btn">Logout</a>
            </div>
        </nav>

        <!-- Notification messages -->
        <c:if test="${not empty param.success}">
            <div class="alert alert-success">
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>${param.success}</span>
            </div>
        </c:if>

        <!-- Stats cards -->
        <div class="stats-grid">
            <div class="stat-card warning">
                <span class="stat-title">Pending Approvals</span>
                <span class="stat-value">${pendingCount}</span>
            </div>
            <div class="stat-card primary">
                <span class="stat-title">Currently Checked Out</span>
                <span class="stat-value">${activeOutCount}</span>
            </div>
            <div class="stat-card success">
                <span class="stat-title">Total Processed</span>
                <span class="stat-value">${totalProcessed}</span>
            </div>
        </div>

        <!-- Pending Requests -->
        <div class="glass-card" style="margin-bottom: 2.5rem;">
            <h3 style="margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Pending Gate Pass Applications</h3>
            
            <c:choose>
                <c:when test="${empty pendingPasses}">
                    <p style="color: var(--text-secondary); text-align: center; padding: 2rem 0;">No pending gate pass requests.</p>
                </c:when>
                <c:otherwise>
                    <div class="table-container">
                        <table class="custom-table">
                            <thead>
                                <tr>
                                    <th>Student</th>
                                    <th>Room / Hostel</th>
                                    <th>Pass Type</th>
                                    <th>Purpose / Destination</th>
                                    <th>Departure</th>
                                    <th>Exp. Return</th>
                                    <th style="text-align: center;">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <c:forEach var="pass" items="${pendingPasses}">
                                    <tr>
                                        <td>
                                            <div style="font-weight: 600;">${pass.student.name}</div>
                                            <div style="font-size: 0.8rem; color: var(--text-secondary);">${pass.student.username} (${pass.student.branch})</div>
                                        </td>
                                        <td>
                                            <div>Room ${pass.student.roomNo}</div>
                                            <div style="font-size: 0.8rem; color: var(--text-secondary);">${pass.student.hostelName}</div>
                                        </td>
                                        <td>
                                            <span style="font-weight: 500;">${pass.passType}</span>
                                        </td>
                                        <td>
                                            <div>${pass.purpose}</div>
                                            <div style="font-size: 0.8rem; color: var(--text-secondary);">Dest: ${pass.destination}</div>
                                        </td>
                                        <td>
                                            <fmt:parseDate value="${pass.departureDateTime}" pattern="yyyy-MM-dd'T'HH:mm" var="parsedDep" type="both"/>
                                            <fmt:formatDate value="${parsedDep}" pattern="dd MMM, hh:mm a"/>
                                        </td>
                                        <td>
                                            <fmt:parseDate value="${pass.expectedReturnDateTime}" pattern="yyyy-MM-dd'T'HH:mm" var="parsedRet" type="both"/>
                                            <fmt:formatDate value="${parsedRet}" pattern="dd MMM, hh:mm a"/>
                                        </td>
                                        <td style="text-align: center;">
                                            <div style="display: flex; gap: 0.5rem; justify-content: center;">
                                                <button onclick="submitWithRemarks('approve', '${pass.id}', '${pass.student.name}')" class="btn btn-success" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;">Approve</button>
                                                <button onclick="submitWithRemarks('reject', '${pass.id}', '${pass.student.name}')" class="btn btn-danger" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;">Reject</button>
                                            </div>
                                        </td>
                                    </tr>
                                </c:forEach>
                            </tbody>
                        </table>
                    </div>
                </c:otherwise>
            </c:choose>
        </div>

        <!-- History Log -->
        <div class="glass-card">
            <h3 style="margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Processed Passes Log</h3>
            
            <c:choose>
                <c:when test="${empty historyPasses}">
                    <p style="color: var(--text-secondary); text-align: center; padding: 2rem 0;">No historical passes recorded.</p>
                </c:when>
                <c:otherwise>
                    <div class="table-container">
                        <table class="custom-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Student</th>
                                    <th>Details</th>
                                    <th>Departure</th>
                                    <th>Exp. Return</th>
                                    <th>Status</th>
                                    <th>Processed By</th>
                                    <th>Remarks</th>
                                </tr>
                            </thead>
                            <tbody>
                                <c:forEach var="pass" items="${historyPasses}">
                                    <tr>
                                        <td>#GP-${pass.id}</td>
                                        <td>
                                            <div style="font-weight: 500;">${pass.student.name}</div>
                                            <div style="font-size: 0.8rem; color: var(--text-secondary);">${pass.student.username}</div>
                                        </td>
                                        <td>
                                            <div>Type: ${pass.passType}</div>
                                            <div style="font-size: 0.8rem; color: var(--text-secondary);">${pass.purpose}</div>
                                        </td>
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
                                                <c:when test="${not empty pass.approvedBy}">
                                                    <span style="font-size: 0.9rem;">${pass.approvedBy.name}</span>
                                                </c:when>
                                                <c:otherwise>
                                                    <span style="color: var(--text-muted);">-</span>
                                                </c:otherwise>
                                            </c:choose>
                                        </td>
                                        <td>
                                            <c:choose>
                                                <c:when test="${not empty pass.remarks}">
                                                    <span style="font-style: italic; font-size: 0.9rem; color: var(--text-secondary);">${pass.remarks}</span>
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
</body>
</html>
