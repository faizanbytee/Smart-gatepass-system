package com.niet.gatepass.controller;

import com.niet.gatepass.model.Role;
import com.niet.gatepass.model.User;
import com.niet.gatepass.repository.UserRepository;
import com.niet.gatepass.repository.GatePassRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("/admin")
public class AdminController {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private GatePassRepository gatePassRepository;

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        List<User> users = userRepository.findAll();
        
        long totalUsers = users.size();
        long studentCount = users.stream().filter(u -> u.getRole() == Role.STUDENT).count();
        long wardenCount = users.stream().filter(u -> u.getRole() == Role.WARDEN).count();
        long guardCount = users.stream().filter(u -> u.getRole() == Role.GUARD).count();
        long totalPasses = gatePassRepository.count();

        model.addAttribute("users", users);
        model.addAttribute("roles", Role.values());
        model.addAttribute("totalUsers", totalUsers);
        model.addAttribute("studentCount", studentCount);
        model.addAttribute("wardenCount", wardenCount);
        model.addAttribute("guardCount", guardCount);
        model.addAttribute("totalPasses", totalPasses);
        
        return "admin/dashboard";
    }

    @PostMapping("/user/add")
    public String addUser(@RequestParam("username") String username,
                          @RequestParam("password") String password,
                          @RequestParam("name") String name,
                          @RequestParam("role") String roleStr,
                          @RequestParam("email") String email,
                          @RequestParam("mobile") String mobile,
                          @RequestParam(value = "hostelName", required = false) String hostelName,
                          @RequestParam(value = "roomNo", required = false) String roomNo,
                          @RequestParam(value = "branch", required = false) String branch,
                          @RequestParam(value = "year", required = false) String year,
                          @RequestParam(value = "parentMobile", required = false) String parentMobile,
                          Model model) {
        
        Optional<User> existing = userRepository.findByUsername(username);
        if (existing.isPresent()) {
            return "redirect:/admin/dashboard?error=Username already exists";
        }

        try {
            Role role = Role.valueOf(roleStr);
            User user = new User();
            user.setUsername(username);
            user.setPassword(password);
            user.setName(name);
            user.setRole(role);
            user.setEmail(email);
            user.setMobile(mobile);
            
            if (role == Role.STUDENT) {
                user.setHostelName(hostelName);
                user.setRoomNo(roomNo);
                user.setBranch(branch);
                user.setYear(year);
                user.setParentMobile(parentMobile);
            }
            
            userRepository.save(user);
            return "redirect:/admin/dashboard?success=User added successfully";
        } catch (Exception e) {
            return "redirect:/admin/dashboard?error=Failed to add user: " + e.getMessage();
        }
    }

    @PostMapping("/user/delete")
    public String deleteUser(@RequestParam("userId") Long userId) {
        try {
            userRepository.deleteById(userId);
            return "redirect:/admin/dashboard?success=User deleted successfully";
        } catch (Exception e) {
            return "redirect:/admin/dashboard?error=Failed to delete user: " + e.getMessage();
        }
    }
}
