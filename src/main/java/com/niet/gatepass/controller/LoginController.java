package com.niet.gatepass.controller;

import com.niet.gatepass.model.User;
import com.niet.gatepass.repository.UserRepository;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import java.util.Optional;

@Controller
public class LoginController {

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/")
    public String index(HttpSession session) {
        if (session != null && session.getAttribute("user") != null) {
            User user = (User) session.getAttribute("user");
            return "redirect:/" + user.getRole().name().toLowerCase() + "/dashboard";
        }
        return "redirect:/login";
    }

    @GetMapping("/login")
    public String showLoginForm(@RequestParam(value = "error", required = false) String error, Model model, HttpSession session) {
        if (session != null && session.getAttribute("user") != null) {
            User user = (User) session.getAttribute("user");
            return "redirect:/" + user.getRole().name().toLowerCase() + "/dashboard";
        }
        if (error != null) {
            model.addAttribute("errorMessage", error);
        }
        return "login";
    }

    @PostMapping("/login")
    public String processLogin(@RequestParam("username") String username,
                               @RequestParam("password") String password,
                               HttpSession session,
                               Model model) {
        Optional<User> userOpt = userRepository.findByUsername(username);

        if (userOpt.isPresent() && userOpt.get().getPassword().equals(password)) {
            User user = userOpt.get();
            session.setAttribute("user", user);
            return "redirect:/" + user.getRole().name().toLowerCase() + "/dashboard";
        } else {
            model.addAttribute("errorMessage", "Invalid Username or Password");
            return "login";
        }
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        if (session != null) {
            session.invalidate();
        }
        return "redirect:/login?error=Logged out successfully";
    }
}
