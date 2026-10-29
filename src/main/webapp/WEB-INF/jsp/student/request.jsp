<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Request Gate Pass - NIET GatePass</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
    <script>
        function validateDates() {
            var depVal = document.getElementById("departureDateTime").value;
            var retVal = document.getElementById("expectedReturnDateTime").value;
            if (depVal && retVal) {
                var depDate = new Date(depVal);
                var retDate = new Date(retVal);
                if (retDate <= depDate) {
                    alert("Expected Return Time must be after Departure Time!");
                    return false;
                }
            }
            return true;
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
                <span class="user-badge">${sessionScope.user.name} (Student)</span>
                <a href="${pageContext.request.contextPath}/logout" class="logout-btn">Logout</a>
            </div>
        </nav>

        <div style="max-width: 600px; margin: 0 auto;">
            <div class="glass-card">
                <h2 class="title-gradient" style="margin-bottom: 0.5rem;">New Gate Pass Request</h2>
                <p style="color: var(--text-secondary); margin-bottom: 2rem;">Please fill out all the details accurately for warden review.</p>

                <c:if test="${not empty errorMessage}">
                    <div class="alert alert-danger">
                        <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                        </svg>
                        <span>${errorMessage}</span>
                    </div>
                </c:if>

                <form action="${pageContext.request.contextPath}/student/request" method="POST" onsubmit="return validateDates();">
                    <div class="form-group">
                        <label class="form-label" for="passType">Pass Type</label>
                        <select id="passType" name="passType" class="form-control" required>
                            <option value="OUTING">Local Outing (Hours-based)</option>
                            <option value="LEAVE">Home Leave (Days-based)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="purpose">Purpose of Outing</label>
                        <input type="text" id="purpose" name="purpose" class="form-control" placeholder="e.g. Buying books, Visiting home, Medical checkup" required autocomplete="off">
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="destination">Destination Address</label>
                        <input type="text" id="destination" name="destination" class="form-control" placeholder="e.g. Greater Noida Alpha-1, New Delhi, Home Address" required autocomplete="off">
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="departureDateTime">Departure Date & Time</label>
                        <input type="datetime-local" id="departureDateTime" name="departureDateTime" class="form-control" required>
                    </div>

                    <div class="form-group" style="margin-bottom: 2rem;">
                        <label class="form-label" for="expectedReturnDateTime">Expected Return Date & Time</label>
                        <input type="datetime-local" id="expectedReturnDateTime" name="expectedReturnDateTime" class="form-control" required>
                    </div>

                    <div style="display: flex; gap: 1rem;">
                        <button type="submit" class="btn btn-primary" style="flex: 1;">Submit Application</button>
                        <a href="${pageContext.request.contextPath}/student/dashboard" class="btn btn-secondary" style="flex: 1; text-align: center;">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
