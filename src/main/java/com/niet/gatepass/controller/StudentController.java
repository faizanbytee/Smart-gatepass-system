package com.niet.gatepass.controller;

import com.niet.gatepass.model.GatePass;
import com.niet.gatepass.model.PassStatus;
import com.niet.gatepass.model.PassType;
import com.niet.gatepass.model.User;
import com.niet.gatepass.repository.GatePassRepository;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import java.time.LocalDateTime;
import java.util.List;

@Controller
@RequestMapping("/student")
public class StudentController {

    @Autowired
    private GatePassRepository gatePassRepository;

    @GetMapping("/dashboard")
    public String dashboard(HttpSession session, Model model) {
        User student = (User) session.getAttribute("user");
        List<GatePass> myPasses = gatePassRepository.findByStudentOrderByCreatedAtDesc(student);
        
        long pendingCount = myPasses.stream().filter(p -> p.getStatus() == PassStatus.PENDING).count();
        long approvedCount = myPasses.stream().filter(p -> p.getStatus() == PassStatus.APPROVED).count();
        long outCount = myPasses.stream().filter(p -> p.getStatus() == PassStatus.OUT).count();
        
        model.addAttribute("myPasses", myPasses);
        model.addAttribute("pendingCount", pendingCount);
        model.addAttribute("approvedCount", approvedCount);
        model.addAttribute("outCount", outCount);
        return "student/dashboard";
    }

    @GetMapping("/request")
    public String showRequestForm() {
        return "student/request";
    }

    @PostMapping("/request")
    public String processRequest(@RequestParam("passType") String passType,
                                 @RequestParam("purpose") String purpose,
                                 @RequestParam("destination") String destination,
                                 @RequestParam("departureDateTime") String departureDateTimeStr,
                                 @RequestParam("expectedReturnDateTime") String expectedReturnDateTimeStr,
                                 HttpSession session,
                                 Model model) {
        User student = (User) session.getAttribute("user");
        
        try {
            LocalDateTime departureDateTime = LocalDateTime.parse(departureDateTimeStr);
            LocalDateTime expectedReturnDateTime = LocalDateTime.parse(expectedReturnDateTimeStr);
            
            if (expectedReturnDateTime.isBefore(departureDateTime)) {
                model.addAttribute("errorMessage", "Expected return time cannot be earlier than departure time.");
                return "student/request";
            }
            
            GatePass pass = new GatePass();
            pass.setStudent(student);
            pass.setPassType(PassType.valueOf(passType));
            pass.setPurpose(purpose);
            pass.setDestination(destination);
            pass.setDepartureDateTime(departureDateTime);
            pass.setExpectedReturnDateTime(expectedReturnDateTime);
            pass.setStatus(PassStatus.PENDING);
            pass.setCreatedAt(LocalDateTime.now());
            
            gatePassRepository.save(pass);
            return "redirect:/student/dashboard?success=Gate pass requested successfully";
            
        } catch (Exception e) {
            model.addAttribute("errorMessage", "Invalid date format. Please select valid date and time.");
            return "student/request";
        }
    }
}
