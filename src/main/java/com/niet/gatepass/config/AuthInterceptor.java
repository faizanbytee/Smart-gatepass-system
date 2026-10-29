package com.niet.gatepass.config;

import com.niet.gatepass.model.Role;
import com.niet.gatepass.model.User;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

@Component
public class AuthInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String uri = request.getRequestURI();
        
        // Allow static resources and public login/logout endpoints
        if (uri.startsWith("/css/") || uri.startsWith("/js/") || uri.startsWith("/images/") ||
            uri.equals("/login") || uri.equals("/logout") || uri.equals("/error")) {
            return true;
        }

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect("/login?error=Please login first");
            return false;
        }

        User user = (User) session.getAttribute("user");
        Role role = user.getRole();

        // Path authorization checks
        if (uri.startsWith("/student/") && role != Role.STUDENT) {
            response.sendRedirect(getDashboardRedirect(role) + "?error=Unauthorized access");
            return false;
        }
        if (uri.startsWith("/warden/") && role != Role.WARDEN) {
            response.sendRedirect(getDashboardRedirect(role) + "?error=Unauthorized access");
            return false;
        }
        if (uri.startsWith("/guard/") && role != Role.GUARD) {
            response.sendRedirect(getDashboardRedirect(role) + "?error=Unauthorized access");
            return false;
        }
        if (uri.startsWith("/admin/") && role != Role.ADMIN) {
            response.sendRedirect(getDashboardRedirect(role) + "?error=Unauthorized access");
            return false;
        }

        return true;
    }

    private String getDashboardRedirect(Role role) {
        switch (role) {
            case STUDENT: return "/student/dashboard";
            case WARDEN: return "/warden/dashboard";
            case GUARD: return "/guard/dashboard";
            case ADMIN: return "/admin/dashboard";
            default: return "/login";
        }
    }
}
